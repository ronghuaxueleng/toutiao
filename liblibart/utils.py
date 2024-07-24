import requests


def send_message(content, title='今日头条极速版'):
    token = '258f84f44f0246c38bffb7d03733a825'
    url = 'http://www.pushplus.plus/send'
    requests.post(url, data={"token": token, "title": title, "content": content, "channel": "cp", "webhook": "4680"})


