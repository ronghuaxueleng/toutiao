# -*- coding: utf-8 -*-
from ql import ql_env


def get_to_run_users():
    to_run_users = ql_env.get_by_id(511)
    return to_run_users['data']['value']


if __name__ == '__main__':
    to_run_users = get_to_run_users()
    print(to_run_users)
