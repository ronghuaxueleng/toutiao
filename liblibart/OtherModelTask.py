# -*- coding: utf-8 -*-
import datetime
import time
import traceback

import requests
import json

from liblibart.OtherModel import OtherModel

url = "https://www.liblib.art/api/www/model/feed/stream?timestamp=1739582730020"

headers = {
    'authority': 'www.liblib.art',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-CN,zh;q=0.9',
    'content-type': 'application/json',
    'dnt': '1',
    'origin': 'https://www.liblib.art',
    'referer': 'https://www.liblib.art/',
    'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.95 Safari/537.36',
    'webid': '1738378706302qrgpkfxe'
}


def getModel():
    payload = json.dumps({
        "isHome": True,
        "page": 1,
        "pageSize": 30,
        "sort": 0,
        "followed": 0,
        "periodTime": [
            "all"
        ],
        "tagIds": [],
        "models": [
            1
        ],
        "types": [
            1
        ],
        "vipType": [
            "0"
        ],
        "modelUsage": [],
        "modelLicense": [],
        "tagV2Id": None
    })

    _saved_models = {}
    response = requests.request("POST", url, headers=headers, data=payload)
    data = json.loads(response.text)
    for model in data['data']['data']:
        version_url = f"https://www.liblib.art/api/www/model/getByUuid/{model['uuid']}?timestamp={time.time()}"
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
                    "user_uuid": model['userUuid'],
                    "modelType": model['modelType']
                }
                key = f"{model['userUuid']}_{version['id']}"
                if key in _saved_models:
                    del _saved_models[key]
                    OtherModel.update(
                        user_name=model['nickname'],
                        modelName=model["name"],
                        modelVersionName=version['name'],
                        showType=version['showType'],
                        updateTime=version['updateTime'],
                        vipUsed=model['vipUsed'],
                        otherInfo=json.dumps(to_save_data),
                        timestamp=datetime.datetime.now()
                    ).where(OtherModel.user_uuid == model['userUuid'], OtherModel.modelId == version["id"]).execute()
                else:
                    try:
                        OtherModel.insert(
                            user_uuid=model['userUuid'],
                            user_name=model['nickname'],
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
                        print(traceback.format_exc())


if __name__ == '__main__':
    getModel()
