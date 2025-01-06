# -*- coding: utf-8 -*-
import email as email_reader
import random
import ssl
from email.header import decode_header
from enum import Enum
import requests
import imaplib

def get_access_token_from_refresh_token(refresh_token, client_id):
    headers = {
        'Host': 'login.microsoftonline.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
    }
    data = {
        "client_id": client_id,
        "refresh_token": refresh_token,
        "grant_type": "refresh_token"
    }
    rr = requests.post("https://login.microsoftonline.com/common/oauth2/v2.0/token", headers=headers, data=data)

    if rr.json().get("error") is None:
        return {"code": 0, "access_token": rr.json()["access_token"], "refresh_token": rr.json()["refresh_token"]}
    if rr.json().get("error_description").find("User account is found to be in service abuse mode") != -1:
        return {"code": 1, "message": "account was blocked or wrong username, password, refresh_token, client_id"}
    return {"code": 1, "message": "get access token is wrong"}

def imap_authenticate_with_oauth2(username, access_token):
    auth_string = f"user={username}\1auth=Bearer {access_token}\1\1"
    mail = imaplib.IMAP4_SSL("outlook.office365.com")
    mail.authenticate("XOAUTH2", lambda x: auth_string)
    return mail

def read_mail(email, access_token):
    mail = imap_authenticate_with_oauth2(email, access_token)

    mail.list()
    mail.select("inbox")
    status, messages = mail.search(None, 'ALL')

    messages = messages[0].split()
    for mail_id in messages:
        status, msg_data = mail.fetch(mail_id, '(RFC822)')
        email_msg = msg_data[0][1].decode('utf-8')
        print(email_msg)
    print("done")

def example():
    email = "cadet-morass-edible@outlook.com"
    client_id = "f76823ba-5521-4b17-8f71-d286178502bf"
    refresh_token = "M.C560_BAY.0.U.-Cv5wWkc0vatEXhjdgMX8PCVWs8wprkmilYOsT66iFBb*kiNPca8LhxgyK8WjUmF6QCbNOlYIsdB!*3EqV5TX*Mb2wM3pSOXpOxYhZ33xX!!63l4c01T43mKZZJd!sFO4*krlR6DGKucB7VXl2AV1ht*KuHbfajNxYWrC91joCreP5vy*13et0C63HM8b1OTT7z9eUhyjMy3dtc!cgqBBYGmmtR3K3Uq1*zMEk0vTrY2jo8i9KrK0JV2vZRoi7JBXOV0SNIe0crADwxwiVm*5G2vf9c0pLGq4u7fTMM95xKYE2fC*0AX6fbI1Is95e7b22AYE4Brqyst4tQrQ79pe83debzHDQS414Spl*K91qeo4TdQ78GAbqtGjFZEoxW!6LoaL!bOWQT!S7q4DYz!mzgYODjkUTX7MrP7a4gD3Zvy06BRENsiDcN8ir5D1QI8VXZ76on9Hyl8a6dUlKkpKundgWcnvDlatDLHK4kug9kUJ"
    access_token = "EwBYA+l3BAAUcDnR9grBJokeAHaUV8R3+rVHX+IAAQuo6rwX2SHz9RweZB5fsVyaV3G3yzvi9Ybz28MCfrOSgpqM/QeK7cPqmp0auh3t9aX2/KEAmbGTJHen3bsb+1TpI3CAB48iM+fVb+vRf+EjdC/JCtDOfUnWzNxoRpR7L9wzn0lcTihG47+K9UhbCmSQfp5lr7aWds2cdCGXQb+JAQuW5yhdDH5MhbykURxmtVutBR7SBDxakUS4vTmSXQ3uSEuul1dDtTxN2LMdgZe6YxWCtm8Dt+tXc6H9hx2ZzY3M+z0R8WG8V/11m0/XcFnex6gtv3p8uYYChSoEd4Z4/fK8uIcpewVwfdCOTCTmevkdc8StfvzfjX+jlGx1tk0QZgAAEJyQplv91ZZSGhgD7Z13qWMgAhgRLoM+U894myv99CfM4WAt3FndwPhAMXFIUa8eylJp2i1OLDMS5aQ1icmFuQE182ngexpb5IpJ4sxSO51OlnEQz8jqWi18ig37sFahMoLJAJbWb8NL7FGM8tz05uXpXq2Qfq8YNtqMjD0VtSewSqBYHH7rf5H5fH1tSXf8oOC+MDNC/+syv3U5qd69YzvaU29/GCVTs7VQffpzkjcA7/uVcqvrJzircJ2eQUhoOsD5qvOA+UptmpaqUrQ1YQW1cyMTOAuhkXRnGbsZG2yLWeyr9IwkHPuRl2MwGjn/10nyvqE49UVoBSHJkwU93YfkqY+ouMEuHUE8p7gZsRfX1jeK3xnT6BnFtW3+UoVVAuwGiQtpkvu7llZ9C6tejRCZqVx4QNbkWMo+BOoHCuTN/hvG3GXAmtVbf65VASOvrSb1T0LW3UG+83t9Ev4grwxuiiFbZFboIfbT04jSWEDQMOLhFMTyQDueUNKslwAdgrONrlt6p2istvou8e8ND3WoVorA5ZvhZL9k1OOFmPXzdssnyxPpj4+BvVDpPFFa1w7flW0qnVMLZJu7ZMyCLoqzofYrSfKlDAdvu7K/AtlSnsoC6BxKgFdo/bZheIZjF/xZYvkqQMXUb+e8DRYK99vJcBdUNmtcaKSr/5dphYHwBI1HSeuyOit9TUEEg8lRHZO7A5XvBOf4eyqiLddSa3UsyLE1NRNC948cU5kf2FFkF/l/Ag=="
    # token = get_access_token_from_refresh_token(refresh_token, client_id)
    read_mail(email, access_token)

# 调用示例
example()
