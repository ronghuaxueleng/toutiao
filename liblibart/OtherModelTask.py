# -*- coding: utf-8 -*-
import base64
import datetime
import time
import traceback

import requests
import json

from liblibart.CookieUtils import save_othercheckpoints, save_otherloras
from liblibart.OtherModel import OtherModel

base64_web_host = 'd3d3LmxpYmxpYi5hcnQ='
base64_api_host = 'bGlibGliLWFwaS52aWJyb3UuY29t'
api_host = str(base64.b64decode(base64_api_host), 'utf-8')
web_host = str(base64.b64decode(base64_web_host), 'utf-8')

url = f"https://{web_host}/api/www/model/feed/stream?timestamp=1739582730020"

headers = {
    'authority': web_host,
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-CN,zh;q=0.9',
    'content-type': 'application/json',
    'dnt': '1',
    'origin': f'https://{web_host}',
    'referer': f'https://{web_host}/',
    'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.95 Safari/537.36',
}


def getModel(modelType=1):
    """
    获取模型
    :param modelType: 模型类型 1 checkpoint 5 lora
    :return:
    """
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
            modelType
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

    models = OtherModel.select()
    saved_models = {}
    for model in models:
        __model = saved_models.setdefault(model.user_uuid, {})
        key = f'{model.user_uuid}_{model.modelId}'
        __model[key] = model
        saved_models[model.user_uuid] = __model

    response = requests.request("POST", url, headers=headers, data=payload)
    data = json.loads(response.text)
    for model in data['data']['data']:
        version_url = f"https://{web_host}/api/www/model/getByUuid/{model['uuid']}?timestamp={time.time()}"
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
                if key in saved_models:
                    del saved_models[key]
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
    getModel(1)
    models = OtherModel.select().where(OtherModel.isEnable == True, OtherModel.modelType == 1, OtherModel.vipUsed != 1,
                                       OtherModel.showType == 1).execute()

    checkpoints = []
    for model in models:
        checkpoints.append(model.modelId)
    print(checkpoints)
    save_othercheckpoints(checkpoints)

    getModel(5)
    models = OtherModel.select().where(OtherModel.isEnable == True, OtherModel.modelType == 5, OtherModel.vipUsed != 1,
                                       OtherModel.showType == 1).execute()
    loras = []
    for model in models:
        loras.append(json.loads(model.otherInfo))
    print(loras)
    save_otherloras(loras)
