import argparse
import json
import time
from urllib.parse import urlencode

from peewee import JOIN

from toutiao.db import Task as DbTask, Account, CommonParams
from toutiao.utils import get, post, request


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
    data = {"count": 5000, "client_time": int(time.time())}
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
def profit_detail(headers, query, account):
    host = 'i-hl.snssdk.com'
    path = '/luckycat/lite/v1/user/profit_detail/?offset=6922228539857356812&num=300&income_type=1&{}'.format(
        query)
    res = get(host, path, headers)
    res_json = json.loads(res)
    print('{}：现有金币{}, ：现金收益{}'.format(account.name, res_json['data']['score_balance'],
                                      res_json['data']['cash_balance'] / 100))


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
    start_path = '/luckycat/lite/v1/sleep/start/?{}'.format(query)
    res = post(host, start_path, headers)
    print('start_sleep' + res)


# 停止睡觉
def end_sleep(headers, query):
    host = 'i-hl.snssdk.com'
    stop_path = '/luckycat/lite/v1/sleep/stop/?{}'.format(query)
    res = post(host, stop_path, headers)
    print('sleep_stop' + res)


# 领取睡觉奖励
def sleep_done_task(headers, query):
    host = 'i-hl.snssdk.com'
    status_path = '/luckycat/lite/v1/sleep/status/?{}'.format(query)
    res = get(host, status_path, headers)
    print('sleep_status' + res)
    res_json = json.loads(res)
    data = res_json['data']
    history_amount = data['history_amount']
    done_task_path = '/luckycat/lite/v1/sleep/done_task/?{}'.format(query)
    res = post(host, done_task_path, headers, json.dumps({"score_amount": history_amount}))
    print('sleep_done_task' + res)


def run_accout_task(type):
    accounts = Account.select()
    for idx, account in enumerate(accounts):
        headers = json.loads(account.headers)
        params = CommonParams.select().where(CommonParams.user_id == account.user_id).dicts().get()
        query = urlencode(params)
        if type == 'sign_in':
            sign_in(headers, query)
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
            profit_detail(headers, query, account)
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


new_excitation_ad_task_ids = ["188", "308" , "216"]


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
                try:
                    res = request(host, method, path, json.loads(headers), '{"task_id":"' + taskId + '"}')
                    print('{} - {} - {} {}'.format(task['name'], task_type, session_key, res))
                except Exception as e:
                    print('{} - {} - {}执行失败'.format(task['name'], task_type, session_key))
        else:
            try:
                res = request(host, method, path, json.loads(headers), body)
                print('{} - {} - {} {}'.format(task['name'], task_type, session_key, res))
            except Exception as e:
                print('{} - {} - {}执行失败'.format(task['name'], task_type, session_key))


parser = argparse.ArgumentParser(description='')
parser.add_argument('--ltype', '-lt', help='主任务类型，必要参数', default=0)
parser.add_argument('--type', '-t', help='任务类型，必要参数', required=True)
args = parser.parse_args()

if __name__ == '__main__':
    ltype = args.ltype
    type = args.type
    if ltype == '1':
        run_task(type)
    else:
        run_accout_task(type)
