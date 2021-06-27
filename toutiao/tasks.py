import datetime
import json
import time
from urllib.parse import urlencode

from apscheduler.schedulers.blocking import BlockingScheduler
from peewee import JOIN

from logger import logger
from toutiao.db import Task as DbTask, Account, CommonParams
from toutiao.utils import request, get, post, send_message

scheduler = BlockingScheduler()


class UserTasks:
    def __init__(self):
        self.books = set()
        self.groups = set()
        self.can_read = dict()

    def init(self):
        query = (DbTask.select(DbTask, Account).join(Account, JOIN.LEFT_OUTER,
                                                     on=(DbTask.session_key == Account.session_key)).dicts())
        for idx, task in enumerate(query):
            self.addJob(task)

        accounts = Account.select()
        for idx, account in enumerate(accounts):
            headers = json.loads(account.headers)
            params = CommonParams.select().where(CommonParams.user_id == account.user_id).dicts().get()
            query = urlencode(params)
            self.sign_in(headers, query)
            self.open_notice(headers, query)
            self.newbie_consume(headers, query)
            self.double_whole_scene_task(headers, query)
            self.get_read(headers, query, account)
            self.get_push_read_bonus(headers, query, account)
            self.walk_count(headers, query)
            # self.sleep(headers, query)

        return self

    def start(self):
        scheduler.start()

    def addJob(self, task):
        session_key = task['session_key']
        task_type = task['type']
        scheduler.add_job(
            self.do_task,
            id=session_key + task_type,
            args=(task,),
            trigger='date',
            run_date=datetime.datetime.now(),
        )

    def do_task(self, task):
        session_key = task['session_key']
        task_type = task['type']
        host = task['host']
        path = task['path']
        method = task['method']
        headers = task['header']
        body = task['body']
        try:
            res = request(host, method, path, json.loads(headers), body)
            logger.info('{} - {} - {} {}'.format(task['name'], task_type, session_key, res))
            res_json = json.loads(res)
        except Exception as e:
            logger.info('{} - {} - {}执行失败'.format(task['name'], task_type, session_key))
            send_message('{} - {} 执行失败'.format(task['name'], task_type))
            res_json = None

        task = DbTask.select(DbTask, Account).join(Account, JOIN.LEFT_OUTER,
                                                   on=(DbTask.session_key == Account.session_key)) \
            .where(DbTask.session_key == session_key, DbTask.type == task_type).dicts().get()
        if task_type == 'done_whole_scene_task':
            seconds = 30
            try:
                if res_json is not None and res_json['err_no'] == 0:
                    next_circle_time = res_json['data']['next_circle_time']
                    seconds = next_circle_time
            except Exception as e:
                logger.exception(e)
                logger.error(task['name'] + '执行读文章任务失败: ')
            scheduler.add_job(
                self.do_task,
                id=session_key + task_type,
                args=(task,),
                trigger='date',
                run_date=datetime.datetime.now() + datetime.timedelta(seconds=seconds)
            )
        elif task_type == 'new_excitation_ad':
            scheduler.add_job(
                self.do_task,
                id=session_key + task_type,
                args=(task,),
                trigger='date',
                run_date=datetime.datetime.now() + datetime.timedelta(minutes=8)
            )
        elif task_type == 'open_treasure_box':
            scheduler.add_job(
                self.do_task,
                id=session_key + task_type,
                args=(task,),
                trigger='date',
                run_date=datetime.datetime.now() + datetime.timedelta(minutes=10)
            )

    # 签到
    def sign_in(self, headers, query):
        def do_sign_in():
            sign_in_host = 'i-hl.snssdk.com'
            sign_in_path = '/luckycat/lite/v1/sign_in/action?{}'
            path = sign_in_path.format(query)
            res = post(sign_in_host, path, headers, b'{"rit": "coin", "use_ecpm": "0"}')
            logger.info('sign_in ' + res)

        scheduler.add_job(
            do_sign_in,
            trigger='cron',
            hour='3'
        )

    # 打开通知
    def open_notice(self, headers, query):
        def do_open():
            host = 'api3-normal-c-hl.snssdk.com'
            path = '/luckycat/lite/v1/task/done_apply_permission?{}'.format(query)
            headers['content-type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
            data = 'body=null'
            res = post(host, path, headers, data)
            logger.info('open_notice ' + res)

        scheduler.add_job(
            do_open,
            trigger='cron',
            hour='3'
        )

    # 新人阅读
    def newbie_consume(self, headers, query):
        def do_read():
            host = 'api3-normal-c-hl.snssdk.com'
            path = '/score_task/lite/v1/newbie_consume/done_consume/?{}'.format(query)
            headers['content-type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
            res = post(host, path, headers, query)
            logger.info('newbie_consume' + res)

        scheduler.add_job(
            do_read,
            trigger='cron',
            hour='3'
        )

    # 点击翻倍
    def double_whole_scene_task(self, headers, query):
        def do_run():
            host = 'i-hl.snssdk.com'
            path = '/luckycat/lite/v1/activity/double_whole_scene_task/?{}'.format(query)
            res = post(host, path, headers)
            logger.info('double_whole_scene_task' + res)

        scheduler.add_job(
            do_run,
            trigger='cron',
            minute='30',
            hour='0'
        )

    # 阅读推送文章
    def get_push_read_bonus(self, headers, query, account):
        scheduler.add_job(
            self.get_read_bonus,
            trigger='cron',
            args=(headers, query, account,),
            minute='30',
            hour='2,4,6,8,14'
        )

    # 阅读
    def get_read(self, headers, query, account):
        scheduler.add_job(
            self.get_read_bonus,
            trigger='cron',
            args=(headers, query, account, False, ),
            hour='2,4,6,8,14'
        )

    # 阅读
    def get_read_bonus(self, headers, query, account, is_push=True):
        try:
            # 文章列表
            feed_host = 'iu.snssdk.com'
            feed_path = '/api/news/feed/v64/?{}'.format(query)
            res = post(feed_host, feed_path, headers)
            res_json = json.loads(res)
            for item in res_json['data']:
                d = json.loads(item['content'])
                group_id = d.get('group_id')
                self.groups.add(group_id)
                if group_id is not None:
                    push = 'push' if is_push else ''
                    read_bonus_host = 'is.snssdk.com'
                    read_bonus_path = '/score_task/v1/task/get_read_bonus/?group_id={}&impression_type={}&{}'
                    path = read_bonus_path.format(group_id, push, query)
                    res = get(read_bonus_host, path, headers)
                    logger.info(account.name + '：get_read_bonus ' + res)
                    time.sleep(10)
        except Exception:
            pass

    # 走路赚金币
    def walk_count(self, headers, query):
        def do_run():
            host = 'i-hl.snssdk.com'
            path = '/luckycat/lite/v1/walk/count/?{}'.format(query)
            data = {"count": 20000, "client_time": int(time.time())}
            post(host, path, headers, json.dumps(data))
            bonus_path = '/luckycat/lite/v1/walk/bonus/?{}'.format(query)
            data = {"task_id": 136, "client_time": int(time.time()), "rit": "coin", "use_ecpm": 0}
            res = post(host, bonus_path, headers, json.dumps(data))
            logger.info('walk_count' + res)

        scheduler.add_job(
            do_run,
            trigger='cron',
            hour='12'
        )

    # 睡觉
    def sleep(self, headers, query):
        def do_run():
            try:
                host = 'i-hl.snssdk.com'
                status_path = '/luckycat/lite/v1/sleep/status/?{}'.format(query)
                res = get(host, status_path, headers)
                logger.info('sleep_status' + res)
                res_json = json.loads(res)
                data = res_json['data']
                sleeping = data['sleeping']
                history_amount = data['history_amount']
                if history_amount > 0:
                    done_task_path = '/luckycat/lite/v1/sleep/done_task/?{}'.format(query)
                    res = post(host, done_task_path, headers, json.dumps({"score_amount": history_amount}))
                    logger.info('sleep_done_task' + res)

                if sleeping:
                    stop_path = '/luckycat/lite/v1/sleep/stop/?{}'.format(query)
                    res = post(host, stop_path, headers)
                    logger.info('sleep_stop' + res)
                elif not sleeping:
                    start_path = '/luckycat/lite/v1/sleep/start/?{}'.format(query)
                    res = post(host, start_path, headers)
                    logger.info('sleep_start' + res)
            except Exception:
                pass

            scheduler.add_job(
                do_run,
                trigger='date',
                run_date=datetime.datetime.now() + datetime.timedelta(minutes=30)
            )

        scheduler.add_job(
            do_run,
            trigger='date'
        )

    # 查询现金收益
    def cash_balance(self, headers, query, account):
        def do_run():
            host = 'i-hl.snssdk.com'
            path = '/luckycat/lite/v1/user/profit_detail/?offset=6922228539857356812&num=300&income_type=1&{}'.format(
                query)
            res = get(host, path, headers)
            res_json = json.loads(res)
            send_message(account.name + '：现金收益' + str(res_json['data']['cash_balance'] / 100))

        scheduler.add_job(
            do_run,
            trigger='cron',
            hour='6'
        )


userTasks = UserTasks()
