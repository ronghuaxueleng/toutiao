# -*- coding: utf-8 -*-
import base64
import datetime
import json
import os
import time
import traceback

import requests

from CookieUtils import get_users
from SStatistics import DownLoadImageStatistics
from SUserInfo import SUserInfo

from dotenv import load_dotenv, find_dotenv
from pathlib import Path

# 指定env文件
env_path = Path.cwd().joinpath('env').joinpath('sos.env')
env_path.parent.mkdir(exist_ok=True)
load_dotenv(find_dotenv(str(env_path)))


class SDownLoadImage(SUserInfo):
    def __init__(self, token, webid, log_filename):
        super().__init__(token, webid, log_filename)
        self.my_headers = self.headers
        self.my_headers['content-type'] = 'application/json'
        self.my_headers['referer'] = f'https://{self.web_host}/aigenerator'

    def feed_image(self, image_id, image_url):
        self.getLogger().info(f'点赞图片')
        url = f"https://{self.api_host}/gateway/sd-api/gen/tool/imageFeedback/save"
        payload = json.dumps({
            "outputId": image_id,
            "imageId": image_url,
            "imageComment": 1,
            "cid": self.webid
        })
        response = requests.request("POST", url, headers=self.my_headers, data=payload)
        self.getLogger().info(f'点赞图片结果: {response.text}')

    def share_image(self, i_en):
        self.getLogger().info(f'分享图片')
        url = f"https://{self.api_host}/api/www/log/acceptor/f"
        payload = json.dumps({
            "uuid": self.uuid,
            "cid": self.webid,
            "ct": time.time(),
            "pageUrl": f"https://{self.api_host}/aigenerator",
            "ua": self.my_headers['user-agent'],
            "e": "tool.canvas.share",
            "var": {
                "share_id": f"https://{self.api_host}/aigenerator/share?p={str(i_en, 'utf-8')}"
            }
        })
        response = requests.request("POST", url, headers=self.my_headers, data=payload)
        self.getLogger().info(f'分享图片结果: {response.text}')

    def download(self, share_image=False, feed_image=False):
        data = self.getImageList(pageSize=1)
        self.getLogger().info(f'查询图片生成历史结果: {data}')

        if len(data) > 0:
            for img in data:
                if img['images'] is not None:
                    for oneImg in img['images']:
                        image_id = oneImg['outputId']
                        image_url = oneImg['imageId']
                        generate_Id = oneImg['generateId']
                        i = f'g={generate_Id}&i={image_id}'
                        i_en = base64.b64encode(i.encode("utf-8"))
                        self.getLogger().info(f'下载图片')
                        url = f"https://{self.api_host}/api/www/log/acceptor/f"
                        payload = json.dumps({
                            "uuid": self.uuid,
                            "cid": self.webid,
                            "ct": time.time(),
                            "pageUrl": f"https://{self.api_host}/aigenerator",
                            "ua": self.my_headers['user-agent'],
                            "e": "tool.canvas.download",
                            "var": {
                                "image_id": image_id,
                                "type": "original"
                            }
                        })
                        response = requests.request("POST", url, headers=self.my_headers, data=payload)
                        self.getLogger().info(f'下载图片结果: {response.text}')
                        downloadImageCount = {}
                        if img['param']['mixModels'] is not None:
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
                                    self.getLogger().error(f'更新下载次数失败: {e}')

                                for user_uuid, model_list in downloadImageCount.items():
                                    try:
                                        for modelId, model in model_list.items():
                                            try:
                                                query = DownLoadImageStatistics.select().where(DownLoadImageStatistics.user_uuid == user_uuid,
                                                                                               DownLoadImageStatistics.modelId == modelId,
                                                                                               DownLoadImageStatistics.day == self.day)
                                                if query.exists():
                                                    downloadImageCount = int(query.dicts().get().get('downloadImageCount'))
                                                    DownLoadImageStatistics.update(
                                                        downloadImageCount=downloadImageCount + model['count'],
                                                        timestamp=datetime.datetime.now()
                                                    ).where(DownLoadImageStatistics.user_uuid == user_uuid,
                                                            DownLoadImageStatistics.modelId == modelId,
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

                        if share_image:
                            self.share_image(i_en)

                        if feed_image:
                            self.feed_image(image_id, image_url)


if __name__ == '__main__':
    users = get_users(cookie_name="shakker_cookie", usertoken_name="liblibai_usertoken")
    for user in users:
        sDownLoadImage = SDownLoadImage(user['usertoken'], user['webid'], f'/mitmproxy/logs/SDownLoadImage_{os.getenv("RUN_OS_KEY")}.log')
        try:
            sDownLoadImage.download(share_image=True, feed_image=True)
        except Exception as e:
            sDownLoadImage.getLogger().error(f"nickname：{sDownLoadImage.userInfo['nickname']} SDownLoadImage，{traceback.format_exc()}")
