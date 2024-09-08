# -*- coding: utf-8 -*-
import datetime
import json
import os

from liblibart.UserInfo import UserInfo
from liblibart.CookieUtils import save_to_suanlibuzu_users

current_day_json_path = '/mitmproxy/config/current_day.json'
checkpointIds_path = '/mitmproxy/config/checkpointIds.json'
gen_params_path = '/mitmproxy/config/gen_params.json'


class Base(UserInfo):
    def __init__(self, token, webid, filename=None):
        super().__init__(token, webid, filename)
        self.gen_param = {
            "checkpointId": 2531860,
            "generateType": 1,
            "frontCustomerReq": {
                "windowId": "",
                "tabType": "txt2img",
                "conAndSegAndGen": "gen"
            },
            "text2img": {
                "prompt": ",1girl,solo,realistic,jewelry,necklace,brown eyes,earrings,lips,looking at viewer,long hair BREAK\nwhite shirt,short sleeves,bracelet,black hair,smile,closed mouth,facing viewer,\nmakeup,fashion model,picture-perfect face,flowing hair,(full body:1.5),shiny skin,(masterpiece, top quality),master piece,professional artwork,famous artwork,(realistic,photorealistic:1.37),HDR,UHD,8K,ultra realistic 8k cg,8K,32k,HD,",
                "negativePrompt": "EasyNegativeV2,(badhandv4:1.2),(worst quality, low quality, cgi, bad eye, worst eye, illustration, cartoon),deformed,distorted,disfigured,poorly drawn,bad anatomy,wrong anatomy,(normal quality:2),lowres,bad anatomy,bad hands,normal quality,((monochrome)),((grayscale)),easynegative,paintings,sketches,",
                "extraNetwork": "",
                "samplingMethod": 24,
                "samplingStep": 30,
                "width": 512,
                "height": 768,
                "imgCount": 1,
                "cfgScale": 5,
                "seed": -1,
                "seedExtra": 0,
                "hiResFix": 0,
                "restoreFaces": 0,
                "tiling": 0,
                "clipSkip": 2
            },
            "adetailerEnable": 1,
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
                        "maskScaling": 4,
                        "maskMergeMode": 1
                    },
                    "inpainting": {
                        "maskBlur": 4,
                        "denoisingStrength": 0.4,
                        "onlyMasked": True,
                        "onlyMaskedPaddingPixels": 32,
                        "separateWH": False,
                        "separateSteps": True,
                        "adetailerSteps": 25,
                        "separateCFGScale": False,
                        "separateNoiseMultiplier": False,
                        "restoreFacesAfterADetailer": False
                    }
                }
            ],
            "additionalNetwork": [],
            "taskQueuePriority": 1
        }

        if not os.path.exists(gen_params_path):
            with open(gen_params_path, 'w') as fp:
                json.dump(self.gen_param, fp, indent=4)
        else:
            with open(gen_params_path, 'r') as fp:
                self.gen_param = json.load(fp)

        self.checkpointIds = [2016037]
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
