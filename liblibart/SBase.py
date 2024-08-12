# -*- coding: utf-8 -*-
import datetime
import json
import os

from liblibart.SUserInfo import SUserInfo
from liblibart.CookieUtils import save_to_suanlibuzu_users

current_day_json_path = os.path.join(os.path.split(os.path.realpath(__file__))[0], '..', 'config', 's_current_day.json')
checkpointIds_path = os.path.join(os.path.split(os.path.realpath(__file__))[0], '..', 'config', 's_checkpointIds.json')
gen_params_path = os.path.join(os.path.split(os.path.realpath(__file__))[0], '..', 'config', 's_gen_params.json')


class SBase(SUserInfo):
    def __init__(self, token, webid, filename=None):
        super().__init__(token, webid, filename)
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
                "width": 384,
                "height": 768,
                "isFixedRatio": "true",
                "hires": "true",
                "count": 1,
                "prompt": "1girl,solo,realistic,jewelry,necklace,brown eyes,earrings,lips,looking at viewer,long hair BREAK\nwhite shirt,short sleeves,bracelet,black hair,smile,closed mouth,facing viewer,\nmakeup,fashion model,picture-perfect face,flowing hair,(full body:1.5),shiny skin,(masterpiece, top quality),master piece,professional artwork,famous artwork,(realistic,photorealistic:1.37),HDR,UHD,8K,ultra realistic 8k cg,8K,32k,HD,",
                "negativePrompt": "EasyNegativeV2,(badhandv4:1.2),(worst quality, low quality, cgi, bad eye, worst eye, illustration, cartoon),deformed,distorted,disfigured,poorly drawn,bad anatomy,wrong anatomy,(normal quality:2),lowres,bad anatomy,bad hands,normal quality,((monochrome)),((grayscale)),easynegative,paintings,sketches,",
                "presetNegativePrompts": [
                    "common",
                    "bad_hand",
                    "real_portrait",
                    "bad_image",
                    "anime"
                ],
                "samplerMethod": "8",
                "samplingSteps": 30,
                "seedType": "0",
                "seedNumber": "",
                "vae": "22541",
                "cfgScale": 7,
                "clipSkip": 2,
                "controlnets": [],
                "hiresOptions": {
                    "enabled": "false",
                    "scale": 1.33,
                    "upscaler": "15",
                    "strength": 0.5,
                    "steps": 20,
                    "width": 384,
                    "height": 768
                },
                "changed": "true",
                "modelGroupCoverUrl": "null",
                "checkpoint": {
                    "name": "my_checkpoint_00000",
                    "versionId": 1511727,
                    "modelId": 1810480,
                    "versionName": "v1",
                    "uuid": "a2ff8a38cb194c339391362adc681631",
                    "baseType": "SD 1.5",
                    "modelType": "Checkpoint",
                    "runCount": 0,
                    "userAvatar": "https://lh3.googleusercontent.com/a/ACg8ocKX_-zG28CmwqlFavPDjDVrOOS8DlFVWsioe2rkTl8JgNSAyeKu=s96-c",
                    "userName": "ronghuahaha",
                    "imageUrl": "https://liblibai-online.vibrou.com/img/02749e73219936808ff45d707b2d01cf/eeeea8451ea05ec8d4f17f3b8333f45f9314287cccfce8d3e66838c1d8ea85c7.png",
                    "vipUsed": 0,
                    "weight": "null",
                    "modelUuid": "25e6c8796cba48d1a7dea267731ae5ad",
                    "triggerWord": "1girl",
                    "remark": "null",
                    "ngPrompt": "nsfw,EasyNegative, EasyNegativeV2, ng_deepnegative_v1_75t, worst quality, low quality,bad-hands-5,BadHandsV5"
                },
                "addOns": [
                    {
                        "name": "Fix Face",
                        "value": 0,
                        "mergeMode": 1,
                        "edge": -4
                    }
                ],
                "seed": 3363921491,
                "mode": 1,
                "isSimpleMode": "false",
                "generateType": "normal",
                "renderWidth": 384,
                "renderHeight": 768,
                "samplerMethodName": "DPM++ SDE"
            },
            "vae": 22541,
            "checkpointId": 1511727,
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
                }
            ],
            "generateType": 1,
            "text2img": {
                "width": 384,
                "height": 768,
                "prompt": "1girl,masterpiece,best quality,4k,1girl,solo,realistic,jewelry,necklace,brown eyes,earrings,lips,looking at viewer,long hair BREAK\nwhite shirt,short sleeves,bracelet,black hair,smile,closed mouth,facing viewer,\nmakeup,fashion model,picture-perfect face,flowing hair,(full body:1.5),shiny skin,(masterpiece, top quality),master piece,professional artwork,famous artwork,(realistic,photorealistic:1.37),HDR,UHD,8K,ultra realistic 8k cg,8K,32k,HD,",
                "negativePrompt": "EasyNegativeV2,(badhandv4:1.2),(worst quality, low quality, cgi, bad eye, worst eye, illustration, cartoon),deformed,distorted,disfigured,poorly drawn,bad anatomy,wrong anatomy,(normal quality:2),lowres,bad anatomy,bad hands,normal quality,((monochrome)),((grayscale)),easynegative,paintings,sketches,,EasyNegative, EasyNegativeV2, ng_deepnegative_v1_75t, worst quality, low quality,bad-hands-5,BadHandsV5,illustration, 3d, 2d, painting, cartoons, sketch,text, error, missing fingers,verybadimagenegative_v1.3, Bybadartist,badhandv4, lowres, bad anatomy, bad hands, ((monochrome)), ((grayscale)) watermark,nsfw,EasyNegative, EasyNegativeV2, ng_deepnegative_v1_75t, worst quality, low quality,bad-hands-5,BadHandsV5",
                "samplingMethod": "8",
                "samplingStep": 30,
                "batchSize": 1,
                "batchCount": 1,
                "cfgScale": 7,
                "clipSkip": 2,
                "seed": -1,
                "tiling": 0,
                "seedExtra": 0,
                "restoreFaces": 0,
                "hiResFix": 0,
                "extraNetwork": [],
                "promptRecommend": "true"
            },
            "cid": "1723355030078utiwqxrz"
        }

        if not os.path.exists(gen_params_path):
            with open(gen_params_path, 'w') as fp:
                json.dump(self.gen_param, fp, indent=4)
        else:
            with open(gen_params_path, 'r') as fp:
                self.gen_param = json.load(fp)

        self.checkpointIds = [1511727]
        if not os.path.exists(checkpointIds_path):
            with open(checkpointIds_path, 'w') as fp:
                json.dump(self.checkpointIds, fp, indent=4)
        else:
            with open(checkpointIds_path, 'r') as fp:
                self.checkpointIds = json.load(fp)
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
            save_to_suanlibuzu_users([])

    def save_to_current_day(self):
        with open(current_day_json_path, 'w') as current_day:
            json.dump(self.current_day, current_day, indent=4)

    def load_from_current_day(self):
        if os.path.exists(current_day_json_path):
            with open(current_day_json_path, 'r') as a:
                current_day = json.load(a)
                return current_day['current_day']
        return None
