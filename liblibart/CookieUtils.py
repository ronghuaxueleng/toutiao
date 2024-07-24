# -*- coding: utf-8 -*-
import json
import os

from liblibart.ql import ql_env

to_run_users_json_path = os.path.join(os.path.split(os.path.realpath(__file__))[0], '..', 'config', 'to_run_users.json')


def save_to_run_users(to_run_users):
    with open(to_run_users_json_path, 'w') as to_run_users_json:
        json.dump(to_run_users, to_run_users_json, indent=4)


def load_from_run_users():
    if os.path.exists(to_run_users_json_path):
        with open(to_run_users_json_path, 'r') as to_run_users_json:
            return json.load(to_run_users_json)
    return []


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
