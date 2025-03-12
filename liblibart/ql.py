# -*- coding: utf-8 -*-
import base64
import json

from qlapi import qlenv

config_base64 = "eyJob3N0Ijoid3d3LnJvbmdodWF4dWVsZW5nLnNpdGUiLCJwb3J0IjoiNTY4MCIsIkNsaWVudElEIjoiODctUXZrNEhrLW5iIiwiQ2xpZW50U2VjcmV0Ijoibi1meHNlcWFRUkU2RjNyQ2xLbzBGMXJsIn0="
ql_config = str(base64.b64decode(config_base64), 'utf-8')
json_config = json.loads(ql_config)
ql_env = qlenv(
    url=json_config['host'],  # 青龙面板IP地址(不包含http://)
    port=json_config['port'],  # 青龙面板端口
    client_id=json_config['ClientID'],  # 青龙面板openapi登录用户名
    client_secret=json_config['ClientSecret'],  # 青龙面板openapi登录密码
)