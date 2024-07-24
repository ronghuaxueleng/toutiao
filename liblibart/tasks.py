import copy
import datetime
import json
import os
import random
import time
from pathlib import Path

from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.blocking import BlockingScheduler

from CookieUtils import get_users, load_from_run_users, save_to_run_users
from DownLoadImage import DownLoadImage
from DownloadModel import DownloadModel
from Image import Image
from UserInfo import UserInfo, Account
from ql import ql_env
from utils import send_message

dbpath = Path(os.path.split(os.path.realpath(__file__))[0]).parent.joinpath('config', 'jobs.db').absolute()
interval_task = {
    # 配置存储器
    "jobstores": {
        # 使用SQLAlchemy进行存储,会自动创建数据库，并创建apscheduler_jobs表
        'default': SQLAlchemyJobStore(url=fr"sqlite:///{dbpath}")
    },
    # 配置执行器
    "executors": {
        # 使用线程池进行执行，最大线程数是20个
        'default': ThreadPoolExecutor(20)
    },
    # 创建job时的默认参数
    "job_defaults": {
        'coalesce': False,  # 是否合并执行
        'max_instances': 3  # 最大实例数
    }

}

scheduler = BlockingScheduler(interval_task)

from dotenv import load_dotenv, find_dotenv
from pathlib import Path

# 指定env文件
env_path = Path.cwd().joinpath('env').joinpath('os.env')
print(env_path)
env_path.parent.mkdir(exist_ok=True)
load_dotenv(find_dotenv(str(env_path)))


class LiblibTasks:
    def __init__(self):
        self.yesterday = 0
        self.today = 0
        self.notAvailableToImageUsers = {}
        self.notAvailableImageUsersFileName = 'notAvailableToImageUsers.json'

    def init_day(self):
        dt = datetime.datetime.now()
        self.yesterday = (dt - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        self.today = dt.strftime('%Y-%m-%d')

    def init_tasks(self):
        scheduler.add_job(
            self.downloadModel,
            id='downloadModel',
            trigger='date',
            run_date=self.get_download_model_run_date(),
        )

        scheduler.add_job(
            self.downLoadImage,
            id='downLoadImage',
            trigger='date',
            run_date=self.get_downLoad_image_run_date(),
        )

        scheduler.add_job(
            self.drawImage,
            id='drawImage',
            trigger='date',
            run_date=self.get_draw_image_run_date(),
        )
        self.get_all_job()
        return self

    def init(self):
        self.drawImage()
        self.downloadModel()
        self.downLoadImage()
        return self

    def start(self):
        scheduler.start()
        return self

    def get_all_job(self, message=None):
        all_jobs = scheduler.get_jobs()
        print(all_jobs)
        msg = []
        if message is not None:
            msg.append(message)
        for job in all_jobs:
            msg.append(f'任务ID：{job.id}，执行时间：{job.trigger}')
        send_message("\n".join(msg), title=f'哩布哩布-{os.getenv("RUN_OS_NAME")}')

    def get_models(self):
        user_model_dict = {}
        my_loras = ql_env.search("my_lora")
        for my_lora in my_loras:
            if my_lora['status'] == 0:
                value = json.loads(my_lora['value'])
                user_models = user_model_dict.setdefault(value['userUuid'], [])
                user_models.append(value)
                user_model_dict[value['userUuid']] = user_models

        final_user_model_dict = {}
        users = get_users()
        for user in users:
            _user_model_dict = copy.deepcopy(user_model_dict)
            usertoken = user['usertoken']
            if usertoken in _user_model_dict:
                del _user_model_dict[usertoken]
            final_user_model_list = final_user_model_dict.setdefault(usertoken, [])
            for user_model in _user_model_dict.values():
                final_user_model_list.extend(user_model)
            final_user_model_dict[usertoken] = final_user_model_list
        return final_user_model_dict

    def update_userInfo(self):
        users = get_users(True)
        disable_ids = []
        enable_ids = []
        for user in users:
            try:
                userInfo = UserInfo(user['usertoken'], user['webid'],
                                    f'/mitmproxy/logs/UserInfo_{os.getenv("RUN_OS_KEY")}.log')
                realUser = userInfo.userInfo
                if realUser is not None:
                    enable_ids.append(user['id'])
                    uuid = realUser['uuid']
                    nickname = realUser['nickname']
                    query = Account.select().where(Account.user_uuid == uuid)
                    if query.exists():
                        Account.update(
                            user_uuid=uuid,
                            nickname=nickname,
                            userInfo=json.dumps(realUser)
                        ).where(Account.user_uuid == uuid).execute()
                    else:
                        Account.insert(
                            user_uuid=uuid,
                            nickname=nickname,
                            userInfo=json.dumps(realUser)
                        ).execute()
                else:
                    disable_ids.append(user['id'])
            except Exception as e:
                print(e)
        if len(disable_ids) > 0:
            ql_env.disable(disable_ids)
        if len(enable_ids) > 0:
            ql_env.enable(enable_ids)

    def get_download_model_run_date(self):
        return datetime.datetime.now() + datetime.timedelta(days=random.randint(1, 3), hours=random.randint(1, 23),
                                                            minutes=random.randint(0, 59),
                                                            seconds=random.randint(0, 59))

    def get_downLoad_image_run_date(self):
        return datetime.datetime.now() + datetime.timedelta(hours=random.randint(3, 5),
                                                            minutes=random.sample([11, 23, 37, 42, 57],
                                                                                  1)[0],
                                                            seconds=random.randint(0, 59))

    def get_draw_image_run_date(self):
        return datetime.datetime.now() + datetime.timedelta(minutes=random.randint(2, 7),
                                                            seconds=random.randint(0, 59))

    def downloadModel(self):
        send_message("开始执行模型下载", title=f'哩布哩布-{os.getenv("RUN_OS_NAME")}')
        job_id = 'downloadModel'
        users = get_users()
        for user in random.sample(users, 4):
            try:
                DownloadModel(user['usertoken'], user['webid'],
                              f'/mitmproxy/logs/DownloadModel_{os.getenv("RUN_OS_KEY")}.log').download_model()
            except Exception as e:
                print(e)
        s = scheduler.get_job(job_id)
        if s is None:
            scheduler.add_job(
                self.downloadModel,
                id=job_id,
                trigger='date',
                run_date=self.get_download_model_run_date(),
            )
        else:
            scheduler.reschedule_job(
                job_id,
                run_date=self.get_download_model_run_date()
            )
        self.get_all_job('模型下载结束')

    def downLoadImage(self):
        send_message("开始执行图片下载", title=f'哩布哩布-{os.getenv("RUN_OS_NAME")}')
        job_id = "downLoadImage"

        users = get_users()
        for user in users:
            try:
                DownLoadImage(user['usertoken'], user['webid'],
                              f'/mitmproxy/logs/DownLoadImage_{os.getenv("RUN_OS_KEY")}.log').download()
            except Exception as e:
                print(e)
        s = scheduler.get_job(job_id)
        if s is None:
            if scheduler.get_job(job_id) is None:
                scheduler.add_job(
                    self.downLoadImage,
                    id=job_id,
                    trigger='date',
                    run_date=self.get_downLoad_image_run_date(),
                )
        else:
            scheduler.reschedule_job(
                job_id,
                run_date=self.get_downLoad_image_run_date(),
            )
        self.get_all_job('图片下载结束')

    def drawImage(self):
        self.init_day()
        star_time = datetime.datetime.now()
        send_message("开始执行绘图", title=f'哩布哩布-{os.getenv("RUN_OS_NAME")}')
        job_id = f"drawImage"
        suanlibuzu = []
        if os.path.exists(f'/mitmproxy/{self.notAvailableImageUsersFileName}'):
            with open(f'/mitmproxy/{self.notAvailableImageUsersFileName}', 'r') as f:
                self.notAvailableToImageUsers = json.load(f)
        if self.yesterday in self.notAvailableToImageUsers:
            del self.notAvailableToImageUsers[self.yesterday]
            with open(f'/mitmproxy/{self.notAvailableImageUsersFileName}', 'w') as f:
                json.dump(self.notAvailableToImageUsers, f)

        def get_percent(user, image, image_num, depth):
            res = image.get_percent(image_num)
            if res['code'] == 0:
                percentCompleted = res['data']['percentCompleted']
                image.getLogger().info(f"nickname：{image.userInfo['nickname']}，{percentCompleted}%.....")
                if percentCompleted != 100:
                    time.sleep(7)
                    get_percent(user, image, image_num, depth + 1)
                else:
                    image.getLogger().info(f"finished nickname：{image.userInfo['nickname']}，100%.....")
                    image.nps()
                    try:
                        DownLoadImage(user['usertoken'], user['webid'],
                                      f'/mitmproxy/logs/DownLoadImage_{os.getenv("RUN_OS_KEY")}.log').download(
                            False)
                    except Exception as e:
                        print(e)
                    image.getLogger().info(f'递归层级{depth}')
                    return depth

        def doDrawImage(user, my_loras):
            try:
                to_save_run_users = load_from_run_users()
                if user['usertoken'] in to_save_run_users:
                    to_save_run_users.remove(user['usertoken'])
                    save_to_run_users(list(set(to_save_run_users)))
                if user['usertoken'] not in suanlibuzu:
                    image = Image(user['usertoken'], user['webid'],
                                  f'/mitmproxy/logs/Image_{os.getenv("RUN_OS_KEY")}.log')
                    runCount = {}
                    for model in my_loras:
                        userUuid = model['userUuid']
                        del model['userUuid']
                        del model['modelType']
                        image.param['additionalNetwork'].append(model)
                        run_model = runCount.setdefault(userUuid, {})
                        __model = run_model.setdefault(model['modelId'], model)
                        run_count = __model.setdefault('count', 0)
                        runCount[userUuid][model['modelId']]['count'] = run_count + 1
                    image_num = image.gen(runCount)
                    if image_num == 'suanlibuzu':
                        suanlibuzu.append(user['usertoken'])
                        notAvailableToImageUsers = self.notAvailableToImageUsers.setdefault(self.today, [])
                        notAvailableToImageUsers.append(user['usertoken'])
                        self.notAvailableToImageUsers[self.today] = notAvailableToImageUsers
                        raise Exception('算力不足')
                    elif image_num == 'qitacuowu':
                        raise Exception('报错了')
                    elif image_num == 'tokenwuxiao':
                        image.getLogger().error('token无效')
                        self.update_userInfo()
                        raise Exception('token无效')
                    else:
                        get_percent(user, image, image_num, 1)
            except Exception as e:
                print(e)

        exclude_user = self.notAvailableToImageUsers.setdefault(self.today, [])
        to_run_users = load_from_run_users()
        exclude_user.extend(to_run_users)
        users = get_users(exclude_user=exclude_user)
        if len(users) == 0:
            self.notAvailableToImageUsers[self.today] = []
        user_model_dict = self.get_models()

        def simple_generator():
            # 当前时间
            now_localtime = time.strftime("%H:%M:%S", time.localtime())
            is_time = "00:00:00" < now_localtime < "08:00:00"
            to_run_user_count = (10 if len(users) >= 10 else len(users)) if is_time else (
                5 if len(users) >= 5 else len(users))
            to_save_run_users = load_from_run_users()
            to_run_users = random.sample(users, to_run_user_count)
            for user in to_run_users:
                to_save_run_users.append(user['usertoken'])
            save_to_run_users(list(set(to_save_run_users)))
            for user in to_run_users:
                # for user in users:
                to_run_models = user_model_dict[user['usertoken']]
                to_run_model_count = (30 if len(to_run_models) >= 30 else len(to_run_models)) if is_time else (
                    20 if len(to_run_models) >= 20 else len(to_run_models))
                to_run_models = random.sample(to_run_models, to_run_model_count)
                group_every_two = [to_run_models[i:i + 1] for i in range(0, len(to_run_models), 1)]
                for to_run_model in group_every_two:
                    yield doDrawImage(user, to_run_model)

        gen = simple_generator()
        try:
            while True:
                next(gen)
        except StopIteration as e:
            print(e.value)
        finally:
            gen.close()
            s = scheduler.get_job(job_id)
            if s is None:
                scheduler.add_job(
                    self.drawImage,
                    id=job_id,
                    trigger='date',
                    run_date=self.get_draw_image_run_date(),
                )
            else:
                scheduler.reschedule_job(
                    job_id,
                    run_date=self.get_draw_image_run_date(),
                )
            with open(f'/mitmproxy/{self.notAvailableImageUsersFileName}', 'w') as f:
                json.dump(self.notAvailableToImageUsers, f)
            end_time = datetime.datetime.now()
            time_consuming = (end_time - star_time).seconds / 60
            self.get_all_job(f'绘图结束\n耗时{time_consuming}分')


liblibTasks = LiblibTasks()

if __name__ == '__main__':
    liblibTasks.drawImage()
    # liblibTasks.init_tasks()
