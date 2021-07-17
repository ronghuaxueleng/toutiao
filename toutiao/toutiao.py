import json
import re

from furl import furl

from toutiao.db import Task, Account, JOIN
from toutiao.userInfo import UserInfo
from toutiao.tasks import userTasks
from toutiao.utils import convert_cookies_to_dict, send_message

is_legal_header_name = re.compile(rb'[^:\s][^:\r\n]*').fullmatch

'''
存储用户请求数据
'''

users = {}


def save_request_data(flow):
    params = furl(flow.request.path)
    # 删除不合法的header头信息
    for header_key in flow.request.headers.keys():
        if not is_legal_header_name(header_key.encode('ascii')):
            del flow.request.headers[header_key]
    headers_json = json.dumps(dict(flow.request.headers.items()))
    response_json = flow.response.text
    user_data = json.loads(response_json)
    if user_data["message"] != "success":
        return
    if "data" in user_data:
        UserInfo(headers_json, user_data["data"], params)
        userName = user_data["data"]["name"]
        user_data["data"]["name"] = userName + "(已成功接入头条系统)"
        flow.response.text = json.dumps(user_data)


def save_task_data(flow, type):
    headers = dict(flow.request.headers)
    cookie = convert_cookies_to_dict(headers['cookie'])
    session_key = cookie['sessionid']
    host = flow.request.host
    path = flow.request.path
    full_url = flow.request.url
    method = flow.request.method
    # 请求中body的内容，有一些http会把请求参数放在body里面，可通过此方法获取，返回字典类型
    body = flow.request.get_text()
    queryTask = Task.select(Task, Account).join(Account, JOIN.LEFT_OUTER,
                                               on=(Task.session_key == Account.session_key)) \
        .where(Task.session_key == session_key, Task.type == type)
    if queryTask.exists():
        Task.update(
            session_key=session_key,
            host=host,
            path=path,
            url=full_url,
            method=method,
            header=json.dumps(headers),
            body=body,
            type=type,
        ).where(Task.session_key == session_key, Task.type == type).execute()
    else:
        Task.create(
            session_key=session_key,
            host=host,
            path=path,
            url=full_url,
            method=method,
            header=json.dumps(headers),
            body=body,
            type=type,
        )
        queryTask = Task.select(Task, Account).join(Account, JOIN.LEFT_OUTER,
                                                    on=(Task.session_key == Account.session_key)) \
            .where(Task.session_key == session_key, Task.type == type)
        result = queryTask.dicts().get()
        userTasks.addJob(result)
        send_message("用户【{}】添加任务【】成功".format(result.get('name'), type))
