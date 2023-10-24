import json
import requests
from bs4 import BeautifulSoup

from others.qinglong import QingLong

url = "https://dfldata.cc/home.php?mod=spacecp&ac=credit&showcredit=1"

payload = {}
headers = {
  'authority': 'dfldata.cc',
  'sec-ch-ua': '"Chromium";v="21", " Not;A Brand";v="99"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"',
  'upgrade-insecure-requests': '1',
  'dnt': '1',
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
  'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
  'sec-fetch-site': 'same-origin',
  'sec-fetch-mode': 'navigate',
  'sec-fetch-user': '?1',
  'sec-fetch-dest': 'document',
  'referer': 'https://dfldata.cc/',
  'accept-language': 'zh-CN,zh;q=0.9',
  'cookie': 'LKzz_2132_saltkey=NZ63y6rj; LKzz_2132_lastvisit=1698110795; LKzz_2132_seccodecSAhbLEoG7ij=155.511ab8e2490b115b1c; LKzz_2132_ulastactivity=4670JxKR4EJdsn4IpMXWFjyDNCQeBx2bGiZ2ThOgvVGJHUotBMHZ; LKzz_2132_auth=552dE1wN5l6zS%2FqxtAwwqx7k7A0XMlGX4tceDpzlHz7%2FgvJcXTwr6Qp6J%2F2lXfm5q8%2FBDD1yatnZGXBv97WujTxI7g; LKzz_2132_lastcheckfeed=55035%7C1698114425; LKzz_2132_nofavfid=1; LKzz_2132_sid=B8d1f1; LKzz_2132_lip=101.40.69.182%2C1698114425; LKzz_2132_onlineusernum=223; LKzz_2132_sendmail=1; LKzz_2132_checkpm=1; LKzz_2132_lastact=1698128335%09misc.php%09patch; LKzz_2132_lastact=1698128407%09home.php%09spacecp; LKzz_2132_sid=B8d1f1'
}

response = QingLong().run('LXAPK_COOKIE')
if response['code'] == 200:
  cookies = response['data']
  for cookie in cookies:
    try:
      headers['Cookie'] = cookie['value']
      response = requests.request("POST", url, headers=headers, data=payload)
      text = response.text
      soup = BeautifulSoup(text, "lxml")
      vwmy = soup.select('.vwmy')
      print(vwmy[0].text)
    except Exception as e:
      print(e)
      token = '258f84f44f0246c38bffb7d03733a825'
      url = 'http://www.pushplus.plus/send'
      title = "deepfacelab中文网"
      content = "登录失败"
      requests.post(url, data={"token": token, "title": title, "content": content, "channel": "cp", "webhook": "4680"})

