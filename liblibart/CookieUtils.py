# -*- coding: utf-8 -*-
import json
import os

from liblibart.ql import ql_env

suanlibuzu_users_json_path = os.path.join(os.path.split(os.path.realpath(__file__))[0], '..', 'config',
                                          'suanlibuzu_users.json')
to_run_users_json_path = os.path.join(os.path.split(os.path.realpath(__file__))[0], '..', 'config', 'to_run_users.json')


def save_to_suanlibuzu_users(suanlibuzu_users):
    with open(suanlibuzu_users_json_path, 'w') as to_run_users_json:
        json.dump(suanlibuzu_users, to_run_users_json, indent=4)


def load_from_suanlibuzu_users():
    if os.path.exists(suanlibuzu_users_json_path):
        with open(suanlibuzu_users_json_path, 'r') as to_run_users_json:
            return json.load(to_run_users_json)
    return []


def save_to_run_users(to_run_users):
    with open(to_run_users_json_path, 'w') as to_run_users_json:
        json.dump(to_run_users, to_run_users_json, indent=4)


def load_from_run_users():
    if os.path.exists(to_run_users_json_path):
        with open(to_run_users_json_path, 'r') as to_run_users_json:
            return json.load(to_run_users_json)
    return []


def get_users(get_all=False, exclude_user=None, cookie_name="liblib_cookie", usertoken_name="usertoken"):
    if exclude_user is None:
        exclude_user = []
    users = []
    try:
        liblib_cookies = ql_env.search(cookie_name)
        for liblib_cookie in liblib_cookies:
            if get_all or liblib_cookie['status'] == 0:
                values = json.loads(liblib_cookie['value'])
                user = {
                    'id': liblib_cookie['id'],
                }
                for value in values:
                    if value['name'] == usertoken_name:
                        user['usertoken'] = value['value']
                    if value['name'] == 'webid':
                        user['webid'] = value['value']
                    if value['name'] == '_bl_uid':
                        user['_bl_uid'] = value['value']
                if user['usertoken'] not in exclude_user:
                    users.append(user)
    except Exception as e:
        print(e)
    return users
