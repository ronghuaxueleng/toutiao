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
from liblibart.Image import Image
from liblibart.ql import ql_env

scheduler = BlockingScheduler()


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

    def downLoadImage(self):
        users = get_users()
        for user in users:
            job_id = user['usertoken'] + 'downLoadImage'
            if scheduler.get_job(job_id) is None:
                try:
                    DownLoadImage(user['usertoken'], user['webid']).download()
                except Exception as e:
                    print(e)
                scheduler.add_job(
                    self.downLoadImage,
                    id=job_id,
                    trigger='date',
                    run_date=datetime.datetime.now() + datetime.timedelta(hours=3,
                                                                          minutes=random.sample([11, 23, 37, 42, 57],
                                                                                                1),
                                                                          seconds=random.randint(0, 59)),
                )

    def drawImage(self):
        users = get_users()
        for user in users:
            job_id = user['usertoken'] + 'drawImage'
            if scheduler.get_job(job_id) is None:
                try:
                    Image(user['usertoken'], user['webid']).gen_image()
                except Exception as e:
                    print(e)
                scheduler.add_job(
                    self.downLoadImage,
                    id=job_id,
                    trigger='date',
                    run_date=datetime.datetime.now() + datetime.timedelta(hours=3,
                                                                          minutes=random.sample([11, 23, 37, 42, 57],
                                                                                                1),
                                                                          seconds=random.randint(0, 59)),
                )


liblibTasks = LiblibTasks()
