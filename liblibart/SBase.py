# -*- coding: utf-8 -*-
import datetime
import json
import os

from SUserInfo import SUserInfo
from CookieUtils import save_to_suanlibuzu_users

current_day_json_path = '/mitmproxy/config/s_current_day.json'

class SBase(SUserInfo):
    def __init__(self, token, webid, bl_uid, filename=None):
        super().__init__(token, webid, bl_uid, filename)
        self.prompt = "1girl,masterpiece,best quality,4k,1girl,solo,realistic,jewelry,necklace,brown eyes,earrings,lips,looking at viewer,long hair BREAK\nwhite shirt,short sleeves,bracelet,black hair,smile,closed mouth,facing viewer,\nmakeup,fashion model,picture-perfect face,flowing hair,(full body:1.5),shiny skin,(masterpiece, top quality),master piece,professional artwork,famous artwork,(realistic,photorealistic:1.37),HDR,UHD,8K,ultra realistic 8k cg,8K,32k,HD,"
        self.negativePrompt = "EasyNegativeV2,(badhandv4:1.2),(worst quality, low quality, cgi, bad eye, worst eye, illustration, cartoon),deformed,distorted,disfigured,poorly drawn,bad anatomy,wrong anatomy,(normal quality:2),lowres,bad anatomy,bad hands,normal quality,((monochrome)),((grayscale)),easynegative,paintings,sketches,,EasyNegative, EasyNegativeV2, ng_deepnegative_v1_75t, worst quality, low quality,bad-hands-5,BadHandsV5,illustration, 3d, 2d, painting, cartoons, sketch,text, error, missing fingers,verybadimagenegative_v1.3, Bybadartist,badhandv4, lowres, bad anatomy, bad hands, ((monochrome)), ((grayscale)) watermark,nsfw,EasyNegative, EasyNegativeV2, ng_deepnegative_v1_75t, worst quality, low quality,bad-hands-5,BadHandsV5"
        self.gen_param = {
            "source": 3,
            "adetailerEnable": 1,
            "mode": 1,
            "projectData": {
                "style": "",
                "baseType": 1,
                "presetBaseModelId": "null",
                "baseModel": "null",
                "loraModels": [],
                "width": 1024,
                "height": 1024,
                "isFixedRatio": "true",
                "hires": "true",
                "count": 1,
                "prompt": self.prompt,
                "negativePrompt": "",
                "presetNegativePrompts": [
                    "common",
                    "bad_hand"
                ],
                "samplerMethod": "15",
                "samplingSteps": 30,
                "seedType": "0",
                "seedNumber": "",
                "vae": "22541",
                "cfgScale": 7,
                "clipSkip": 2,
                "controlnets": [],
                "changed": "true",
                "modelGroupCoverUrl": "null",
                "checkpoint": {
                    "name": "my_checkpoint_xx",
                    "versionId": 1531927,
                    "modelId": 1827982,
                    "versionName": "v1",
                    "uuid": "7a0ea24618aa4fc8804e66d37b7b4dfb",
                    "tagV2Ids": [
                        100031,
                        100054,
                        100070,
                        100026,
                        100028,
                        100029,
                        100069
                    ],
                    "baseType": "SD 1.5",
                    "modelType": "Checkpoint",
                    "runCount": 0,
                    "userAvatar": "https://models-online-persist.shakker.cloud/img/44d172fc437d490f87bfc261258fb183/d8040a5eab6ae654eb53f1cf4793466c3f50679692cf3782f5fa067dcfce0da6.png",
                    "userName": "ronghua",
                    "imageUrl": "https://liblibai-online.liblib.cloud/img/b8b05c9cf1c1487b802fba02dbfb128d/b8b5fce330f93e6b937f96f5d2ea5152214a8325806c025abb3b7ce3b27a2aa9.png",
                    "vipUsed": 0,
                    "weight": "null",
                    "modelUuid": "de7debe397b54451b36b59b2af8daaab",
                    "triggerWord": "1girl",
                    "remark": "null",
                    "ngPrompt": "nsfw,EasyNegative, EasyNegativeV2, ng_deepnegative_v1_75t, worst quality, low quality,bad-hands-5,BadHandsV5"
                },
                "hiresOptions": {
                    "enabled": "true",
                    "scale": 1.33,
                    "upscaler": "15",
                    "strength": 0.5,
                    "steps": 20,
                    "width": 768,
                    "height": 768
                },
                "modelCfgScale": 7,
                "addOns": [
                    {
                        "name": "Fix Face",
                        "value": 0,
                        "mergeMode": 1,
                        "edge": -4
                    },
                    {
                        "name": "Fix Hand",
                        "value": 1,
                        "mergeMode": 1,
                        "edge": -4
                    }
                ],
                "mode": 1,
                "isSimpleMode": "false",
                "generateType": "normal",
                "renderWidth": 1024,
                "renderHeight": 1024,
                "samplerMethodName": "DPM++ SDE"
            },
            "vae": 22541,
            "checkpointId": 1531927,
            "additionalNetwork": [],
            "adetailerList": [
                {
                    "adetailerModelVerId": 0,
                    "prompt": "",
                    "negativePrompt": "",
                    "detection": {
                        "threshold": 0.3,
                        "maskMinAreaRatio": 0,
                        "maskMaxAreaRatio": 1
                    },
                    "maskPreprocessing": {
                        "maskXOffset": 0,
                        "maskYOffset": 0,
                        "maskScaling": -4,
                        "maskMergeMode": 1
                    },
                    "inpainting": {
                        "maskBlur": 4,
                        "denoisingStrength": 0.4,
                        "onlyMasked": "true",
                        "onlyMaskedPaddingPixels": 32,
                        "separateWH": "false",
                        "separateSteps": "true",
                        "adetailerSteps": 25,
                        "separateCFGScale": "false",
                        "separateNoiseMultiplier": "false",
                        "restoreFacesAfterADetailer": "false"
                    }
                },
                {
                    "adetailerModelVerId": 1,
                    "prompt": "",
                    "negativePrompt": "",
                    "detection": {
                        "threshold": 0.3,
                        "maskMinAreaRatio": 0,
                        "maskMaxAreaRatio": 1
                    },
                    "maskPreprocessing": {
                        "maskXOffset": 0,
                        "maskYOffset": 0,
                        "maskScaling": -4,
                        "maskMergeMode": 1
                    },
                    "inpainting": {
                        "maskBlur": 4,
                        "denoisingStrength": 0.4,
                        "onlyMasked": "true",
                        "onlyMaskedPaddingPixels": 32,
                        "separateWH": "false",
                        "separateSteps": "true",
                        "adetailerSteps": 25,
                        "separateCFGScale": "false",
                        "separateNoiseMultiplier": "false",
                        "restoreFacesAfterADetailer": "false"
                    }
                }
            ],
            "generateType": 1,
            "text2img": {
                "width": 768,
                "height": 768,
                "prompt": self.prompt,
                "negativePrompt": self.negativePrompt,
                "samplingMethod": "15",
                "samplingStep": 30,
                "batchSize": 1,
                "batchCount": 1,
                "cfgScale": 7,
                "clipSkip": 2,
                "seed": -1,
                "tiling": 0,
                "seedExtra": 0,
                "restoreFaces": 0,
                "hiResFix": 1,
                "extraNetwork": [],
                "promptRecommend": "true",
                "hiResFixInfo": {
                    "upscaler": 15,
                    "upscaleBy": 1.33,
                    "resizeWidth": 1024,
                    "resizeHeight": 1024
                },
                "hiresSteps": 20,
                "denoisingStrength": 0.5
            },
            "cid": "1725802989955hopmyqxc"
        }

        dt = datetime.datetime.now()
        self.today = dt.strftime("%Y%m%d")
        self.current_day = {
            'current_day': self.today
        }
        current_day = self.load_from_current_day()
        if current_day is None:
            self.save_to_current_day()
        if current_day != self.today:
            self.save_to_current_day()
            save_to_suanlibuzu_users([], True)

    def save_to_current_day(self):
        with open(current_day_json_path, 'w') as current_day:
            json.dump(self.current_day, current_day, indent=4)

    def load_from_current_day(self):
        if os.path.exists(current_day_json_path):
            with open(current_day_json_path, 'r') as a:
                current_day = json.load(a)
                return current_day['current_day']
        return None
