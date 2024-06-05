import datetime
import json
import random
import time
from urllib.parse import urlencode

from apscheduler.schedulers.blocking import BlockingScheduler
from peewee import JOIN

from liblibart.CookieUtils import get_users
from liblibart.DownLoadImage import DownLoadImage
from liblibart.DownloadModel import DownloadModel
from liblibart.ql import ql_env

scheduler = BlockingScheduler()


class LiblibTasks:
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

    def downloadModel(self):
        my_loras = ql_env.search("my_lora")
        download_models = []
        for my_lora in my_loras:
            if my_lora['status'] == 0:
                download_models.append(json.loads(my_lora['value'])['modelId'])
        for pageNo in range(1, 5):
            users = get_users()
            for user in random.sample(users, 4):
                job_id = user['usertoken'] + 'downloadModel' + pageNo
                if scheduler.get_job(job_id) is None:
                    try:
                        DownloadModel(user['usertoken'], user['webid']).download_model(pageNo, download_models)
                    except Exception as e:
                        print(e)
                    scheduler.add_job(
                        self.downloadModel,
                        id=job_id,
                        trigger='date',
                        run_date=datetime.datetime.now() + datetime.timedelta(hours=4, minutes=random.randint(0, 59),
                                                                              seconds=random.randint(0, 59)),
                    )

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


liblibTasks = LiblibTasks()
