# -*- coding: utf-8 -*-
import datetime
import json
import os

from UserInfo import UserInfo
from CookieUtils import save_to_suanlibuzu_users

current_day_json_path = os.path.join(os.path.split(os.path.realpath(__file__))[0], '..', 'config', 'current_day.json')
checkpointIds_path = os.path.join(os.path.split(os.path.realpath(__file__))[0], '..', 'config', 'checkpointIds.json')
gen_params_path = os.path.join(os.path.split(os.path.realpath(__file__))[0], '..', 'config', 'gen_params.json')


class Base(UserInfo):
    def __init__(self, token, webid, filename=None):
        super().__init__(token, webid, filename)
        self.gen_param = {
            "checkpointId": 2016037,
            "generateType": 1,
            "frontCustomerReq": {
                "windowId": "",
                "tabType": "txt2img",
                "conAndSegAndGen": "gen"
            },
            "text2img": {
                "prompt": ",1girl,chinese new year,photorealistic,photography,jewelry,indoors,red sweater,simple background,tassel,lantern,make up,Chinese fan,hair ornament,dress ",
                "negativePrompt": "text,chinese red packet,leg,(worst quality, low quality:2), monochrome, zombie,overexposure, watermark,text,bad anatomy,bad hand,extra hands,extra fingers,too many fingers,fused fingers,bad arm,distorted arm,extra arms,fused arms,extra legs,missing leg,disembodied leg,extra nipples, detached arm, liquid hand,inverted hand,disembodied limb, small breasts, loli, oversized head,extra body,completely nude,",
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
                json.dump(self.gen_param, fp)
        else:
            with open(gen_params_path, 'r') as fp:
                self.gen_param = json.load(fp)

        self.checkpointIds = [2016037, 2321317]
        if not os.path.exists(checkpointIds_path):
            with open(checkpointIds_path, 'w') as fp:
                json.dump(self.checkpointIds, fp)
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
        with open(current_day_json_path, 'w') as to_run_users_json:
            json.dump(self.current_day, to_run_users_json, indent=4)

    def load_from_current_day(self):
        if os.path.exists(current_day_json_path):
            with open(current_day_json_path, 'r') as to_run_users_json:
                current_day = json.load(to_run_users_json)
                return current_day['current_day']
        return None
