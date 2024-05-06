import json
import re

from furl import furl

from toutiao.toutiaoUserInfo import ToutiaoUserInfo
from utils.logger import logger
from db.toutiao import Task as ToutiaoTask, Account as ToutiaoAccount
from db.toutiao_jisu import Task, Account, JOIN, Jd, Iad
from toutiao.jisu.userInfo import UserInfo
from utils.utils import convert_cookies_to_dict, send_message
from liblibart.ql import ql_env

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


def save_toutiao_data(flow):
    params = furl(flow.request.path)
    # 删除不合法的header头信息
    for header_key in flow.request.headers.keys():
        if not is_legal_header_name(header_key.encode('ascii')):
            del flow.request.headers[header_key]
    response_json = flow.response.text
    user_data = json.loads(response_json)
    if user_data["message"] != "success":
        return
    if "data" in user_data:
        ToutiaoUserInfo(dict(flow.request.headers.items()), user_data["data"],
                        dict(zip(params.args.keys(), params.args.values())))
        userName = user_data["data"]["name"]
        user_data["data"]["name"] = userName + "(已成功接入头条系统)"
        flow.response.text = json.dumps(user_data)


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


def save_toutiao_task_data(flow, type):
    headers = dict(flow.request.headers)
    cookie = convert_cookies_to_dict(headers['cookie'])
    session_key = cookie['sessionid']
    host = flow.request.host
    path = flow.request.path
    full_url = flow.request.url
    method = flow.request.method
    # 请求中body的内容，有一些http会把请求参数放在body里面，可通过此方法获取，返回字典类型
    body = flow.request.get_text()
    queryTask = ToutiaoTask.select(ToutiaoTask, ToutiaoAccount).join(ToutiaoAccount, JOIN.LEFT_OUTER,
                                                                     on=(
                                                                                 ToutiaoTask.session_key == ToutiaoAccount.session_key)) \
        .where(ToutiaoTask.session_key == session_key, ToutiaoTask.type == type)
    if queryTask.exists():
        ToutiaoTask.update(
            session_key=session_key,
            host=host,
            path=path,
            url=full_url,
            method=method,
            header=json.dumps(headers),
            body=body,
            type=type,
        ).where(ToutiaoTask.session_key == session_key, ToutiaoTask.type == type).execute()
        result = queryTask.dicts().get()
        send_message("用户【{}】更新任务【{}】成功".format(result.get('name'), type))
    else:
        ToutiaoTask.create(
            session_key=session_key,
            host=host,
            path=path,
            url=full_url,
            method=method,
            header=json.dumps(headers),
            body=body,
            type=type,
        )
        queryTask = ToutiaoTask.select(ToutiaoTask, ToutiaoAccount).join(ToutiaoAccount, JOIN.LEFT_OUTER,
                                                                         on=(
                                                                                     ToutiaoTask.session_key == ToutiaoAccount.session_key)) \
            .where(ToutiaoTask.session_key == session_key, ToutiaoTask.type == type)
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
        pin_exist = False
        value = f"pin={pin};wskey={wskey}"
        jd_wscks = ql_env.search("JD_WSCK")
        for jd_wsck in jd_wscks:
            if jd_wsck['status'] == 0 and pin in jd_wsck['pin']:
                pin_exist = True
                ql_env.update(value, jd_wsck['name'], jd_wsck['id'])
                logger.info("更新京东用户【{}】信息".format(pin))
                send_message("更新京东用户【{}】信息".format(pin))
                break
        if not pin_exist:
            ql_env.add("JD_WSCK", value)
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
