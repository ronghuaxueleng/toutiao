# -*- coding: utf-8 -*-
import datetime
import json
import time

import requests

from liblibart.Statistics import Statistics
from liblibart.UserInfo import UserInfo


class DownLoadImage(UserInfo):
    def __init__(self, token):
        super().__init__(token)

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

        idList = []
        downloadImageCount = {}
        for img in res['data']['list']:
            idList.append(img['id'])
            for model in img['param']['mixModels']:
                modelVersionId = model['modelVersionId']
                _model = self.model_dict[modelVersionId]
                userUuid = _model['userUuid']
                download_model = downloadImageCount.setdefault(userUuid, {})
                __model = download_model.setdefault(modelVersionId, _model)
                download_count = __model.setdefault('count', 0)
                downloadImageCount[userUuid][modelVersionId]['count'] = download_count + 1


        url = f"https://{self.api_host}/gateway/sd-api/generate/image/delete"

        payload = json.dumps({
            "idList": idList
        })

        response = requests.request("POST", url, headers=headers, data=payload)

        print(response.text)
        for user_uuid, model_list in downloadImageCount.items():
            for modelId, model in model_list.items():
                query = Statistics.select().where(Statistics.user_uuid == user_uuid, Statistics.modelId == modelId,
                                                  Statistics.day == self.day)
                if query.exists():
                    downloadImageCount = int(query.dicts().get().get('downloadImageCount'))
                    Statistics.update(
                        downloadImageCount=downloadImageCount + model['count'],
                        timestamp=datetime.datetime.now
                    ).where(Statistics.user_uuid == user_uuid, Statistics.modelId == modelId, Statistics.day == self.day).execute()
                else:
                    Statistics.insert(
                        user_uuid=user_uuid,
                        modelId=modelId,
                        modelName=model['modelName'],
                        downloadImageCount=model['count'],
                        day=self.day
                    ).execute()


if __name__ == '__main__':
    tokens = [
        'd1894681b7c5438b9051b840431e9b59',
        '3cc0cddb72874db49eb02f60d81fbf31',
        '5035e42609394bdfa3ddaee8b88a1b78',
        '66149bee12304248beb571d1c0d9e553',
        '5dfe53b85ed947a6a92586182768a84e'
    ]
    for token in tokens:
        try:
            DownLoadImage(token).download()
        except Exception as e:
            print(e)
