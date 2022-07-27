import datetime
import random
import re
import time

import requests
from chinese_calendar import is_workday
from hyper import HTTP20Connection


def get_sample(url, headers):
    return requests.get(url, headers=headers)


def post_sample(url, headers, data=None):
    return requests.post(url, headers=headers, data=data)


def get(host, path, headers):
    return request(host, 'GET', path, headers)


def post(host, path, headers, data=None):
    return request(host, 'POST', path, headers, data)


def request(host, method, path, headers=None, body=None):
    if headers is None:
        headers = {}
    headers['Accept'] = '*/*'
    headers['Connection'] = 'keep-alive'
    c = HTTP20Connection(host)
    response = c.request(method, path, headers=headers, body=body)
    resp = c.get_response(response)
    return resp.read().decode('utf-8')


def convert_cookies_to_dict(cookies, delimiter="; |;|, |,"):
    """
    cookie 转换成 字典
    :param cookies:
    :param delimiter:
    :return:
    """
    cookies = dict([l.split("=", 1) for l in re.split(delimiter, cookies)])
    return cookies


def send_message(content, title='今日头条极速版'):
    token = '258f84f44f0246c38bffb7d03733a825'
    url = 'http://www.pushplus.plus/send'
    requests.post(url, data={"token": token, "title": title, "content": content, "channel": "cp", "webhook": "4680"})


def todat_is_workday():
    """
    今天是否是工作日
    """
    da = datetime.date.today()
    return is_workday(da)


def randomtimes(start, end, n, frmt="%Y-%m-%d %H:%M:%S", istimestamp=False):
    """
    随机获得一段时间内的一组时间
    """
    return [randomtime(start, end, frmt, istimestamp) for _ in range(n)]


def randomtime(start, end, frmt="%Y-%m-%d %H:%M:%S", istimestamp=True):
    """
    随机获得一段时间内的某一个时间
    """
    stime = datetime.datetime.strptime(start, frmt)
    etime = datetime.datetime.strptime(end, frmt)
    res = random.random() * (etime - stime) + stime
    return res if istimestamp is not True else int(datetime.datetime.timestamp(res) * 1000)


def get_today_ymd():
    """
    获得今天的时间，格式如2022-07-20
    """
    today = datetime.date.today()
    year = today.year
    month = today.month
    day = today.day
    return '{}-{:0>2d}-{:0>2d}'.format(year, month, day)


def get_today_hm(hm):
    """
    获得今天某一时分的时间
    """
    today = get_today_ymd()
    return '{} {}'.format(today, hm)


def get_today_hm_timestamp(hm):
    """
    获得今天某一时分的时间戳
    """
    hmstr = get_today_hm(hm)
    # 先转换为时间数组
    timeArray = time.strptime(hmstr, "%Y-%m-%d %H:%M:%S")
    # 转换为时间戳
    return int(time.mktime(timeArray) * 1000)


def timestamp_format(timestamp):
    """
    时间戳格式化
    """
    # 转换为其他日期格式,如:"%Y-%m-%d %H:%M:%S"
    timeArray = time.localtime(timestamp)
    return time.strftime("%Y-%m-%d %H:%M:%S", timeArray)


if __name__ == '__main__':
    print(int(time.time() * 1000))
