# -*- coding: utf-8 -*-
import base64

from peewee import MySQLDatabase


def get_conn(database='bGlibGli'):
    user = 'cm9vdA=='
    password = 'MTIzNDU2Nzg='
    host = 'MTkyLjE0NC4yMTUuMjE4'
    port = 'MzMwNjA='
    return MySQLDatabase(str(base64.b64decode(database), 'utf-8'),
                         user=str(base64.b64decode(user), 'utf-8'),
                         password=str(base64.b64decode(password), 'utf-8'),
                         host=str(base64.b64decode(host), 'utf-8'),
                         port=int(str(base64.b64decode(port), 'utf-8'))
                         )