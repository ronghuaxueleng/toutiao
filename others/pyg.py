import requests

session = requests.session()

url = "https://www.chinapyg.com/member.php?mod=logging&action=login&loginsubmit=yes&infloat=yes&lssubmit=yes&inajax=1"

payload='fastloginfield=email&username=caoqianghappy%40126.com&password=3f0ed655a128fedda9efd124afbe3037&quickforward=yes'
headers = {
  'Connection': 'keep-alive',
  'Cache-Control': 'max-age=0',
  'sec-ch-ua': '"Chromium";v="21", " Not;A Brand";v="99"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"',
  'Upgrade-Insecure-Requests': '1',
  'Origin': 'https://www.chinapyg.com',
  'Content-Type': 'application/x-www-form-urlencoded',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
  'Sec-Fetch-Site': 'same-origin',
  'Sec-Fetch-Mode': 'navigate',
  'Sec-Fetch-User': '?1',
  'Sec-Fetch-Dest': 'iframe',
  'Referer': 'https://www.chinapyg.com/',
  'Accept-Language': 'zh-CN,zh;q=0.9',
  'Cookie': 'discuz_2132_auth=b1fa%2FGIxoucSsq8%2BRh3dwqdh%2Fvmi8mtKAe4LOUkH7ZIobR4jO7WYV%2Bb27s9aH0akSly6iNadoyPZ302wfLHnfqTRUQ; discuz_2132_connect_is_bind=0; discuz_2132_lastact=1660098953%09member.php%09logging; discuz_2132_lastcheckfeed=62025%7C1660098932; discuz_2132_lastvisit=1660095332; discuz_2132_lip=101.40.69.178%2C1660098690; discuz_2132_saltkey=r2M4BF9e; discuz_2132_sid=br04W5; discuz_2132_ulastactivity=c871yJ3NJ%2BU%2BFiLbw7vgW%2B7PAdEDO5PeB6XnJhn7vypT1k2gf862'
}

response = session.request("POST", url, headers=headers, data=payload)

print(response.text)


url = "https://www.chinapyg.com/plugin.php?id=dsu_paulsign:sign&operation=qiandao&infloat=1&sign_as=1&inajax=1"

payload='qdxq=kx&qdmode=2&todaysay=&fastreply=0'
response = session.request("POST", url, headers=headers, data=payload)

print(response.text)
