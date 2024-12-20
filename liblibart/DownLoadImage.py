# -*- coding: utf-8 -*-
import datetime
import json
import os
import random
import time
import traceback

import requests

from CookieUtils import get_users
from Statistics import DownLoadImageStatistics
from UserInfo import UserInfo

from dotenv import load_dotenv, find_dotenv
from pathlib import Path

# 指定env文件
env_path = Path.cwd().joinpath('env').joinpath('os.env')
env_path.parent.mkdir(exist_ok=True)
load_dotenv(find_dotenv(str(env_path)))


class DownLoadImage(UserInfo):
    def __init__(self, token, webid, log_filename):
        super().__init__(token, webid, log_filename)

    def download(self, delete=True, fromTime=None, pageSize=1):
        url = f"https://{self.web_host}/gateway/sd-api/generate/image/history"

        if fromTime is None:
            day = datetime.datetime.now() - datetime.timedelta(days=7)
            fromTime = datetime.datetime(day.year, day.month, day.day).strftime('%Y-%m-%d 00:00:00')

        payload = json.dumps({
            "pageSize": pageSize,
            "pageNo": 1,
            "fromTime": fromTime,
            "toTime": datetime.datetime.now().strftime("%Y-%m-%d 24:00:00")
        })
        headers = self.headers
        headers['content-type'] = 'application/json'
        headers['referer'] = f'https://{self.web_host}/v4/editor'

        response = requests.request("POST", url, headers=headers, data=payload)
        self.getLogger().info(f'查询图片生成历史结果: {response.text}')
        res = json.loads(response.text)

        if len(res['data']['list']) > 0:
            url = f"https://{self.web_host}/api/www/log/acceptor/f"

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
                "pageUrl": f"https://{self.web_host}/v4/editor#/?id=undefined&defaultCheck=undefined&type=undefined",
                "ct": time.time(),
                "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.160 Safari/537.36",
                "referer": f"https://{self.web_host}/sd",
                "e": "sdp.generate.resp.download",
                "var": {
                    "img-ids": [
                        res['data']['list'][0]['outputId']
                    ],
                    "img-urls": [
                        res['data']['list'][0]['imageId']
                    ],
                    "gen-img-type": "gallery"
                }
            })
            response = requests.request("POST", url, headers=headers, data=payload)
            self.getLogger().info(f'保存图片下载记录结果: {response.text}')
            idList = []
            downloadImageCount = {}
            for img in res['data']['list']:
                idList.append(img['id'])
                for model in img['param']['mixModels']:
                    try:
                        modelVersionId = model['modelVersionId']
                        _model = self.model_dict[modelVersionId]
                        userUuid = _model['user_uuid']
                        download_model = downloadImageCount.setdefault(userUuid, {})
                        __model = download_model.setdefault(modelVersionId, _model)
                        download_count = __model.setdefault('count', 0)
                        downloadImageCount[userUuid][modelVersionId]['count'] = download_count + 1
                    except Exception as e:
                        self.getLogger().error(f'更新下载次数失败: {traceback.format_exc()}')

            if delete:
                url = f"https://{self.web_host}/gateway/sd-api/generate/image/delete"

                payload = json.dumps({
                    "idList": idList
                })

                response = requests.request("POST", url, headers=headers, data=payload)

                self.getLogger().info(f'删除图片结果：{response.text}')
            for user_uuid, model_list in downloadImageCount.items():
                try:
                    for modelId, model in model_list.items():
                        try:
                            query = DownLoadImageStatistics.select().where(DownLoadImageStatistics.modelId == modelId,
                                                                           DownLoadImageStatistics.day == self.day)
                            if query.exists():
                                downloadImageCount = int(query.dicts().get().get('downloadImageCount'))
                                DownLoadImageStatistics.update(
                                    downloadImageCount=downloadImageCount + model['count'],
                                    timestamp=datetime.datetime.now()
                                ).where(DownLoadImageStatistics.modelId == modelId,
                                        DownLoadImageStatistics.day == self.day).execute()
                            else:
                                DownLoadImageStatistics.insert(
                                    user_uuid=user_uuid,
                                    modelId=modelId,
                                    modelName=model['modelName'],
                                    downloadImageCount=model['count'],
                                    day=self.day
                                ).execute()
                        except Exception as e:
                            self.getLogger().error(f'更新下载次数失败: {traceback.format_exc()}')
                except Exception as e:
                    self.getLogger().error(f'更新下载次数失败: {traceback.format_exc()}')



if __name__ == '__main__':
    users = get_users()
    for user in users:
        downLoadImage = DownLoadImage(user['usertoken'], user['webid'],
                      f'/mitmproxy/logs/DownLoadImage_{os.getenv("RUN_OS_KEY")}.log')
        try:
            downLoadImage.download()
        except Exception as e:
            downLoadImage.getLogger().error(f"nickname：{downLoadImage.userInfo['nickname']} DownLoadImage，{traceback.format_exc()}")
