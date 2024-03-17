# -*- coding: utf-8 -*-
import datetime
import json
import random
import time
import uuid

import requests

from liblibart.Statistics import RunStatistics
from liblibart.UserInfo import UserInfo
from liblibart.ql import ql_env


class Image(UserInfo):
    def __init__(self, token):
        super().__init__(token)
        self.frontId = str(uuid.uuid1())

    def gen_image(self):
        url = f"https://{self.api_host}/gateway/sd-api/generate/image"

        param = {
            "checkpointId": 1094830,
            "generateType": 1,
            "frontCustomerReq": {
                "frontId": self.frontId,
                "windowId": "",
                "tabType": "txt2img",
                "conAndSegAndGen": "gen"
            },
            "text2img": {
                "prompt": ",1girl,chinese new year,photorealistic,photography,jewelry,indoors,red sweater,simple background,tassel,lantern,make up,Chinese fan,hair ornament,dress ",
                "negativePrompt": "text,chinese red packet,leg,(worst quality, low quality:2), monochrome, zombie,overexposure, watermark,text,bad anatomy,bad hand,extra hands,extra fingers,too many fingers,fused fingers,bad arm,distorted arm,extra arms,fused arms,extra legs,missing leg,disembodied leg,extra nipples, detached arm, liquid hand,inverted hand,disembodied limb, small breasts, loli, oversized head,extra body,completely nude,",
                "extraNetwork": "",
                "samplingMethod": 24,
                "samplingStep": 30,
                "width": 512,
                "height": 768,
                "imgCount": 1,
                "cfgScale": 5,
                "seed": -1,
                "seedExtra": 0,
                "hiResFix": 0,
                "restoreFaces": 0,
                "tiling": 0,
                "clipSkip": 2
            },
            "adetailerEnable": 0,
            "adetailerList": [
                {
                    "adetailerModelVerId": 0,
                    "prompt": "",
                    "negativePrompt": "",
                    "detection": {
                        "threshold": 0.3,
                        "maskMinAreaRatio": 0,
                        "maskMaxAreaRatio": 1
                    },
                    "maskPreprocessing": {
                        "maskXOffset": 0,
                        "maskYOffset": 0,
                        "maskScaling": 4,
                        "maskMergeMode": 1
                    },
                    "inpainting": {
                        "maskBlur": 4,
                        "denoisingStrength": 0.4,
                        "onlyMasked": True,
                        "onlyMaskedPaddingPixels": 32,
                        "separateWH": False,
                        "separateSteps": True,
                        "adetailerSteps": 25,
                        "separateCFGScale": False,
                        "separateNoiseMultiplier": False,
                        "restoreFacesAfterADetailer": False
                    }
                }
            ],
            "additionalNetwork": [],
            "taskQueuePriority": 0
        }
        runCount = {}
        for userUuid, models in self.user_model_dict.items():
            if len(models) >= 6:
                my_loras = random.sample(models, 6)
            else:
                my_loras = models
            for my_lora in my_loras:
                if my_lora['status'] == 0:
                    value = json.loads(my_lora['value'])
                    modelId = value['modelId']
                    userUuid = value['userUuid']
                    run_model = runCount.setdefault(userUuid, {})
                    __model = run_model.setdefault(modelId, value)
                    run_count = __model.setdefault('count', 0)
                    runCount[userUuid][modelId]['count'] = run_count + 1
                    if value['modelType'] == 5:
                        del value['userUuid']
                        del value['modelType']
                        param['additionalNetwork'].append(value)
        if len(param['additionalNetwork']) > 0:
            payload = json.dumps(param)
            headers = self.headers
            headers['content-type'] = 'application/json'
            headers['referer'] = f'https://{self.web_host}/v4/editor'

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
                    "cid": "1701652270086cvpnqgrl",
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
                            "text2img": param['text2img'],
                            "adetailerEnable": 0,
                            "additionalNetwork": param['additionalNetwork'],
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
                    "cid": "1701652270086cvpnqgrl",
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
    tokens = [
        'd1894681b7c5438b9051b840431e9b59',
        '3cc0cddb72874db49eb02f60d81fbf31',
        '5035e42609394bdfa3ddaee8b88a1b78',
        '66149bee12304248beb571d1c0d9e553',
        '5dfe53b85ed947a6a92586182768a84e',
        '48e8c753b8674b1499f274d8973b9e60'
    ]
    for token in tokens:
        try:
            Image(token).gen_image()
        except Exception as e:
            print(e)
