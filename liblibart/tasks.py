import copy
import datetime
import json
import os
import random
import time

from apscheduler.schedulers.blocking import BlockingScheduler

from liblibart.CookieUtils import get_users
from liblibart.DownLoadImage import DownLoadImage
from liblibart.DownloadModel import DownloadModel
from liblibart.Image import Image
from liblibart.ql import ql_env
from utils.utils import send_message

scheduler = BlockingScheduler()


class LiblibTasks:
    def __init__(self):
        dt = datetime.datetime.now()
        self.yesterday = (dt - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        self.today = dt.strftime('%Y-%m-%d')
        self.notAvailableToImageUsers = {}
        self.notAvailableImageUsersFileName = 'notAvailableToImageUsers.json'

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
        send_message("\n".join(msg), title='哩布哩布')

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

    def get_download_model_run_date(self):
        return datetime.datetime.now() + datetime.timedelta(days=random.randint(3, 5), hours=random.randint(1, 23),
                                                     minutes=random.randint(0, 59),
                                                     seconds=random.randint(0, 59))

    def get_downLoad_image_run_date(self):
        return datetime.datetime.now() + datetime.timedelta(hours=random.randint(3, 5),
                                                     minutes=random.sample([11, 23, 37, 42, 57],
                                                                           1)[0],
                                                     seconds=random.randint(0, 59))

    def get_draw_image_run_date(self):
        return datetime.datetime.now() + datetime.timedelta(minutes=random.randint(20, 40),
                                                            seconds=random.randint(0, 59))

    def downloadModel(self):
        send_message("开始执行模型下载", title='哩布哩布')
        job_id = 'downloadModel'

        my_loras = ql_env.search("my_lora")
        download_models = []
        for my_lora in my_loras:
            if my_lora['status'] == 0:
                download_models.append(json.loads(my_lora['value'])['modelId'])
        for pageNo in range(1, 5):
            users = get_users()
            for user in random.sample(users, 4):
                try:
                    DownloadModel(user['usertoken'], user['webid'], '/mitmproxy/logs/DownloadModel.log').download_model(
                        pageNo, download_models)
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
        send_message("开始执行图片下载", title='哩布哩布')
        job_id = "downLoadImage"

        users = get_users()
        for user in users:
            try:
                DownLoadImage(user['usertoken'], user['webid'], '/mitmproxy/logs/DownLoadImage.log').download()
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
        send_message("开始执行绘图", title='哩布哩布')
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
                image.getLogger().info(f"mobile：{image.userInfo['mobile']}，{percentCompleted}%.....")
                if percentCompleted != 100:
                    time.sleep(7)
                    get_percent(user, image, image_num, depth + 1)
                else:
                    image.getLogger().info(f"finished mobile：{image.userInfo['mobile']}，100%.....")
                    image.nps()
                    try:
                        DownLoadImage(user['usertoken'], user['webid'], '/mitmproxy/logs/DownLoadImage.log').download()
                    except Exception as e:
                        print(e)
                    image.getLogger().info(f'递归层级{depth}')
                    return depth

        def doDrawImage(user, my_loras):
            try:
                if user['usertoken'] not in suanlibuzu:
                    image = Image(user['usertoken'], user['webid'], '/mitmproxy/logs/Image.log')
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
                    else:
                        get_percent(user, image, image_num, 1)
            except Exception as e:
                print(e)

        users = get_users(exclude_user=self.notAvailableToImageUsers.setdefault(self.today, []))
        user_model_dict = self.get_models()

        def simple_generator():
            # for user in random.sample(users, 5):
            for user in users:
                to_run_models = user_model_dict[user['usertoken']]
                # to_run_models = random.sample(to_run_models, 20) if len(to_run_models) > 20 else to_run_models
                group_every_two = [to_run_models[i:i + 2] for i in range(0, len(to_run_models), 2)]
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
            self.get_all_job('绘图结束')
            with open(f'/mitmproxy/{self.notAvailableImageUsersFileName}', 'w') as f:
                json.dump(self.notAvailableToImageUsers, f)


liblibTasks = LiblibTasks()

if __name__ == '__main__':
    liblibTasks.drawImage()
