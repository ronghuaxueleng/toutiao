'''
用户信息
'''
import json

from db.toutiao import Account
from utils.logger import logger
from utils.utils import send_message, convert_cookies_to_dict


class ToutiaoUserInfo:
    def __init__(self, header, userInfo, params):
        self.header = header
        self.userInfo = userInfo
        self.params = params
        self.initUser()

    def initUser(self):
        user_id = self.userInfo["user_id"]
        name = self.userInfo["name"]
        sec_user_id = self.userInfo["user_id"]
        cookie = convert_cookies_to_dict(self.header.get('cookie'))
        session_key = cookie['sessionid']
        query = Account.select().where(Account.user_id == user_id)
        if query.exists():
            Account.update(
                user_id=user_id,
                name=name,
                sec_user_id=sec_user_id,
                session_key=session_key,
                userInfo=json.dumps(dict(self.userInfo)),
                headers=json.dumps(self.header),
                commonParams=json.dumps(self.params)
            ).where(Account.user_id == user_id).execute()
            logger.info("更新用户【{}】信息".format(name))
        else:
            Account.insert(
                user_id=user_id,
                name=name,
                sec_user_id=sec_user_id,
                session_key=session_key,
                userInfo=json.dumps(dict(self.userInfo)),
                headers=json.dumps(self.header),
                commonParams=json.dumps(self.params)
            ).execute()
            logger.info("添加用户【{}】信息".format(name))
            send_message("添加用户【{}】信息".format(name))