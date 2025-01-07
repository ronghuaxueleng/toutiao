# -*- coding: utf-8 -*-
import requests


def refreshToken(client_id, refresh_token, client_secret):
    url = "https://login.microsoftonline.com/common/oauth2/v2.0/token"

    payload = f'client_id={client_id}&grant_type=refresh_token&refresh_token={refresh_token}&client_secret={client_secret}'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': 'fpc=AuynGZaRD-lFtjpqAhrAdKBjsc4rAQAAAEubDt8OAAAA'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)


def authorizationCode(client_id, code, client_secret, redirect_uri):
    url = "https://login.microsoftonline.com/common/oauth2/v2.0/token"

    payload = f'client_id={client_id}&code={code}&redirect_uri={redirect_uri}&client_secret={client_secret}&grant_type=authorization_code&scope=https%3A%2F%2Foutlook.office.com%2FIMAP.AccessAsUser.All%20https%3A%2F%2Foutlook.office.com%2FPOP.AccessAsUser.All%20https%3A%2F%2Foutlook.office.com%2FSMTP.Send%20https%3A%2F%2Foutlook.office.com%2FUser.Read%20https%3A%2F%2Foutlook.office.com%2FMail.Read%20offline_access'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': 'fpc=AuynGZaRD-lFtjpqAhrAdKBjsc4rAQAAANnLDt8OAAAA; stsservicecookie=estsfd; x-ms-gateway-slice=estsfd'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)
