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

from liblibart.SBase import SBase
from liblibart.CookieUtils import get_users, load_from_suanlibuzu_users, save_to_suanlibuzu_users
from liblibart.SStatistics import RunStatistics

from dotenv import load_dotenv, find_dotenv
from pathlib import Path

# 指定env文件
env_path = Path.cwd().joinpath('env').joinpath('sos.env')
env_path.parent.mkdir(exist_ok=True)
load_dotenv(find_dotenv(str(env_path)))


class SImage(SBase):
    _instance_lock = threading.Lock()

    def __init__(self, token, webid, bl_uid, log_filename):
        super().__init__(token, webid, bl_uid, log_filename)
        self.param = copy.deepcopy(self.gen_param)
        self.param['cid'] = self.webid

    def __new__(cls, *args, **kwargs):
        if not hasattr(SImage, "_instance"):
            with SImage._instance_lock:
                if not hasattr(SImage, "_instance"):
                    SImage._instance = object.__new__(cls)
        return SImage._instance

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
                    userUuid = value['user_uuid']
                    run_model = runCount.setdefault(userUuid, {})
                    __model = run_model.setdefault(modelId, value)
                    run_count = __model.setdefault('count', 0)
                    runCount[userUuid][modelId]['count'] = run_count + 1
                    if value['modelType'] == 5:
                        del value['user_uuid']
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

    def gen(self, runCount):
        self.param["checkpointId"] = self.to_run_checkpointId
        payload = json.dumps(self.param)

        headers = self.headers
        headers['accept-language'] = 'en'
        headers['content-type'] = 'application/json'
        headers['referer'] = f'https://{self.web_host}/aigenerator'
        url = f"https://{self.api_host}/gateway/sd-api/gen/tool/shake"
        response = requests.request("POST", url, headers=headers, data=payload)
        res = json.loads(response.text)

        if res['code'] == 0:
            self.getLogger().info(f"nickname：{self.userInfo['nickname']} generate image，{response.text}")
            url = f"https://{self.api_host}/api/www/log/acceptor/f"
            payload = json.dumps({
                "uuid": self.uuid,
                "cid": self.webid,
                "ct": time.time(),
                "pageUrl": f"https://{self.api_host}/aigenerator",
                "ua": headers['user-agent'],
                "e": "tool.shake",
                "var": {
                    "original_prompt": self.prompt,
                    "mode": "pro",
                    "sd-generate-req": {
                        "adetailerEnable": 1,
                        "mode": 1,
                        "vae": 22541,
                        "checkpointId": checkpointId,
                        "additionalNetwork": self.param['additionalNetwork'],
                        "adetailerList": self.param['adetailerList'],
                        "generateType": 1,
                        "text2img": self.param['text2img'],
                    }
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
                suanlibuzu_user = load_from_suanlibuzu_users(True)
                suanlibuzu_user.append(self.userInfo['uuid'])
                save_to_suanlibuzu_users(list(set(suanlibuzu_user)), True)
            return 'suanlibuzu'
        elif res['code'] == 1100000102:
            return 'tokenwuxiao'
        else:
            self.getLogger().error(response.text)
            return 'qitacuowu'

    def get_percent(self, image_num):
        url = f"https://{self.api_host}/gateway/sd-api/generate/progress/msg/v1/{image_num}"
        payload = json.dumps({
            "flag": 3,
            "cid": self.webid
        })
        headers = copy.deepcopy(self.headers)
        headers['content-type'] = 'application/json'
        headers['referer'] = f'https://{self.web_host}/aigenerator'
        response = requests.request("POST", url, headers=headers, data=payload)
        return json.loads(response.text)

    def nps(self):
        url = f"https://{self.api_host}/gateway/sd-api/common/getStatisticsCount"

        payload = json.dumps({
            "businessType": "nps",
            "source": 3,
            "cid": self.webid
        })
        headers = copy.deepcopy(self.headers)
        headers['content-type'] = 'application/json'
        headers['referer'] = f'https://{self.web_host}/aigenerator'

        response = requests.request("POST", url, headers=headers, data=payload)
        self.getLogger().info(f"nickname：{self.userInfo['nickname']} getStatisticsCount，{response.text}")

    def progress_msg(self, headers, progress_code):
        url = f"https://{self.api_host}/gateway/sd-api/generate/progress/msg/{progress_code}"

        payload = json.dumps({})
        response = requests.request("POST", url, headers=headers, data=payload)
        return json.loads(response.text)


if __name__ == '__main__':
    users = get_users(cookie_name="shakker_cookie", usertoken_name="liblibai_usertoken")
    for user in random.sample(users, 1):
    # for user in users:
        try:
            SImage(user['usertoken'], user['webid'], user['_bl_uid'], f'/mitmproxy/logs/SImage_{os.getenv("RUN_OS_KEY")}.log').gen_image()
        except Exception as e:
            print(e)
