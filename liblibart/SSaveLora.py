# -*- coding: utf-8 -*-
import datetime
import json
import os
import time
import traceback

import requests

from liblibart.CookieUtils import get_users
from liblibart.SModel import Model
from liblibart.SUserInfo import SUserInfo

from dotenv import load_dotenv, find_dotenv
from pathlib import Path

from liblibart.DbUtils import get_redis_conn

# 指定env文件
env_path = Path.cwd().joinpath('env').joinpath('sos.env')
env_path.parent.mkdir(exist_ok=True)
load_dotenv(find_dotenv(str(env_path)))
r = get_redis_conn()


class SSaveLora(SUserInfo):
    def __init__(self, token, webid, bl_uid, log_filename):
        super().__init__(token, webid, bl_uid, log_filename)

    def get_models(self, saved_models=None):
        if saved_models is None:
            saved_models = {}
        headers = self.headers
        headers['content-type'] = 'application/json'
        headers['referer'] = f"https://{self.web_host}/userpage/{self.userInfo['uuid']}/publish"

        __saved_models = saved_models[self.userInfo['uuid']]

        pageNo = 1
        total_models = None
        while total_models is None or total_models > 0:
            url = f"https://{self.api_host}/api/www/model/list?timestamp={time.time()}"
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
                version_url = f"https://{self.api_host}/api/www/model/getByUuid/{model['uuid']}?timestamp={time.time()}"
                payload = {}
                response = requests.request("POST", version_url, headers=headers, data=payload)

                model_data = json.loads(response.text)
                if model_data['code'] == 0:
                    tagCodesV2 = []
                    for tag in model_data['data']['tagsV2']['modelContent']:
                        tagCodesV2.append(tag['id'])

                    for version in model_data['data']['versions']:
                        otherInfo = {
                            "name": model['name'],
                            "versionId": version['id'],
                            "modelId": model['id'],
                            "versionName": version['name'],
                            "uuid": version['uuid'],
                            "tagV2Ids": tagCodesV2,
                            "baseType": "SD 1.5",
                            "modelType": model['modelTypeName'].upper(),
                            "runCount": version['runCount'],
                            "userAvatar": model['avatar'],
                            "userName": model['nickname'],
                            "imageUrl": model['imageUrl'],
                            "vipUsed": version['vipUsed'],
                            "weight": 1,
                            "modelUuid": model['uuid'],
                            "triggerWord": version['triggerWord'],
                            "remark": "",
                            "ngPrompt": "nsfw,EasyNegative, EasyNegativeV2, ng_deepnegative_v1_75t, worst quality, low quality,bad-hands-5,BadHandsV5"
                        }
                        key = f"{self.userInfo['uuid']}_{version['id']}"
                        if key in __saved_models:
                            del __saved_models[key]
                            Model.update(
                                user_name=self.userInfo['nickname'],
                                modelName=model["name"],
                                modelVersionName=version['name'],
                                showType=version['showType'],
                                updateTime=version['updateTime'],
                                vipUsed=model['vipUsed'],
                                otherInfo=json.dumps(otherInfo),
                                timestamp=datetime.datetime.now()
                            ).where(Model.user_uuid == self.userInfo['uuid'], Model.modelId == version["id"]).execute()
                        else:
                            Model.insert(
                                user_uuid=self.userInfo['uuid'],
                                user_name=self.userInfo['nickname'],
                                modelId=version["id"],
                                modelName=model["name"],
                                modelVersionName=version['name'],
                                modelType=model['modelType'],
                                showType=version['showType'],
                                vipUsed=model['vipUsed'],
                                otherInfo=json.dumps(otherInfo),
                                createTime=version['createTime'],
                                updateTime=version['updateTime'],
                            ).execute()

        for model in __saved_models:
            Model.delete().where(Model.modelId == model.modelId).execute()


if __name__ == '__main__':
    models = Model.select()
    saved_models = {}
    for model in models:
        __model = saved_models.setdefault(model.user_uuid, {})
        key = f'{model.user_uuid}_{model.modelId}'
        __model[key] = model
        saved_models[model.user_uuid] = __model
    users = get_users(cookie_name="shakker_cookie", usertoken_name="liblibai_usertoken")
    for user in users:
        try:
            SSaveLora(user['usertoken'], user['webid'], user['_bl_uid'],
                      f'/mitmproxy/logs/SSaveLora_{os.getenv("RUN_OS_KEY")}.log').get_models(saved_models)
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
    r.set("s_checkpoints", json.dumps(checkpoints))
