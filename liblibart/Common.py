# -*- coding: utf-8 -*-
from ql import ql_env

id = 511


def get_to_run_users():
    to_run_users = ql_env.get_by_id(id)
    return to_run_users['data']['value']


def update_to_run_users(to_run_users):
    ql_env.update(to_run_users, id=id)


if __name__ == '__main__':
    to_run_users = get_to_run_users()
    print(to_run_users)
