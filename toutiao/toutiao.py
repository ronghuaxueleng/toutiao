import json
import re

from furl import furl

from utils.logger import logger
from toutiao.db import Task, Account, JOIN, Jd, Iad, Abb
from toutiao.userInfo import UserInfo
from utils.utils import convert_cookies_to_dict, send_message

is_legal_header_name = re.compile(rb'[^:\s][^:\r\n]*').fullmatch

'''
存储用户请求数据
'''

users = {}
cookieReg = re.compile('pin=(?P<pin>\S+?);.*?wskey=(?P<wskey>\S+?);')
abbUserReg = re.compile('lu_name\s=\s"(?P<username>.*?)"')
abbUserIdReg = re.compile('uid=(?P<uid>\d+)')
abbPhoneReg = re.compile('<div\s+class="phone">(?P<phone>.*?)</div>')

abbMoneyReg = re.compile('<div\s+class="money">(?P<money>.*?)</div>')
abbAliNameReg = re.compile('<input(?:\s+\S+)+\s+placeholder="输入姓名"\s+value="(?P<aliname>.*?)">')
abbAlipayReg = re.compile('<input(?:\s+\S+)+\s+placeholder="输入支付宝账号"\s+value="(?P<alipay>.*?)">')


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
        result = queryTask.dicts().get()
        send_message("用户【{}】更新任务【{}】成功".format(result.get('name'), type))
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
        send_message("用户【{}】添加任务【{}】成功".format(result.get('name'), type))


def save_jd_pin(flow):
    headers_json = dict(flow.request.headers.items())
    cookie = headers_json.get("cookie")
    regMatch = cookieReg.match(cookie)
    cookies = regMatch.groupdict()
    pin = cookies.get("pin")
    wskey = cookies.get("wskey")
    if pin is not None and wskey is not None:
        query = Jd.select().where(Jd.pin == pin)
        if query.exists():
            Jd.update(
                pin=pin,
                wskey=wskey,
            ).where(Jd.pin == pin).execute()
            logger.info("更新京东用户【{}】信息".format(pin))
            send_message("更新京东用户【{}】信息".format(pin))
        else:
            Jd.insert(
                pin=pin,
                wskey=wskey,
            ).execute()
            logger.info("添加京东用户【{}】信息".format(pin))
            send_message("添加京东用户【{}】信息".format(pin))


def save_ad(source, web_url):
    query = Iad.select().where(Iad.source == source)
    if not query.exists():
        Iad.insert(
            source=source,
            web_url=web_url,
        ).execute()
        logger.info("添加广告【{}】信息".format(source))
        send_message("添加广告【{}】信息\n下载地址：{}".format(source, web_url))
    else:
        Iad.update(
            source=source,
            web_url=web_url,
        ).where(Iad.source == source).execute()
        logger.info("更新广告【{}】信息".format(source))
        send_message("更新广告【{}】信息\n下载地址：{}".format(source, web_url))


def save_abb_header(flow):
    body = flow.response.text
    userMatch = abbUserReg.search(body)
    phoneMatch = abbPhoneReg.search(body)
    userIdMatch = abbUserIdReg.search(body)
    if userMatch is not None and userIdMatch is not None and phoneMatch is not None:
        usernames = userMatch.groupdict()
        username = usernames.get("username")
        userIds = userIdMatch.groupdict()
        userId = userIds.get("uid")
        phones = phoneMatch.groupdict()
        phone = phones.get("phone")
        headers_json = json.dumps(dict(flow.request.headers.items()))
        query = Abb.select().where(Abb.uid == userId)
        if not query.exists():
            Abb.insert(
                uid=userId,
                nick=username,
                header=headers_json,
                phone=phone
            ).execute()
            logger.info("添加用户【{}】信息".format(username))
            send_message("添加用户【{}】信息".format(username), "爱步宝")
        else:
            Abb.update(
                phone=phone,
                header=headers_json,
            ).where(Abb.uid == userId).execute()
            logger.info("更新用户【{}】信息".format(username))
            send_message("更新用户【{}】信息".format(username), "爱步宝")
