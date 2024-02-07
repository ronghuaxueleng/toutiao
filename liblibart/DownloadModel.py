# -*- coding: utf-8 -*-
import time

import requests
import json

from liblibart.UserInfo import UserInfo
from liblibart.ql import ql_env


class DownloadModel(UserInfo):
    def __init__(self, token):
        super().__init__(token)

    def download_model(self, pageNo, download_models):
        url = f"https://liblib-api.vibrou.com/api/www/model/list?timestamp={time.time()}"

        payload = json.dumps({
            "pageNo": pageNo,
            "pageSize": 20,
            "uuid": "02749e73219936808ff45d707b2d01cf",
            "status": -2,
            "type": 0
        })
        headers = self.headers
        headers['content-type'] = 'application/json'
        headers['referer'] = 'https://www.liblib.art/userpage/02749e73219936808ff45d707b2d01cf/publish'

        response = requests.request("POST", url, headers=headers, data=payload)

        data = json.loads(response.text)
        for model in data['data']['list']:
            url = f"https://liblib-api.vibrou.com/api/www/model/getByUuid/{model['uuid']}?timestamp={time.time()}"
            payload = {}
            response = requests.request("POST", url, headers=headers, data=payload)

            model_data = json.loads(response.text)
            for version in model_data['data']['versions']:
                if version['id'] in download_models:
                    url = f"https://liblib-api.vibrou.com/api/www/community/downloadCheck?timestamp={time.time()}"
                    payload = json.dumps({
                        "uuid": model["uuid"],
                        "cid": "1701652270086cvpnqgrl",
                        "modelName": model["name"],
                        "modelVersionId": version['uuid'],
                        "modelId": model["id"]
                    })

                    response = requests.request("POST", url, headers=headers, data=payload)

                    self.logger.info(f"token:{token}, 模型[{model['name']}], 版本[{version['uuid']}], 运行结果：{response.text}")

                    url = f"https://liblib-api.vibrou.com/api/www/log/acceptor/f?timestamp={time.time()}"

                    payload = json.dumps({
                        "t": 2,
                        "e": "model.view.download",
                        "page": 2,
                        "var": {
                            "download": "start",
                            "model_id": model['uuid'],
                            "version_id": version['id']
                        },
                        "cid": "1701652270086cvpnqgrl",
                        "uuid": self.userInfo['uuid'],
                        "ct": time.time(),
                        "pageUrl": f"https://www.liblib.art/modelinfo/{model['uuid']}",
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
                    headers['referer'] = f"https://www.liblib.art/modelinfo/{model['uuid']}"

                    response = requests.request("POST", url, headers=headers, data=payload)

                    print(response.text)
                    time.sleep(2)


if __name__ == '__main__':
    my_loras = ql_env.search("my_lora")
    download_models = []
    for my_lora in my_loras:
        if my_lora['status'] == 0:
            download_models.append(json.loads(my_lora['value'])['modelId'])
    tokens = [
        'd1894681b7c5438b9051b840431e9b59',
        '3cc0cddb72874db49eb02f60d81fbf31',
        '5035e42609394bdfa3ddaee8b88a1b78',
        '66149bee12304248beb571d1c0d9e553',
        '5dfe53b85ed947a6a92586182768a84e'
    ]
    for pageNo in range(1, 5):
        for token in tokens:
            try:
                DownloadModel(token).download_model(pageNo, download_models)
            except Exception as e:
                print(e)
