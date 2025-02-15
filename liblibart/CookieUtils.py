# -*- coding: utf-8 -*-
import datetime
import json
import traceback

from DbUtils import get_redis_conn
from ql import ql_env

r = get_redis_conn()


def save_to_suanlibuzu_users(suanlibuzu_users, is_shakker=False):
    if is_shakker:
        r.set("s_suanlibuzu_users", json.dumps(suanlibuzu_users))
    else:
        r.set("suanlibuzu_users", json.dumps(suanlibuzu_users))


def load_from_suanlibuzu_users(is_shakker=False):
    if is_shakker:
        suanlibuzu_users = r.get('s_suanlibuzu_users')
    else:
        suanlibuzu_users = r.get('suanlibuzu_users')
    if suanlibuzu_users is not None:
        return json.loads(suanlibuzu_users)
    else:
        return []


def save_to_run_users(to_run_users, is_shakker=False):
    if is_shakker:
        r.set("s_to_run_users", json.dumps(to_run_users))
    else:
        r.set("to_run_users", json.dumps(to_run_users))


def load_from_run_users(is_shakker=False):
    if is_shakker:
        to_run_users = r.get('s_to_run_users')
    else:
        to_run_users = r.get('to_run_users')
    if to_run_users is not None:
        return json.loads(to_run_users)
    else:
        return []


def save_checkpoints(checkpoints, is_shakker=False):
    if is_shakker:
        r.set("s_checkpoints", json.dumps(checkpoints))
    else:
        r.set("checkpoints", json.dumps(checkpoints))


def load_from_checkpoints(is_shakker=False):
    if is_shakker:
        checkpoints = r.get('s_checkpoints')
    else:
        checkpoints = r.get('checkpoints')
    if checkpoints is not None:
        return json.loads(checkpoints)
    else:
        return {}


def save_otherloras(checkpoints, is_shakker=False):
    if is_shakker:
        r.set("s_other_loras", json.dumps(checkpoints))
    else:
        r.set("other_loras", json.dumps(checkpoints))


def load_from_otherloras(is_shakker=False):
    if is_shakker:
        checkpoints = r.get('s_other_loras')
    else:
        checkpoints = r.get('other_loras')
    if checkpoints is not None:
        return json.loads(checkpoints)
    else:
        return []


def save_othercheckpoints(checkpoints, is_shakker=False):
    if is_shakker:
        r.set("s_other_checkpoints", json.dumps(checkpoints))
    else:
        r.set("other_checkpoints", json.dumps(checkpoints))


def load_from_othercheckpoints(is_shakker=False):
    if is_shakker:
        checkpoints = r.get('s_other_checkpoints')
    else:
        checkpoints = r.get('other_checkpoints')
    if checkpoints is not None:
        return json.loads(checkpoints)
    else:
        return []


def save_to_runcheckpoints(to_runcheckpoints, is_shakker=False):
    if is_shakker:
        r.set('s_to_runcheckpoints', json.dumps(to_runcheckpoints))
    else:
        r.set('to_runcheckpoints', json.dumps(to_runcheckpoints))


def load_from_to_runcheckpoints(is_shakker=False):
    if is_shakker:
        to_run_checkpoints = r.get('s_to_runcheckpoints')
    else:
        to_run_checkpoints = r.get('to_runcheckpoints')
    if to_run_checkpoints is not None:
        return json.loads(to_run_checkpoints)
    else:
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
                        try:
                            user['expirationDate'] = value['expirationDate']
                        except Exception as e:
                            pass
                    if value['name'] == 'webid':
                        user['webid'] = value['value']
                    if value['name'] == '_bl_uid':
                        user['_bl_uid'] = value['value']
                try:
                    if user['usertoken'] not in exclude_user:
                        users.append(user)
                except:
                    print(liblib_cookie['remarks'])
    except Exception as e:
        print(traceback.format_exc())
    return users
