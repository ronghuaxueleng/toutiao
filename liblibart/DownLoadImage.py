# -*- coding: utf-8 -*-
import datetime
import json
import time

import requests

from liblibart.UserInfo import UserInfo


class DownLoadImage(UserInfo):
    def __init__(self, token):
        super().__init__(token)

    def download(self):
        url = "https://liblib-api.vibrou.com/gateway/sd-api/generate/image/history"

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
        headers['referer'] = 'https://www.liblib.art/v4/editor'

        response = requests.request("POST", url, headers=headers, data=payload)
        res = json.loads(response.text)

        url = "https://liblib-api.vibrou.com/api/www/log/acceptor/f"

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
            "pageUrl": "https://www.liblib.art/v4/editor#/?id=undefined&defaultCheck=undefined&type=undefined",
            "ct": time.time(),
            "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.160 Safari/537.36",
            "referer": "https://www.liblib.art/sd",
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
        for img in res['data']['list']:
            idList.append(img['id'])

        url = "https://liblib-api.vibrou.com/gateway/sd-api/generate/image/delete"

        payload = json.dumps({
            "idList": idList
        })

        response = requests.request("POST", url, headers=headers, data=payload)

        print(response.text)


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
