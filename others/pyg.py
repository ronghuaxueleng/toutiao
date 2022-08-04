import requests

url = "https://www.chinapyg.com/plugin.php?id=dsu_paulsign:sign&operation=qiandao&infloat=1&sign_as=1&inajax=1"

payload='formhash=318e4f52&qdxq=kx&qdmode=2&todaysay=&fastreply=0'
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
  'Cookie': 'discuz_2132_saltkey=vdD0dj40; discuz_2132_lastvisit=1657457842; discuz_2132_auth=8f8fYYgwDcBbki%2Bnl2iAI3rjX6RqeDCWaZuK3pQuBqWsaeQTrhwCK49BluvNuvXRRJsT9n8%2FIqdmZX2lKUIDRZPYKQ; discuz_2132_connect_is_bind=0; discuz_2132_nofavfid=1; discuz_2132_smile=1D1; discuz_2132_st_p=62025%7C1659488656%7C4d63ea4661c3b0fb65fa02aab91ba990; discuz_2132_viewid=tid_144234; discuz_2132_sid=nxS227; discuz_2132_lip=101.40.69.178%2C1659488650; discuz_2132_onlineusernum=2151; discuz_2132_ulastactivity=6be0TS4GvcGrjEHSq0G8Y98A%2Bvha58BF42gVHZ9g46ZN1JVsY9Au; discuz_2132_lastcheckfeed=62025%7C1659574875; discuz_2132_checkfollow=1; discuz_2132_checkpm=1; discuz_2132_sendmail=1; discuz_2132_lastact=1659574891%09plugin.php%09; discuz_2132_connect_is_bind=0; discuz_2132_lastact=1659574998%09plugin.php%09'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
