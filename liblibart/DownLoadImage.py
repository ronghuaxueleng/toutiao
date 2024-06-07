# -*- coding: utf-8 -*-
import datetime
import json
import random
import time

import requests

from liblibart.CookieUtils import get_users
from liblibart.Statistics import DownLoadImageStatistics
from liblibart.UserInfo import UserInfo


class DownLoadImage(UserInfo):
    def __init__(self, token, webid):
        super().__init__(token, webid)

    def download(self):
        url = f"https://{self.api_host}/gateway/sd-api/generate/image/history"

        day = datetime.datetime.now() - datetime.timedelta(days=7)
        fromTime = datetime.datetime(day.year, day.month, day.day).strftime('%Y-%m-%d 00:00:00')

        payload = json.dumps({
            "pageSize": 1,
            "pageNo": 1,
            "fromTime": fromTime,
            "toTime": datetime.datetime.now().strftime("%Y-%m-%d 24:00:00")
        })
        headers = self.headers
        headers['content-type'] = 'application/json'
        headers['referer'] = f'https://{self.web_host}/v4/editor'

        response = requests.request("POST", url, headers=headers, data=payload)
        res = json.loads(response.text)

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
        self.logger.info(response.text)
        idList = []
        downloadImageCount = {}
        for img in res['data']['list']:
            idList.append(img['id'])
            for model in img['param']['mixModels']:
                try:
                    modelVersionId = model['modelVersionId']
                    _model = self.model_dict[modelVersionId]
                    userUuid = _model['userUuid']
                    download_model = downloadImageCount.setdefault(userUuid, {})
                    __model = download_model.setdefault(modelVersionId, _model)
                    download_count = __model.setdefault('count', 0)
                    downloadImageCount[userUuid][modelVersionId]['count'] = download_count + 1
                except Exception as e:
                    self.logger.error(e)


        url = f"https://{self.api_host}/gateway/sd-api/generate/image/delete"

        payload = json.dumps({
            "idList": idList
        })

        response = requests.request("POST", url, headers=headers, data=payload)

        self.logger.info(response.text)
        for user_uuid, model_list in downloadImageCount.items():
            for modelId, model in model_list.items():
                query = DownLoadImageStatistics.select().where(DownLoadImageStatistics.user_uuid == user_uuid, DownLoadImageStatistics.modelId == modelId,
                                                               DownLoadImageStatistics.day == self.day)
                if query.exists():
                    downloadImageCount = int(query.dicts().get().get('downloadImageCount'))
                    DownLoadImageStatistics.update(
                        downloadImageCount=downloadImageCount + model['count'],
                        timestamp=datetime.datetime.now()
                    ).where(DownLoadImageStatistics.user_uuid == user_uuid, DownLoadImageStatistics.modelId == modelId, DownLoadImageStatistics.day == self.day).execute()
                else:
                    DownLoadImageStatistics.insert(
                        user_uuid=user_uuid,
                        modelId=modelId,
                        modelName=model['modelName'],
                        downloadImageCount=model['count'],
                        day=self.day
                    ).execute()


if __name__ == '__main__':
    users = get_users()
    for user in users:
        try:
            DownLoadImage(user['usertoken'], user['webid']).download()
        except Exception as e:
            print(e)
