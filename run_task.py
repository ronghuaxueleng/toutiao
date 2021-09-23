import argparse
import json
import time
from urllib.parse import urlencode

from peewee import JOIN

from toutiao.db import Task as DbTask, Account, CommonParams
from toutiao.toutiao import save_ad
from utils.utils import get, post, request, send_message


# 签到
def sign_in(headers, query):
    sign_in_host = 'i-hl.snssdk.com'
    sign_in_path = '/luckycat/lite/v1/sign_in/action?{}'
    path = sign_in_path.format(query)
    res = post(sign_in_host, path, headers, b'{"rit": "coin", "use_ecpm": "0"}')
    print('sign_in ' + res)


# 打开通知
def open_notice(headers, query):
    host = 'api3-normal-c-hl.snssdk.com'
    path = '/luckycat/lite/v1/task/done_apply_permission?{}'.format(query)
    headers['content-type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
    data = 'body=null'
    res = post(host, path, headers, data)
    print('open_notice ' + res)


# 新人阅读
def newbie_consume(headers, query):
    host = 'api3-normal-c-hl.snssdk.com'
    path = '/score_task/lite/v1/newbie_consume/done_consume/?{}'.format(query)
    headers['content-type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
    res = post(host, path, headers, query)
    print('newbie_consume' + res)


# 点击翻倍
def double_whole_scene_task(headers, query):
    host = 'i-hl.snssdk.com'
    path = '/luckycat/lite/v1/activity/double_whole_scene_task/?{}'.format(query)
    res = post(host, path, headers)
    print('double_whole_scene_task' + res)


# 阅读推送文章
def get_push_read_bonus(headers, query, account):
    get_read_bonus(headers, query, account)


# 阅读
def get_read(headers, query, account):
    get_read_bonus(headers, query, account, False)


# 走路赚金币
def walk_count(headers, query):
    host = 'i-hl.snssdk.com'
    path = '/luckycat/lite/v1/walk/count/?{}'.format(query)
    data = {"count": 20000, "client_time": int(time.time())}
    res = post(host, path, headers, json.dumps(data))
    print('walk_count' + res)
    walk_bonus_136(headers, query)


# 领取走路赚钱奖励
def walk_bonus_136(headers, query):
    host = 'i-hl.snssdk.com'
    bonus_path = '/luckycat/lite/v1/walk/bonus/?{}'.format(query)
    data = {"task_id": 136, "client_time": int(time.time()), "rit": "coin", "use_ecpm": 0}
    res = post(host, bonus_path, headers, json.dumps(data))
    print('walk_bonus_136' + res)


# 领取走路赚钱满勤奖
def walk_bonus_137(headers, query):
    host = 'i-hl.snssdk.com'
    bonus_path = '/luckycat/lite/v1/walk/bonus/?{}'.format(query)
    data = {"task_id": 137, "client_time": int(time.time()), "rit": "coin", "use_ecpm": 0}
    res = post(host, bonus_path, headers, json.dumps(data))
    print('walk_bonus_137' + res)


# 金币详情
def profit_detail(headers, query, account, fromAPI = False):
    host = 'i-hl.snssdk.com'
    path = '/luckycat/lite/v1/user/profit_detail/?offset=6922228539857356812&num=300&income_type=1&{}'.format(
        query)
    res = get(host, path, headers)
    res_json = json.loads(res)
    err_no = res_json['err_no']
    if err_no == 0:
        data = res_json['data']
        score_balance = data['score_balance'] if data is not None else '-'
        cash_balance = data['cash_balance'] if data is not None else 0
        cash_amount = data['cash_amount'] if data is not None else 0
        if fromAPI is False:
            return '{}：现有金币{}，现金收益{}，总收益{}'.format(account.name, score_balance, cash_balance / 100, cash_amount / 100)
        else:
            return {
                'name': account.name,
                'score_balance': score_balance,
                'cash_balance': cash_balance / 100,
                'cash_amount': cash_amount / 100
            }
    elif err_no == 10001:
        if fromAPI is False:
            return '{} 请重新登录'.format(account.name)
        else:
            return {
                'name': account.name,
                'score_balance': '请重新登录',
                'cash_balance': '请重新登录',
                'cash_amount': '请重新登录'
            }


# 阅读
def get_read_bonus(headers, query, account, is_push=True):
    try:
        # 文章列表
        feed_host = 'iu.snssdk.com'
        feed_path = '/api/news/feed/v64/?{}'.format(query)
        res = post(feed_host, feed_path, headers)
        res_json = json.loads(res)
        for item in res_json['data']:
            d = json.loads(item['content'])
            group_id = d.get('group_id')
            if group_id is not None:
                push = 'push' if is_push else ''
                read_bonus_host = 'is.snssdk.com'
                read_bonus_path = '/score_task/v1/task/get_read_bonus/?group_id={}&impression_type={}&{}'
                path = read_bonus_path.format(group_id, push, query)
                res = get(read_bonus_host, path, headers)
                print(json.loads(res))
                print(account.name + '：get_read_bonus ' + res)
                time.sleep(10)
    except Exception:
        pass


# 开始睡觉
def start_sleep(headers, query):
    host = 'i-hl.snssdk.com'
    start_path = '/luckycat/lite/v1/sleep/start/?_request_from=web&{}'.format(query)
    res = post(host, start_path, headers)
    print('start_sleep' + res)


# 停止睡觉
def end_sleep(headers, query):
    host = 'i-hl.snssdk.com'
    stop_path = '/luckycat/lite/v1/sleep/stop/?_request_from=web&{}'.format(query)
    res = post(host, stop_path, headers)
    print('sleep_stop' + res)


# 领取睡觉奖励
def sleep_done_task(headers, query):
    host = 'i-hl.snssdk.com'
    status_path = '/luckycat/lite/v1/sleep/status/?_request_from=web&{}'.format(query)
    res = get(host, status_path, headers)
    print('sleep_status' + res)
    res_json = json.loads(res)
    data = res_json['data']
    history_amount = data['history_amount']
    done_task_path = '/luckycat/lite/v1/sleep/done_task/?_request_from=web&device_platform=undefined&{}'.format(query)
    res = post(host, done_task_path, headers, json.dumps({"score_amount": history_amount}))
    print('sleep_done_task' + res)


# 删除失效任务
def delete_shixiao_task():
    session_keys = [session_key.get('session_key') for session_key in Account.select(Account.session_key).dicts()]
    DbTask.delete().where(DbTask.session_key.not_in(session_keys)).execute()


iads = ['爱步宝']


# 获得喜爱的广告
def get_ad(headers, query):
    host = 'api3-normal-lf.toutiaoapi.com'
    status_path = '/api/ad/v1/inspire/?van_package=1&ad_count=1&creator_id=2000&client_extra_params=%7B%22ad_download%22%3A%7B%7D%7D&ad_from=coin&enable_one_more=true&{}'.format(
        query)
    res = get(host, status_path, headers)
    if res is not None:
        res_json = json.loads(res)
        ad_item = res_json.get('ad_item')
        if ad_item is not None:
            for item in ad_item:
                try:
                    data = item.get('dynamic_ad').get('data')
                    source = data.get('source')
                    if source in iads:
                        web_url = data.get('web_url')
                        save_ad(source, web_url)
                except Exception as e:
                    pass


def run_accout_task(type):
    results = []
    accounts = Account.select()
    for idx, account in enumerate(accounts):
        headers = json.loads(account.headers)
        params = CommonParams.select().where(CommonParams.user_id == account.user_id).dicts().get()
        query = urlencode(params)
        if type == 'sign_in':
            sign_in(headers, query)
        elif type == 'get_ad':
            get_ad(headers, query)
        elif type == 'open_notice':
            open_notice(headers, query)
        elif type == 'newbie_consume':
            newbie_consume(headers, query)
        elif type == 'double_whole_scene_task':
            double_whole_scene_task(headers, query)
        elif type == 'get_push_read_bonus':
            get_push_read_bonus(headers, query, account)
        elif type == 'get_read':
            get_read(headers, query, account)
        elif type == 'walk_count':
            walk_count(headers, query)
        elif type == 'profit_detail':
            result = profit_detail(headers, query, account)
            results.append(result)
        elif type == 'walk_bonus_136':
            walk_bonus_136(headers, query)
        elif type == 'walk_bonus_137':
            walk_bonus_137(headers, query)
        elif type == 'start_sleep':
            start_sleep(headers, query)
        elif type == 'end_sleep':
            end_sleep(headers, query)
        elif type == 'sleep_done_task':
            sleep_done_task(headers, query)
    if len(results) > 0:
        send_message("\n".join(results))


new_excitation_ad_task_ids = ["188", "308", "216", "255"]


def new_excitation_ad(host, method, path, headers, taskId, task, task_type, session_key):
    try:
        res = request(host, method, path, json.loads(headers), '{"task_id":"' + taskId + '"}')
        print('{} - {} - {} {}'.format(task['name'], task_type, session_key, res))
        res_json = json.loads(res)
        if res_json.get("err_no") == 0:
            new_excitation_ad(host, method, path, headers, taskId, task, task_type, session_key)
    except Exception as e:
        print('{} - {} - {}执行失败'.format(task['name'], task_type, session_key))


def run_task(task_type):
    query = (DbTask.select(DbTask, Account).join(Account, JOIN.LEFT_OUTER,
                                                 on=(DbTask.session_key == Account.session_key))
             # .where(DbTask.type == task_type, DbTask.session_key == '3b5be15157963546ef0c58a394d40119').dicts())
             .where(DbTask.type == task_type).dicts())
    for idx, task in enumerate(query):
        session_key = task['session_key']
        host = task['host']
        path = task['path']
        method = task['method']
        headers = task['header']
        body = task['body']
        if task_type == 'new_excitation_ad':
            for taskId in new_excitation_ad_task_ids:
                new_excitation_ad(host, method, path, headers, taskId, task, task_type, session_key)
        elif task_type == 'open_treasure_box':
            res = request(host, method, path, json.loads(headers), body)
            print('{} - {} - {} {}'.format(task['name'], task_type, session_key, res))
            res_json = json.loads(res)
            if res_json.get("err_no") == 0:
                for taskId in new_excitation_ad_task_ids:
                    new_excitation_ad(host, method, path, headers, taskId, task, 'new_excitation_ad', session_key)
        else:
            try:
                res = request(host, method, path, json.loads(headers), body)
                print('{} - {} - {} {}'.format(task['name'], task_type, session_key, res))
                res_json = json.loads(res)
                if res_json.get("err_no") == 0:
                    for taskId in new_excitation_ad_task_ids:
                        new_excitation_ad(host, method, path, headers, taskId, task, 'new_excitation_ad', session_key)
            except Exception as e:
                print('{} - {} - {}执行失败'.format(task['name'], task_type, session_key))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='今日头条运行')
    parser.add_argument('--ltype', '-lt', help='主任务类型，必要参数', default=0)
    parser.add_argument('--type', '-t', help='任务类型，必要参数', required=True)
    args = parser.parse_args()
    ltype = args.ltype
    type = args.type
    if ltype == '1':
        run_task(type)
    else:
        run_accout_task(type)
