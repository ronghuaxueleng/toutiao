# -*- coding: utf-8 -*-
import datetime
import json
import traceback

from liblibart.RunningInfo import RunningInfo
from liblibart.SRunningInfo import RunningInfo as SRunningInfo
from liblibart.ql import ql_env


def save_to_suanlibuzu_users(suanlibuzu_users, is_shakker=False):
    if is_shakker:
        query = SRunningInfo.select().where(SRunningInfo.id == 1)
        if query.exists():
            SRunningInfo.update(
                suanlibuzu_users=json.dumps(suanlibuzu_users),
                timestamp=datetime.datetime.now()
            ).where(SRunningInfo.id == 1).execute()
        else:
            SRunningInfo.insert(
                id=1,
                suanlibuzu_users=json.dumps(suanlibuzu_users),
                timestamp=datetime.datetime.now()
            ).execute()
    else:
        query = RunningInfo.select().where(RunningInfo.id == 1)
        if query.exists():
            RunningInfo.update(
                suanlibuzu_users=json.dumps(suanlibuzu_users),
                timestamp=datetime.datetime.now()
            ).where(RunningInfo.id == 1).execute()
        else:
            RunningInfo.insert(
                id=1,
                suanlibuzu_users=json.dumps(suanlibuzu_users),
                timestamp=datetime.datetime.now()
            ).execute()


def load_from_suanlibuzu_users(is_shakker=False):
    if is_shakker:
        query = SRunningInfo.select().where(SRunningInfo.id == 1)
        if query.exists():
            info = SRunningInfo.get(SRunningInfo.id == 1)
            return json.loads(info.suanlibuzu_users)
        else:
            return []
    else:
        query = RunningInfo.select().where(RunningInfo.id == 1)
        if query.exists():
            info = RunningInfo.get(RunningInfo.id == 1)
            return json.loads(info.suanlibuzu_users)
        else:
            return []


def save_to_run_users(to_run_users, is_shakker=False):
    if is_shakker:
        query = SRunningInfo.select().where(SRunningInfo.id == 1)
        if query.exists():
            SRunningInfo.update(
                to_run_users=json.dumps(to_run_users),
                timestamp=datetime.datetime.now()
            ).where(SRunningInfo.id == 1).execute()
        else:
            SRunningInfo.insert(
                id=1,
                to_run_users=json.dumps(to_run_users),
                timestamp=datetime.datetime.now()
            ).execute()
    else:
        query = RunningInfo.select().where(RunningInfo.id == 1)
        if query.exists():
            RunningInfo.update(
                to_run_users=json.dumps(to_run_users),
                timestamp=datetime.datetime.now()
            ).where(RunningInfo.id == 1).execute()
        else:
            RunningInfo.insert(
                id=1,
                to_run_users=json.dumps(to_run_users),
                timestamp=datetime.datetime.now()
            ).execute()


def load_from_run_users(is_shakker=False):
    if is_shakker:
        query = SRunningInfo.select().where(SRunningInfo.id == 1)
        if query.exists():
            info = SRunningInfo.get(SRunningInfo.id == 1)
            return json.loads(info.to_run_users)
        else:
            return []
    else:
        query = RunningInfo.select().where(RunningInfo.id == 1)
        if query.exists():
            info = RunningInfo.get(RunningInfo.id == 1)
            return json.loads(info.to_run_users)
        else:
            return []


def save_checkpoints(checkpoints, is_shakker=False):
    if is_shakker:
        query = SRunningInfo.select().where(SRunningInfo.id == 1)
        if query.exists():
            SRunningInfo.update(
                checkpoints=json.dumps(checkpoints),
                timestamp=datetime.datetime.now()
            ).where(SRunningInfo.id == 1).execute()
        else:
            SRunningInfo.insert(
                id=1,
                checkpoints=json.dumps(checkpoints),
                timestamp=datetime.datetime.now()
            ).execute()
    else:
        query = RunningInfo.select().where(RunningInfo.id == 1)
        if query.exists():
            RunningInfo.update(
                checkpoints=json.dumps(checkpoints),
                timestamp=datetime.datetime.now()
            ).where(RunningInfo.id == 1).execute()
        else:
            RunningInfo.insert(
                id=1,
                checkpoints=json.dumps(checkpoints),
                timestamp=datetime.datetime.now()
            ).execute()


def load_from_checkpoints(is_shakker=False):
    if is_shakker:
        query = SRunningInfo.select().where(SRunningInfo.id == 1)
        if query.exists():
            info = SRunningInfo.get(SRunningInfo.id == 1)
            return json.loads(info.checkpoints)
        else:
            return {}
    else:
        query = RunningInfo.select().where(RunningInfo.id == 1)
        if query.exists():
            info = RunningInfo.get(RunningInfo.id == 1)
            return json.loads(info.checkpoints)
        else:
            return {}


def save_to_runcheckpoints(to_runcheckpoints, is_shakker=False):
    if is_shakker:
        query = SRunningInfo.select().where(SRunningInfo.id == 1)
        if query.exists():
            SRunningInfo.update(
                to_runcheckpoints=json.dumps(to_runcheckpoints),
                timestamp=datetime.datetime.now()
            ).where(SRunningInfo.id == 1).execute()
        else:
            SRunningInfo.insert(
                id=1,
                to_runcheckpoints=json.dumps(to_runcheckpoints),
                timestamp=datetime.datetime.now()
            ).execute()
    else:
        query = RunningInfo.select().where(RunningInfo.id == 1)
        if query.exists():
            RunningInfo.update(
                to_runcheckpoints=json.dumps(to_runcheckpoints),
                timestamp=datetime.datetime.now()
            ).where(RunningInfo.id == 1).execute()
        else:
            RunningInfo.insert(
                id=1,
                to_runcheckpoints=json.dumps(to_runcheckpoints),
                timestamp=datetime.datetime.now()
            ).execute()


def load_from_to_runcheckpoints(is_shakker=False):
    if is_shakker:
        query = SRunningInfo.select().where(SRunningInfo.id == 1)
        if query.exists():
            info = SRunningInfo.get(SRunningInfo.id == 1)
            return json.loads(info.to_runcheckpoints)
        else:
            return []
    else:
        query = RunningInfo.select().where(RunningInfo.id == 1)
        if query.exists():
            info = RunningInfo.get(RunningInfo.id == 1)
            return json.loads(info.to_runcheckpoints)
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
                        user['expirationDate'] = value['expirationDate']
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
