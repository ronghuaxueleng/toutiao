# -*- coding: utf-8 -*-
import re
import time
import uuid
from random import random

import requests

sourceURL = "https://graph.qq.com/oauth2.0/login_jump"

sessionMap = {}


class liblibQQLogin:
    def __init__(self, session_id=None):
        self.sess = None
        self.js_ver = '24091915'
        if session_id is None:
            self.newSession()
            self.session_id = str(uuid.uuid1())
            sessionMap[self.session_id] = self.sess
        else:
            self.session_id = session_id
            self.sess = sessionMap[self.session_id]

    def newSession(self):
        self.sess = requests.Session()
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/130.0.0.0 Safari/537.36',
        }
        self.sess.headers.update(headers)
        return

    def genQRToken(self, qrsig):
        e = 0
        for i in range(0, len(qrsig)):
            e += (e << 5) + ord(qrsig[i])
        qrtoken = (e & 2147483647)
        return str(qrtoken)

    def qrShow(self):
        url = 'https://xui.ptlogin2.qq.com/cgi-bin/xlogin'
        params = {
            "appid": 716027609,
            "daid": 383,
            "style": 33,
            "login_text": "登录",
            "hide_title_bar": 1,
            "hide_border": 1,
            "target": "self",
            "s_url": sourceURL,
            "pt_3rd_aid": 102049234,
            "pt_feedback_link": "https://support.qq.com/products/77942?customInfo=.appid102049234",
            "theme": 2,
            "verify_theme": ""
        }
        resp = self.sess.get(url, params=params, timeout=1000)
        pattern = r'imgcache\.qq\.com/ptlogin/ver/(\d+)/js'
        try:
            self.js_ver = re.search(pattern, resp.content).group(1)
        except:
            pass
        self.sess.headers.update({'Referer': url})
        url = 'https://ssl.ptlogin2.qq.com/ptqrshow'
        params = {
            "appid": 716027609,
            "e": 2,
            "l": "M",
            "s": 3,
            "d": 72,
            "v": 4,
            "t": '%.17f' % (random()),
            "daid": 383,
            "pt_3rd_aid": 102049234,
            "u1": sourceURL
        }
        resp = self.sess.get(url, params=params, timeout=1000)
        return resp

    def qrLogin(self, id, qrsig, login_sig):
        while True:
            url = 'https://ssl.ptlogin2.qq.com/ptqrlogin'
            params = {
                "u1": sourceURL,
                "ptqrtoken": self.genQRToken(qrsig),
                "ptredirect": 0,
                "h": 1,
                "t": 1,
                "g": 1,
                "from_ui": 1,
                "ptlang": 2052,
                "action": '0-0-%d' % (time.time() * 1000),
                "js_ver": self.js_ver,
                "js_type": 1,
                "login_sig": login_sig,
                "pt_uistyle": 40,
                "aid": 716027609,
                "daid": 383,
                "pt_3rd_aid": 102049234,
                "o1vId": "531f114a7808a5cfef819c6f7a04c98d",
                "pt_js_version": "v1.57.0"
            }
            res = self.sess.get(url, params=params, timeout=1000)
            print(res)
            print(res.text)
            time.sleep(2)
