# 爱步宝
import argparse
import json
import random
import re
import time

import requests
from toutiao.db import Abb

from bs4 import BeautifulSoup

# 签到
from toutiao.toutiao import abbPhoneReg, abbMoneyReg, abbAliNameReg, abbAlipayReg
from utils.utils import send_message


def signin(headers):
    url = "http://front15.ncziliyun.com/handle/signin.html"
    payload = "phone=1"
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)


# 提交步数
def convert_step(headers):
    url = "http://front15.ncziliyun.com/mobile/convert_step.html"
    payload = "todayStep={}".format(20000 + random.randint(100, 1000))
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)


# 提现
def fuli(headers):
    url = "http://front15.ncziliyun.com/user/fuli.html"
    requests.request("POST", url, headers=headers)


# 早起挑战赛报名
def getup(headers):
    url = "http://front15.ncziliyun.com/mobile/getup/apply.html"
    payload = 'cost=money'
    requests.request("POST", url, headers=headers, data=payload)
    url = "http://front15.ncziliyun.com/handle/apply.html"
    payload = "phone=1"
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)


# 早起打卡
def getup_clock(headers):
    url = "http://front15.ncziliyun.com/mobile/getup/clock.html"
    requests.request("GET", url, headers=headers)


# 提现记录
def record(headers, nick, money, fromApi=False):
    url = "http://front15.ncziliyun.com/user/cash/record.html"
    response = requests.request("GET", url, headers=headers)
    html = response.text
    soup = BeautifulSoup(html, 'lxml')
    finder = soup.find('table')
    rows = finder.find_all('tr')
    succ_total = 0
    processing = []
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        if len(cols) > 0:
            if cols[2] == '提现成功':
                succ_total += float(cols[0])
            if cols[2] == '处理中':
                processing.append("时间【{}】，金额: {}元".format(cols[1], cols[0]))
    if fromApi is False:
        if len(processing) > 0:
            return "{}\n共提现金额:{}元，还有{}笔提现正在处理，如下：\n{}".format(nick, succ_total, len(processing), "\n".join(processing))
        else:
            return "{}\n共提现金额:{}元，没有正在处理的提现款项".format(nick, succ_total)
    else:
        return {
            'nick': nick,
            'money': money,
            'succ_total': succ_total,
            'processing': 0 if len(processing) == 0 else "\n".join(processing)
        }


# 获得支付宝信息
def getalipay(headers, uid):
    url = "http://front15.ncziliyun.com/user/alipay.html"
    response = requests.request("GET", url, headers=headers)
    body = response.text
    aliNameMatch = abbAliNameReg.search(body)
    aliPayMatch = abbAlipayReg.search(body)
    if aliNameMatch is not None and aliPayMatch is not None:
        aliNames = aliNameMatch.groupdict()
        aliName = aliNames.get("aliname")
        aliPays = aliPayMatch.groupdict()
        aliPay = aliPays.get("alipay")
        Abb.update(
            alipay='{}:{}'.format(aliName, aliPay)
        ).where(Abb.uid == uid).execute()


# 获得账号信息
def getperson(headers, uid):
    url = "http://front15.ncziliyun.com/user/person.html"
    response = requests.request("GET", url, headers=headers)
    body = response.text
    phoneMatch = abbPhoneReg.search(body)
    moneyMatch = abbMoneyReg.search(body)
    if phoneMatch is not None and moneyMatch is not None:
        phones = phoneMatch.groupdict()
        phone = phones.get("phone")
        moneys = moneyMatch.groupdict()
        money = moneys.get("money")
        Abb.update(
            phone=phone,
            money=money
        ).where(Abb.uid == uid).execute()


extype = ['record', 'getalipay', 'getperson']


def run_accout_task(type):
    items = Abb.select().dicts()
    results = []
    for item in items:
        if type not in extype:
            # 休眠1-100秒之间一个数执行
            sec = random.randint(1, 100)
            print("休眠{}秒后继续执行".format(sec))
            time.sleep(sec)
        uid = item.get('uid')
        nick = item.get('nick')
        money = item.get('money')
        print("\n" + nick + "\n")
        header = item.get('header')
        header_json = json.loads(header)
        if type == 'convert_step':
            convert_step(header_json)
        elif type == 'signin':
            signin(header_json)
        elif type == 'fuli':
            fuli(header_json)
        elif type == 'record':
            results.append(record(header_json, nick, money))
        elif type == 'getup':
            getup(header_json)
        elif type == 'getup_clock':
            getup_clock(header_json)
        elif type == 'getalipay':
            getalipay(header_json, uid)
        elif type == 'getperson':
            getperson(header_json, uid)

    if len(results) > 0:
        send_message("\n".join(results), '爱步宝')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--type', '-t', help='任务类型，必要参数', required=True)
    args = parser.parse_args()
    run_accout_task(args.type)
