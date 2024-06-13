import copy
import datetime
import json
import queue
import random
import time
import types

from apscheduler.schedulers.blocking import BlockingScheduler

from liblibart.CookieUtils import get_users
from liblibart.DownLoadImage import DownLoadImage
from liblibart.DownloadModel import DownloadModel
from liblibart.Image import Image
from liblibart.ql import ql_env

scheduler = BlockingScheduler()


class LiblibTasks:
    def __init__(self):
        pass

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
        return self

    def init(self):
        self.drawImage()
        self.downloadModel()
        self.downLoadImage()
        return self

    def start(self):
        scheduler.start()
        return self

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
        datetime.datetime.now() + datetime.timedelta(days=random.randint(5, 7), hours=4,
                                                     minutes=random.randint(0, 59),
                                                     seconds=random.randint(0, 59))

    def get_downLoad_image_run_date(self):
        datetime.datetime.now() + datetime.timedelta(hours=random.randint(3, 5),
                                                     minutes=random.sample([11, 23, 37, 42, 57],
                                                                           1)[0],
                                                     seconds=random.randint(0, 59))

    def get_draw_image_run_date(self):
        return datetime.datetime.now() + datetime.timedelta(hours=random.randint(3, 5),
                                                            minutes=random.randint(5, 20),
                                                            seconds=random.randint(0, 59))

    def downloadModel(self):
        job_id = 'downloadModel'

        my_loras = ql_env.search("my_lora")
        download_models = []
        for my_lora in my_loras:
            if my_lora['status'] == 0:
                download_models.append(json.loads(my_lora['value'])['modelId'])
        for pageNo in range(1, 5):
            users = get_users()
            for user in users:
                try:
                    DownloadModel(user['usertoken'], user['webid']).download_model(pageNo, download_models)
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

    def downLoadImage(self):
        job_id = "downLoadImage"

        users = get_users()
        for user in users:
            try:
                DownLoadImage(user['usertoken'], user['webid']).download()
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

    def drawImage(self):
        q = queue.Queue()
        job_id = f"drawImage"

        def f_percent_wapper(generator, image, image_num):
            gen = generator(image, image_num)
            while isinstance(gen, types.GeneratorType):
                gen = gen.__next__()

            return gen

        def get_percent(image, image_num):
            res = image.get_percent(image_num)
            if res['code'] == 0:
                percentCompleted = res['data']['percentCompleted']
                image.logger.info(f"mobile：{image.userInfo['mobile']}，{percentCompleted}%.....")
                if percentCompleted != 100:
                    time.sleep(7)
                    yield get_percent(image, image_num)
                else:
                    image.logger.info(f"mobile：{image.userInfo['mobile']}，100%.....")
                    image.nps()
                    try:
                        DownLoadImage(user['usertoken'], user['webid']).download()
                    except Exception as e:
                        print(e)
                    if q.not_empty:
                        r = q.get()
                        doDrawImage(r[0], r[1])
                    else:
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

        def doDrawImage(user, model):
            try:
                userUuid = model['userUuid']
                image = Image(user['usertoken'], user['webid'])
                del model['userUuid']
                del model['modelType']
                image.param['additionalNetwork'].append(model)
                runCount = {}
                run_model = runCount.setdefault(userUuid, {})
                __model = run_model.setdefault(model['modelId'], model)
                run_count = __model.setdefault('count', 0)
                runCount[userUuid][model['modelId']]['count'] = run_count + 1
                image_num = image.gen(runCount)
                if image_num != 'suanlibuzu':
                    f_percent_wapper(get_percent, image, image_num)
                else:
                    if q.not_empty:
                        r = q.get()
                        doDrawImage(r[0], r[1])
                    else:
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
            except Exception as e:
                print(e)

        users = get_users()
        user_model_dict = self.get_models()
        for user in users:
            to_run_models = user_model_dict[user['usertoken']]
            for to_run_model in to_run_models:
                q.put((user, to_run_model))
        r = q.get()
        doDrawImage(r[0], r[1])


liblibTasks = LiblibTasks()

if __name__ == '__main__':
    liblibTasks.drawImage()
    all_jobs = scheduler.get_jobs()
    print(all_jobs)
