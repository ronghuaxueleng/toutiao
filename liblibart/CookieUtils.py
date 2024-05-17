# -*- coding: utf-8 -*-
import json

from liblibart.ql import ql_env


def get_users():
    liblib_cookies = ql_env.search("liblib_cookie")
    users = []
    for liblib_cookie in liblib_cookies:
        if liblib_cookie['status'] == 0:
            values = json.loads(liblib_cookie['value'])
            user = {
                'id': liblib_cookie['id'],
            }
            for value in values:
                if value['name'] == 'usertoken':
                    user['usertoken'] = value['value']
                if value['name'] == 'webid':
                    user['webid'] = value['value']
            users.append(user)
    return users