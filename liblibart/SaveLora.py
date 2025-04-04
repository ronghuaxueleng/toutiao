# -*- coding: utf-8 -*-
import datetime
import json
import os
import time
import traceback

import requests

from CookieUtils import get_users, save_checkpoints
from UserInfo import UserInfo
from Model import Model

from dotenv import load_dotenv, find_dotenv
from pathlib import Path

# 指定env文件
env_path = Path.cwd().joinpath('env').joinpath('os.env')
env_path.parent.mkdir(exist_ok=True)
load_dotenv(find_dotenv(str(env_path)))


class SaveLora(UserInfo):
    def __init__(self, token, webid, log_filename):
        super().__init__(token, webid, log_filename)

    def get_models(self, saved_models=None):
        if saved_models is None:
            saved_models = {}
        headers = self.headers
        headers['content-type'] = 'application/json'
        headers['referer'] = f"https://{self.web_host}/userpage/{self.userInfo['uuid']}/publish"

        _saved_models = {}
        if self.userInfo['uuid'] in saved_models:
            _saved_models = saved_models[self.userInfo['uuid']]

        pageNo = 1
        total_models = None
        while total_models is None or total_models > 0:
            url = f"https://{self.web_host}/api/www/model/list?timestamp={time.time()}"
            payload = json.dumps({
                "pageNo": pageNo,
                "pageSize": 10,
                "status": -2,
                "type": 0
            })

            response = requests.request("POST", url, headers=headers, data=payload)
            data = json.loads(response.text)
            pageNo = pageNo + 1
            total_models = len(data['data']['list'])
            for model in data['data']['list']:
                version_url = f"https://{self.web_host}/api/www/model/getByUuid/{model['uuid']}?timestamp={time.time()}"
                payload = {}
                response = requests.request("POST", version_url, headers=headers, data=payload)

                model_data = json.loads(response.text)
                if model_data['code'] == 0:
                    for version in model_data['data']['versions']:
                        to_save_data = {
                            "modelId": version["id"],
                            "type": 0,
                            "modelName": model["name"],
                            "modelVersionName": version['name'],
                            "weight": 0.8,
                            "user_uuid": self.userInfo['uuid'],
                            "modelType": model['modelType']
                        }
                        key = f"{self.userInfo['uuid']}_{version['id']}"
                        if key in _saved_models:
                            del _saved_models[key]
                            Model.update(
                                user_name=self.userInfo['nickname'],
                                modelName=model["name"],
                                modelVersionName=version['name'],
                                showType=version['showType'],
                                updateTime=version['updateTime'],
                                vipUsed=model['vipUsed'],
                                otherInfo=json.dumps(to_save_data),
                                timestamp=datetime.datetime.now()
                            ).where(Model.user_uuid == self.userInfo['uuid'], Model.modelId == version["id"]).execute()
                        else:
                            try:
                                Model.insert(
                                    user_uuid=self.userInfo['uuid'],
                                    user_name=self.userInfo['nickname'],
                                    modelId=version["id"],
                                    modelName=model["name"],
                                    modelVersionName=version['name'],
                                    modelType=model['modelType'],
                                    showType=version['showType'],
                                    vipUsed=model['vipUsed'],
                                    otherInfo=json.dumps(to_save_data),
                                    createTime=version['createTime'],
                                    updateTime=version['updateTime'],
                                ).execute()
                            except Exception as e:
                                self.getLogger().error(traceback.format_exc())

        for key, model in _saved_models.items():
            try:
                Model.delete().where(Model.modelId == model.modelId).execute()
            except Exception as e:
                self.getLogger().error(traceback.format_exc())


if __name__ == '__main__':
    models = Model.select()
    saved_models = {}
    for model in models:
        __model = saved_models.setdefault(model.user_uuid, {})
        key = f'{model.user_uuid}_{model.modelId}'
        __model[key] = model
        saved_models[model.user_uuid] = __model
    users = get_users()
    for user in users:
        try:
            SaveLora(user['usertoken'], user['webid'],
                     f'/mitmproxy/logs/SaveLora_{os.getenv("RUN_OS_KEY")}.log').get_models(saved_models)
        except Exception as e:
            print('error', e)
            print(traceback.format_exc())

    models = Model.select().where(Model.isEnable == True, Model.modelType == 1, Model.vipUsed != 1,
                                  Model.showType == 1).execute()

    checkpoints = {}
    for model in models:
        ids = checkpoints.setdefault(model.user_uuid, [])
        ids.append(model.modelId)
        checkpoints[model.user_uuid] = ids
    print(checkpoints)
    save_checkpoints(checkpoints)
