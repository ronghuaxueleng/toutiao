# -*- coding: utf-8 -*-
"""
# @Author  : RanKe
# @Time    : 2024/10/18 22:16
# @File      : get_mail_info.py
# @Desc   :
"""

import imaplib
import email
import requests
from email.utils import parsedate_to_datetime
from email.header import decode_header, make_header


def get_access_token(client_id, refresh_token):
    url = 'https://login.microsoftonline.com/common/oauth2/v2.0/token'
    data = {
        'client_id': client_id,
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
    }
    response = requests.post(url, data=data)
    result_status = response.json().get('error')
    if result_status is not None:
        print(result_status)
        return [False, f"邮箱状态异常：{result_status}"]
    else:
        new_access_token = response.json()['access_token']
        return [True, new_access_token]


def generate_auth_string(email_name, access_token):
    auth_string = f"user={email_name}\1auth=Bearer {access_token}\1\1"
    print(auth_string)
    return auth_string


def get_mail_info(email_name, access_token):
    result_list = []
    mail = imaplib.IMAP4_SSL('outlook.live.com')
    mail.authenticate('XOAUTH2', lambda x: generate_auth_string(email_name, access_token))
    mail.select('inbox')  #选择收件箱
    # mail.select('Junk')  #选择垃圾箱
    result, data = mail.search(None, 'ALL')
    if result == "OK":
        mail_ids = sorted(data[0].split(), reverse=True)
        last_mail_id_list = mail_ids[:3]
        for last_mail_id in last_mail_id_list:
            result, msg_data = mail.fetch(last_mail_id, "(RFC822)")
            body = ""
            if result == 'OK':
                # 解析邮件内容
                raw_email = msg_data[0][1]
                email_message = email.message_from_bytes(raw_email)
                subject = str(make_header(decode_header(email_message['SUBJECT'])))  # 主题
                mail_from = str(make_header(decode_header(email_message['From']))).replace('<', '(').replace('>',
                                                                                                             ')')  # 发件人
                mail_to = str(make_header(decode_header(email_message['To']))).replace('<', '(').replace('>',
                                                                                                         ')')  # 收件人
                mail_dt = parsedate_to_datetime(email_message['Date']).strftime("%Y-%m-%d %H:%M:%S")  # 收件时间
                if email_message.is_multipart():
                    for part in email_message.walk():
                        content_type = part.get_content_type()
                        if content_type in ["text/html"]:
                            payload = part.get_payload(decode=True)
                            body += payload.decode('utf-8', errors='ignore')

                else:
                    body = email_message.get_payload(decode=True).decode('utf-8', errors='ignore')
                res_dict = {"subject": subject, "mail_from": mail_from, "mail_to": mail_to, "mail_dt": mail_dt,
                            "body": body}
                result_list.append(res_dict)
            else:
                res_dict = {"error_key": "解析失败", "error_msg": "邮件信息解析失败，请联系管理员优化处理！"}
                return res_dict
        return result_list
    else:
        res_dict = {"error_key": "登录失败", "error_msg": "登录失败，账号异常!"}
        return res_dict


# https://login.microsoftonline.com/common/oauth2/v2.0/authorize?client_id=f76823ba-5521-4b17-8f71-d286178502bf&scope=IMAP.AccessAsUser.All%20POP.AccessAsUser.All%20SMTP.Send%20User.Read%20Mail.Read%20offline_access&response_type=code&redirect_uri=https://login.microsoftonline.com/common/oauth2/nativeclient&prompt=login

if __name__ == '__main__':
    client_id = 'f76823ba-5521-4b17-8f71-d286178502bf'
    email_name = 'cadet-morass-edible@outlook.com'
    refresh_token = 'M.C560_SN1.0.U.-CsPoPdeVgJOgQOX6W3TpIouJ7pHTrEyYKaiv5bNbHvrIQAcJm2M7Rcg1EcJKmgPOUwUuLD2yYn06q4pCC5FY2Kl0lCGK4n6xFRjXtK95fGp9RmxvthAkMkWfIScKB98ERo3a4wYoB3IpV5MdSdeb!lxaFfv7jxuFOHuQbqYygfjXCLhDZ4xKjMfogewERX1SdBO1aTj01qnX7DvwCBO52i5iuUGwrZstgxo53KMihjcHHea!mVwyK7L1z2L5Lx72IWyFOVHJwHgau0iaQLRxNlgC2D*5IbbwYHT*1J78KzHPSP7K0KEN0zIXdb738iRxQtB0O9GHj!ac9fnbrEcg6oDTLWqGZ8qHP3tEe184h*z6ATLmmliil18A3D7VpcNKrNeYAQ!BNFk3Cdi5YFVBHfr5VI2zJ2wpVEyJ0rCkyLHicrpt*tIGUXqfuy3fEccyWg$$'
    access_token = 'EwBYA+l3BAAUcDnR9grBJokeAHaUV8R3+rVHX+IAAcz4DhHgkK1gull4DlRvRQCrrNQ1vykb5d0+RkZnMWP+itR2fNXmdpLvV1bU5zVlqQ0k1FvCNIRa1NJ+ZXdluyJk4xD68whjROghH1RD9yhz03AghJfSLeBLjpOu+PBUJkLAyFPF0XIjBbOC+wmLDkmALR6srtwlgjOcezXgpfzlzZK13rbXrJKygnyYs97Tp05kEt2ZTNi33ZA0yCs2w4Iv72+zy4EfaOhkL2sHvlrVwVn+N6bSNhvPUZ2kqKlHc8Wh8iG06Y8IQ8Ad+JDbnj8Jj/pO0GEHSh7Nqu1griI/g3x5r6uLh9B8nS6BLZdIMO1uxqZiMFr47UDfjFKZTFsQZgAAEAxykFEywMtz+JKDXuEJzEogAl9CNa4wSj0kyj30EiK7mfnQv02lkE0qA+kJd8jF72E+ECR4PiHqay/uCvO9/nSJcKlcinvbfSlo3jS0OvnDeJ/zIBCkTZ1tTBv6xjc9b5ksO3qxr+OSUPUHIY1DR761m/U2ZORw3afDmhxWu8JJuuzDxkD5fEFSWfqYOluxu0Wc0T7/sNWG5Fwg0ME/9DM5rsiWa7mRdCReGPH7WhCbS6uQgW+AEv6aGGMOBm7EPa9HHO+Yi/lvccUuyhAy4aYHME5Nu+N849HVo7q2eUyIsY0uCx3Ef8KMZzCVAGC/Uwpri9T00JWjfkLp5ItfUxzEKSeNOBqsF1s7Pbs89r3ZeZrZ556vkG7YmPEahZrnpyDMQ+vpe8CCrEAVOUjB1qus0rwJ99kTG9QGNKX0VQY59+Ya59brpdr9AX7f4ECGHkiKyb6fdvSln+R6vkEf/dMy7saizDvALEVhSZddT8iNqFjGQQGFFtvJW94zQfWf5iJCYvDvf/RFqyA4aAL6+LRFpDqKKBkHmxXVuBjQ/uKSUYxAIgXgE2X8dnyOe88QFFNQhURrozG7v4eYy2qKf/Qv6asDPquphXex9WeY5RVRFq/7nPFYqSeg25V/Ipy6kud7NIVQ3p9iHZ4Qa+vYaH6AzkReGlL+/Bqq75BKfIuvhi3CLyaDRbQYDnMZnz+SdJyHuIdgI9I3ZimXhEJ/P4cnac78Ga99cG7ARRioGEaY4ZV/Ag=='
    mail_info_res = get_mail_info(email_name, access_token)
    if isinstance(mail_info_res, list):
        for mail_info in mail_info_res:
            print(f"邮件主题：{mail_info['subject']}")
            print(f"发件时间：{mail_info['mail_dt']}")
            print(f"发件人：{mail_info['mail_from']}")
            print(f"收件人：{mail_info['mail_to']}")
            print(f"邮件正文：{mail_info['body']}")