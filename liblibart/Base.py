# -*- coding: utf-8 -*-
from liblibart.UserInfo import UserInfo


class Base(UserInfo):
    def __init__(self, token, webid):
        super().__init__(token, webid)
        self.gen_param = {
            "checkpointId": 650910,
            "generateType": 1,
            "frontCustomerReq": {
                # "frontId": self.frontId,
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
            "adetailerEnable": 0,
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