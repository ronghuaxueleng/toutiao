import re

import requests
from hyper import HTTP20Connection


def get_sample(url, headers):
    return requests.get(url, headers=headers)


def post_sample(url, headers, data=None):
    return requests.post(url, headers=headers, data=data)


def get(host, path, headers):
    return request(host, 'GET', path, headers)


def post(host, path, headers, data=None):
    return request(host, 'POST', path, headers, data)


def request(host, method, path, headers=None, body=None):
    if headers is None:
        headers = {}
    headers['Accept'] = '*/*'
    headers['Connection'] = 'keep-alive'
    c = HTTP20Connection(host)
    response = c.request(method, path, headers=headers, body=body)
    resp = c.get_response(response)
    return resp.read().decode('utf-8')


def convert_cookies_to_dict(cookies, delimiter="; |;|, |,"):
    cookies = dict([l.split("=", 1) for l in re.split(delimiter, cookies)])
    return cookies


def send_message(content):
    token = '653a27049c144b80936a55a7600541cf'
    title = '今日头条极速版'
    url = 'http://pushplus.hxtrip.com/send?token=' + token + '&title=' + title + '&content=' + content
    requests.get(url)


if __name__ == '__main__':
    print(convert_cookies_to_dict(
        "gd=20210113, PIXIEL_RATIO=3, FRM=new, n_mh=5Ho88Y9x8PnG2gZlMXiZs6cPCspJVlnR4t2RoO1GPxQ, uid_tt=dc70dcaf296cf0ef2ffefe5b413789be, uid_tt_ss=dc70dcaf296cf0ef2ffefe5b413789be, sid_tt=74faabce5e1d6eccde51388fe56ffdb7, sessionid=74faabce5e1d6eccde51388fe56ffdb7, sessionid_ss=74faabce5e1d6eccde51388fe56ffdb7, WIN_WH=360_522, ssr_tz=Asia/Shanghai, ssr_sbh__=24, sid_guard=74faabce5e1d6eccde51388fe56ffdb7%7C1609552413%7C5180666%7CWed%2C+03-Mar-2021+00%3A57%3A59+GMT, UM_distinctid=176cd227956fc-0bbab6e9aec9b-450c3405-1fa400-176cd22795b93, d_ticket=89dcff96241fec82ddaee374379f3d6599c69, odin_tt=b07475c40ea1373a3b2c3c64b4393f130e1024b3e5e99112b91d879fd9a2f5938053a3bc981269599c588d33f3031895, passport_csrf_token=34067122c05173a7dcffa8977511846a, passport_csrf_token_default=34067122c05173a7dcffa8977511846a, install_id=2023515197541988, ttreq=1$8583db968663d6bcd44256b418b7a0e99a426578"))
