import copy
import datetime
import json
import random

from apscheduler.schedulers.background import BackgroundScheduler

from liblibart.CookieUtils import get_users
from liblibart.DownLoadImage import DownLoadImage
from liblibart.DownloadModel import DownloadModel
from liblibart.Image import Image
from liblibart.UserInfo import UserInfo
from liblibart.ql import ql_env

scheduler = BackgroundScheduler()


class LiblibTasks:
    def __init__(self):
        pass

    def init(self):
        self.drawImage()
        self.downloadModel()
        self.downLoadImage()
        return self

    def start(self):
        scheduler.start()

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

    def downloadModel(self):
        def doDownloadModel(user):
            try:
                DownloadModel(user['usertoken'], user['webid']).download_model(pageNo, download_models)
            except Exception as e:
                print(e)

        my_loras = ql_env.search("my_lora")
        download_models = []
        for my_lora in my_loras:
            if my_lora['status'] == 0:
                download_models.append(json.loads(my_lora['value'])['modelId'])
        for pageNo in range(1, 5):
            users = get_users()
            for user in random.sample(users, 4):
                job_id = f"{user['usertoken']}_downloadModel_{pageNo}"
                if scheduler.get_job(job_id) is None:
                    scheduler.add_job(
                        doDownloadModel,
                        id=job_id,
                        trigger='date',
                        args=[user],
                        run_date=datetime.datetime.now() + datetime.timedelta(hours=4, minutes=random.randint(0, 59),
                                                                              seconds=random.randint(0, 59)),
                    )

    def downLoadImage(self):
        def doDownloadImage(user):
            try:
                DownLoadImage(user['usertoken'], user['webid']).download()
            except Exception as e:
                print(e)

        users = get_users()
        for user in users:
            job_id = f"{user['usertoken']}_downLoadImage"
            if scheduler.get_job(job_id) is None:
                scheduler.add_job(
                    doDownloadImage,
                    id=job_id,
                    trigger='date',
                    args=[user],
                    run_date=datetime.datetime.now() + datetime.timedelta(hours=3,
                                                                          minutes=random.sample([11, 23, 37, 42, 57],
                                                                                                1)[0],
                                                                          seconds=random.randint(0, 59)),
                )

    def drawImage(self):
        def doDrawImage(user, model):
            try:
                image = Image(user['usertoken'], user['webid'])
                del model['userUuid']
                del model['modelType']
                image.param['additionalNetwork'].append(model)
                runCount = {}
                run_model = runCount.setdefault(user['usertoken'], {})
                __model = run_model.setdefault(model['modelId'], model)
                run_count = __model.setdefault('count', 0)
                image.gen(run_count)
            except Exception as e:
                print(e)

        users = get_users()
        user_model_dict = self.get_models()
        for user in users:
            to_run_models = user_model_dict[user['usertoken']]
            for to_run_model in to_run_models:
                job_id = f"{user['usertoken']}_{to_run_model['modelId']}_drawImage"
                if scheduler.get_job(job_id) is None:
                    scheduler.add_job(
                        doDrawImage,
                        id=job_id,
                        trigger='date',
                        args=[user, to_run_model],
                        run_date=datetime.datetime.now() + datetime.timedelta(minutes=random.randint(5, 20),
                                                                              seconds=random.randint(0, 59)),
                    )


liblibTasks = LiblibTasks()

if __name__ == '__main__':
    models = liblibTasks.drawImage()
    print(models)
