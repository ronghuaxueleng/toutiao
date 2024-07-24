# -*- coding: utf-8 -*-
import json

from ql import ql_env


def get_users(get_all=False, exclude_user=None):
    if exclude_user is None:
        exclude_user = []
    liblib_cookies = ql_env.search("liblib_cookie")
    users = []
    for liblib_cookie in liblib_cookies:
        if get_all or liblib_cookie['status'] == 0:
            values = json.loads(liblib_cookie['value'])
            user = {
                'id': liblib_cookie['id'],
            }
            for value in values:
                if value['name'] == 'usertoken':
                    user['usertoken'] = value['value']
                if value['name'] == 'webid':
                    user['webid'] = value['value']
            if user['usertoken'] not in exclude_user:
                users.append(user)
    return users