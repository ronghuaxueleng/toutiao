# -*- coding: utf-8 -*-
import datetime
import os
import random
import time
import traceback

import requests
import json

from liblibart.CookieUtils import get_users
from liblibart.Statistics import DownloadModelStatistics
from liblibart.UserInfo import UserInfo
from liblibart.Model import Model as MyModel

from dotenv import load_dotenv, find_dotenv
from pathlib import Path

# 指定env文件
env_path = Path.cwd().joinpath('env').joinpath('os.env')
env_path.parent.mkdir(exist_ok=True)
load_dotenv(find_dotenv(str(env_path)))


class DownloadModel(UserInfo):
    def __init__(self, token, webid, log_filename):
        super().__init__(token, webid, log_filename)

    def download_model(self):
        global query, downloadModelCount
        download_models = []
        models = MyModel.select(
            MyModel.user_uuid,
            MyModel.modelId,
            MyModel.modelName
        ).where(MyModel.isEnable == True,
                MyModel.user_uuid != self.uuid, MyModel.vipUsed != 1).execute()
        for model in models:
            download_models.append(model.modelId)
        url = f"https://{self.web_host}/api/www/model/list?timestamp={time.time()}"
        for uuid in self.uuids:
            if uuid != self.uuid:
                for pageNo in range(1, 5):
                    payload = json.dumps({
                        "pageNo": pageNo,
                        "pageSize": 20,
                        "uuid": uuid,
                        "status": -2,
                        "type": 0
                    })
                    headers = self.headers
                    headers['content-type'] = 'application/json'
                    headers['referer'] = f'https://{self.web_host}/userpage/{uuid}/publish'

                    response = requests.request("POST", url, headers=headers, data=payload)

                    data = json.loads(response.text)
                    model_list = data['data']['list']
                    if len(model_list) > 0:
                        for model in model_list:
                            url = f"https://{self.web_host}/api/www/model/getByUuid/{model['uuid']}?timestamp={time.time()}"
                            payload = {}
                            response = requests.request("POST", url, headers=headers, data=payload)

                            model_data = json.loads(response.text)
                            for version in model_data['data']['versions']:
                                if version['id'] in download_models:
                                    try:
                                        query = DownloadModelStatistics.select().where(
                                            DownloadModelStatistics.user_uuid == uuid,
                                            DownloadModelStatistics.modelId == version['id'],
                                            DownloadModelStatistics.day == self.day)
                                        if query.exists():
                                            downloadModelCount = int(query.dicts().get().get('downloadModelCount'))
                                            if downloadModelCount >= 1000:
                                                continue
                                    except Exception as e:
                                        self.getLogger().error(f'更新下载次数失败: {traceback.format_exc()}')
                                    url = f"https://{self.web_host}/api/www/community/downloadCheck?timestamp={time.time()}"
                                    payload = json.dumps({
                                        "uuid": model["uuid"],
                                        "cid": self.webid,
                                        "modelName": model["name"],
                                        "modelVersionId": version['uuid'],
                                        "modelId": model["id"]
                                    })

                                    response = requests.request("POST", url, headers=headers, data=payload)

                                    self.getLogger().info(
                                        f"token:{uuid}, 模型[{model['name']}], 版本[{version['uuid']}], 运行结果：{response.text}")

                                    url = f"https://{self.web_host}/api/www/log/acceptor/f?timestamp={time.time()}"

                                    payload = json.dumps({
                                        "t": 2,
                                        "e": "model.view.download",
                                        "page": 2,
                                        "var": {
                                            "download": "start",
                                            "model_id": model['uuid'],
                                            "version_id": version['id']
                                        },
                                        "cid": self.webid,
                                        "uuid": self.userInfo['uuid'],
                                        "ct": time.time(),
                                        "pageUrl": f"https://{self.web_host}/modelinfo/{model['uuid']}",
                                        "sys": "COMMUNITY",
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
                                        "ua": "mozilla/5.0 (windows nt 10.0; win64; x64) applewebkit/537.36 (khtml, like gecko) chrome/119.0.6045.160 safari/537.36"
                                    })
                                    headers['referer'] = f"https://{self.web_host}/modelinfo/{model['uuid']}"

                                    requests.request("POST", url, headers=headers, data=payload)
                                    try:
                                        if query.exists():
                                            DownloadModelStatistics.update(
                                                downloadModelCount=downloadModelCount + 1,
                                                timestamp=datetime.datetime.now()
                                            ).where(DownloadModelStatistics.user_uuid == uuid,
                                                    DownloadModelStatistics.modelId == version['id'],
                                                    DownloadModelStatistics.day == self.day).execute()
                                        else:
                                            DownloadModelStatistics.insert(
                                                user_uuid=uuid,
                                                modelId=version['id'],
                                                modelName=model["name"],
                                                downloadModelCount=1,
                                                day=self.day
                                            ).execute()
                                    except Exception as e:
                                        self.getLogger().error(f'更新下载次数失败: {traceback.format_exc()}')
                                    time.sleep(2)


if __name__ == '__main__':
    users = get_users()
    for user in random.sample(users, 4):
        downloadModel = DownloadModel(user['usertoken'], user['webid'],
                      f'/mitmproxy/logs/DownloadModel_{os.getenv("RUN_OS_KEY")}.log')
        try:
            downloadModel.download_model()
        except Exception as e:
            downloadModel.getLogger().error(f"nickname：{downloadModel.userInfo['nickname']} DownloadModel，{traceback.format_exc()}")
