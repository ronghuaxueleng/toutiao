# -*- coding: utf-8 -*-
import copy
import datetime
import json
import random
import time
import uuid

import requests

from liblibart.Base import Base
from liblibart.CookieUtils import get_users
from liblibart.Statistics import RunStatistics


class Image(Base):
    def __init__(self, token, webid):
        super().__init__(token, webid)
        self.frontId = str(uuid.uuid1())
        self.param = copy.deepcopy(self.gen_param)
        self.param['frontCustomerReq']['frontId'] = self.frontId

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

        self.gen(runCount)

    def gen(self, runCount):
        if len(self.param['additionalNetwork']) > 0:
            payload = json.dumps(self.param)
            headers = self.headers
            headers['content-type'] = 'application/json'
            headers['referer'] = f'https://{self.web_host}/v4/editor'
            url = f"https://{self.api_host}/gateway/sd-api/generate/image"
            response = requests.request("POST", url, headers=headers, data=payload)
            self.logger.info(f"mobile：{self.userInfo['mobile']}，{response.text}")
            res = json.loads(response.text)

            if res['code'] == 0:
                res = self.progress_msg(headers, res['data'])
                url = f"https://{self.api_host}/api/www/log/acceptor/f"
                payload = json.dumps({
                    "abtest": [
                        {
                            "name": "image_recommend",
                            "group": "IMAGE_REC_SERVICE"
                        },
                        {
                            "name": "model_recommend",
                            "group": "PERSONALIZED_RECOMMEND"
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
                            "frontCustomerReq": res['data']['frontCustomerReq'],
                            "text2img": self.param['text2img'],
                            "adetailerEnable": 0,
                            "additionalNetwork": self.param['additionalNetwork'],
                            "taskQueuePriority": 1
                        },
                        "gen-img-type": "txt2img"
                    }
                })
                response = requests.request("POST", url, headers=headers, data=payload)

                payload = json.dumps({
                    "abtest": [
                        {
                            "name": "image_recommend",
                            "group": "IMAGE_REC_SERVICE"
                        },
                        {
                            "name": "model_recommend",
                            "group": "PERSONALIZED_RECOMMEND"
                        }
                    ],
                    "sys": "SD",
                    "t": 2,
                    "uuid": self.userInfo['uuid'],
                    "cid": self.webid,
                    "page": "SD_GENERATE",
                    "pageUrl": f"https://{self.web_host}/v4/editor#/?id=undefined&defaultCheck=undefined&type=undefined",
                    "ct": time.time(),
                    "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.160 Safari/537.36",
                    "referer": f"https://{self.web_host}/sd",
                    "e": "sdp.generate.success",
                    "var": {
                        "generateId": self.frontId,
                        "gen-img-type": "txt2img",
                        "serverId": res['data']['generateId']
                    }
                })
                response = requests.request("POST", url, headers=headers, data=payload)

                print(response.text)
                for user_uuid, model_list in runCount.items():
                    for modelId, model in model_list.items():
                        query = RunStatistics.select().where(RunStatistics.user_uuid == user_uuid, RunStatistics.modelId == modelId,
                                                             RunStatistics.day == self.day)
                        if query.exists():
                            runCount = int(query.dicts().get().get('runCount'))
                            RunStatistics.update(
                                runCount=runCount + model['count'],
                                timestamp=datetime.datetime.now()
                            ).where(RunStatistics.user_uuid == user_uuid, RunStatistics.modelId == modelId, RunStatistics.day == self.day).execute()
                        else:
                            RunStatistics.insert(
                                user_uuid=user_uuid,
                                modelId=modelId,
                                modelName=model['modelName'],
                                runCount=model['count'],
                                day=self.day
                            ).execute()

    def progress_msg(self, headers, progress_code):
        url = f"https://{self.api_host}/gateway/sd-api/generate/progress/msg/{progress_code}"

        payload = json.dumps({})
        response = requests.request("POST", url, headers=headers, data=payload)
        return json.loads(response.text)


if __name__ == '__main__':
    users = get_users()
    for user in random.sample(users, 4):
        try:
            Image(user['usertoken'], user['webid']).gen_image()
        except Exception as e:
            print(e)
