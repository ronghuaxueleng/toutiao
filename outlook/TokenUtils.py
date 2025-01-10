# -*- coding: utf-8 -*-
import datetime
import json

import requests

from outlook.OutlookInfo import OutlookInfo


def refreshToken(client_id, refresh_token, client_secret):
    url = "https://login.microsoftonline.com/common/oauth2/v2.0/token"

    payload = f'client_id={client_id}&grant_type=refresh_token&refresh_token={refresh_token}&client_secret={client_secret}'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)


def authorizationCode(client_id, code, client_secret, redirect_uri):
    url = "https://login.microsoftonline.com/common/oauth2/v2.0/token"

    payload = f'client_id={client_id}&code={code}&redirect_uri={redirect_uri}&client_secret={client_secret}&grant_type=authorization_code&scope=https%3A%2F%2Foutlook.office.com%2FIMAP.AccessAsUser.All%20https%3A%2F%2Foutlook.office.com%2FPOP.AccessAsUser.All%20https%3A%2F%2Foutlook.office.com%2FSMTP.Send%20https%3A%2F%2Foutlook.office.com%2FUser.Read%20https%3A%2F%2Foutlook.office.com%2FMail.Read%20offline_access'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.text


def getToken(client_id, code):
    info = OutlookInfo.get(OutlookInfo.client_id == client_id)
    client_secret = info.client_secret
    redirect_uri = f'http://localhost:5000/outlook-callBack?client_id={client_id}'
    result = authorizationCode(client_id, code, client_secret, redirect_uri)
    if "error" not in result:
        res = json.loads(result)
        refresh_token = res['refresh_token']
        OutlookInfo.update(
            refresh_token=refresh_token,
            timestamp=datetime.datetime.now()
        ).where(OutlookInfo.client_id == client_id).execute()
    return result


def genLoginUrl():
    urls = []
    outlooks = OutlookInfo.select().execute()
    for outlook in outlooks:
        if outlook.refresh_token is None:
            client_id = outlook.client_id
            redirect_uri = f'http://localhost:5000/outlook-callBack?client_id={client_id}'
            url = f'https://login.microsoftonline.com/common/oauth2/v2.0/authorize?client_id={client_id}&scope=IMAP.AccessAsUser.All%20POP.AccessAsUser.All%20SMTP.Send%20User.Read%20Mail.Read%20offline_access&response_type=code&redirect_uri={redirect_uri}&prompt=login'
            urls.append(url)
    return json.dumps(urls)


if __name__ == '__main__':
    urls = genLoginUrl()
    print(urls)
