# -*- coding: utf-8 -*-
import base64
import json

from qlapi import qlenv

config_base64 = "eyJ1cmwiOiJxaW5nbG9uZy5yb25naHVheHVlbGVuZy50b3AiLCJDbGllbnRJRCI6Ijg3LVF2azRIay1uYiIsIkNsaWVudFNlY3JldCI6Im4tZnhzZXFhUVJFNkYzckNsS28wRjFybCJ9"
ql_config = str(base64.b64decode(config_base64), 'utf-8')
json_config = json.loads(ql_config)
ql_env = qlenv(
    url=json_config['url'],  # 青龙面板IP地址(不包含http://)
    client_id=json_config['ClientID'],  # 青龙面板openapi登录用户名
    client_secret=json_config['ClientSecret'],  # 青龙面板openapi登录密码
)