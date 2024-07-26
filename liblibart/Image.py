# -*- coding: utf-8 -*-
import copy
import datetime
import json
import os
import random
import threading
import time
import uuid

import requests

from liblibart.Base import Base
from liblibart.CookieUtils import get_users, load_from_suanlibuzu_users, save_to_suanlibuzu_users
from liblibart.DownLoadImage import DownLoadImage
from liblibart.Statistics import RunStatistics

from dotenv import load_dotenv, find_dotenv
from pathlib import Path

# 指定env文件
env_path = Path.cwd().joinpath('env').joinpath('os.env')
env_path.parent.mkdir(exist_ok=True)
load_dotenv(find_dotenv(str(env_path)))


class Image(Base):
    _instance_lock = threading.Lock()

    def __init__(self, token, webid, log_filename):
        super().__init__(token, webid, log_filename)
        self.frontId = str(uuid.uuid1())
        self.param = copy.deepcopy(self.gen_param)
        self.param['frontCustomerReq']['frontId'] = self.frontId

    def __new__(cls, *args, **kwargs):
        if not hasattr(Image, "_instance"):
            with Image._instance_lock:
                if not hasattr(Image, "_instance"):
                    Image._instance = object.__new__(cls)
        return Image._instance

    def gen_image(self):
        runCount = {}
        for userUuid, models in self.user_model_dict.items():
            if len(models) >= 6:
                my_loras = random.sample(models, 6)
            else:
                my_loras = models
            for value in my_loras:
                if userUuid != self.uuid:
                    modelId = value['modelId']
                    userUuid = value['userUuid']
                    run_model = runCount.setdefault(userUuid, {})
                    __model = run_model.setdefault(modelId, value)
                    run_count = __model.setdefault('count', 0)
                    runCount[userUuid][modelId]['count'] = run_count + 1
                    if value['modelType'] == 5:
                        del value['userUuid']
                        del value['modelType']
                        self.param['additionalNetwork'].append(value)

        image_num = self.gen(runCount)
        if image_num != 'suanlibuzu':
            res = self.get_percent(image_num)
            if res['code'] == 0:
                if res['data']['percentCompleted'] != 100:
                    self.get_percent(image_num)
                else:
                    self.nps()
                    try:
                        DownLoadImage(self.token, self.webid, '/mitmproxy/logs/DownLoadImage.log').download()
                    except Exception as e:
                        print(e)
                    return True

    def gen(self, runCount):
        if len(self.param['additionalNetwork']) > 0:
            payload = json.dumps(self.param)
            headers = self.headers
            headers['content-type'] = 'application/json'
            headers['referer'] = f'https://{self.web_host}/v4/editor'
            url = f"https://{self.api_host}/gateway/sd-api/generate/image"
            response = requests.request("POST", url, headers=headers, data=payload)
            res = json.loads(response.text)

            if res['code'] == 0:
                self.getLogger().info(f"nickname：{self.userInfo['nickname']} generate image，{response.text}")
                res1 = self.progress_msg(headers, res['data'])
                url = f"https://{self.api_host}/api/www/log/acceptor/f"
                payload = json.dumps({
                    "abtest": [
                        {
                            "name": "image_recommend",
                            "group": "IMAGE_REC_SERVICE_DEFAULT"
                        },
                        {
                            "name": "model_recommend",
                            "group": "PERSONALIZED_RECOMMEND_V11"
                        }
                    ],
                    "sys": "SD",
                    "t": 2,
                    "uuid": self.userInfo['uuid'],
                    "cid": self.webid,
                    "page": "SD_GENERATE",
                    "pageUrl": f"https://{self.web_host}/v4/editor#/?id=1707050189693&defaultCheck=undefined&type=undefined",
                    "ct": time.time(),
                    "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.160 Safari/537.36",
                    "referer": f"https://{self.web_host}/sd",
                    "e": "sdp.generate.req",
                    "generateId": self.frontId,
                    "var": {
                        "gen-img-req-param": {
                            "checkpointId": 159549,
                            "generateType": 1,
                            "frontCustomerReq": res1['data']['frontCustomerReq'],
                            "text2img": self.param['text2img'],
                            "adetailerEnable": 0,
                            "additionalNetwork": self.param['additionalNetwork'],
                            "taskQueuePriority": 1
                        },
                        "gen-img-type": "txt2img"
                    }
                })
                response = requests.request("POST", url, headers=headers, data=payload)
                self.getLogger().info(f"nickname：{self.userInfo['nickname']} log acceptor，{response.text}")

                for user_uuid, model_list in runCount.items():
                    for modelId, model in model_list.items():
                        query = RunStatistics.select().where(RunStatistics.user_uuid == user_uuid,
                                                             RunStatistics.modelId == modelId,
                                                             RunStatistics.day == self.day)
                        if query.exists():
                            runCount = int(query.dicts().get().get('runCount'))
                            RunStatistics.update(
                                runCount=runCount + model['count'],
                                timestamp=datetime.datetime.now()
                            ).where(RunStatistics.user_uuid == user_uuid, RunStatistics.modelId == modelId,
                                    RunStatistics.day == self.day).execute()
                        else:
                            RunStatistics.insert(
                                user_uuid=user_uuid,
                                modelId=modelId,
                                modelName=model['modelName'],
                                runCount=model['count'],
                                day=self.day
                            ).execute()
                return res['data']
            elif res['code'] == 1200000136 or res['code'] == 1200000170:
                if res['code'] == 1200000136:
                    suanlibuzu_user = load_from_suanlibuzu_users()
                    suanlibuzu_user.append(self.userInfo['uuid'])
                    save_to_suanlibuzu_users(list(set(suanlibuzu_user)))
                return 'suanlibuzu'
            elif res['code'] == 1100000102:
                return 'tokenwuxiao'
            else:
                self.getLogger().error(response.text)
                return 'qitacuowu'

    def get_percent(self, image_num):
        url = f"https://liblib-api.vibrou.com/gateway/sd-api/generate/progress/msg/v1/{image_num}"
        payload = json.dumps({
            "flag": 0
        })
        headers = copy.deepcopy(self.headers)
        del headers['authority']
        headers['content-type'] = 'application/json'
        headers['referer'] = f'https://{self.web_host}'
        response = requests.request("POST", url, headers=headers, data=payload)
        return json.loads(response.text)

    def nps(self):
        url = "https://liblib-api.vibrou.com/gateway/sd-api/common/getStatisticsCount"

        payload = json.dumps({
            "businessType": "nps",
            "source": 0
        })
        headers = copy.deepcopy(self.headers)
        del headers['authority']
        headers['content-type'] = 'application/json'
        headers['referer'] = f'https://{self.web_host}'

        response = requests.request("POST", url, headers=headers, data=payload)
        self.getLogger().info(f"nickname：{self.userInfo['nickname']} getStatisticsCount，{response.text}")

    def progress_msg(self, headers, progress_code):
        url = f"https://{self.api_host}/gateway/sd-api/generate/progress/msg/{progress_code}"

        payload = json.dumps({})
        response = requests.request("POST", url, headers=headers, data=payload)
        return json.loads(response.text)


if __name__ == '__main__':
    users = get_users()
    for user in random.sample(users, 4):
        try:
            Image(user['usertoken'], user['webid'], f'/mitmproxy/logs/Image_{os.getenv("RUN_OS_KEY")}.log').gen_image()
        except Exception as e:
            print(e)
