import requests

url = "http://www.51twx.com/wp-admin/index.php?act=jf"

payload={}
headers = {
  'Connection': 'keep-alive',
  'Pragma': 'no-cache',
  'Cache-Control': 'no-cache',
  'Upgrade-Insecure-Requests': '1',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
  'Referer': 'http://www.51twx.com/wp-admin/index.php',
  'Accept-Language': 'zh-CN,zh;q=0.9',
  'Cookie': 'wordpress_53e0937787fe0b41d3a9e543f2bbf3a3=ronghuaxueleng%7C1651503503%7CEpye7jz0W1E6xRrBuSGPuDLvp5EIzd9ju0YjTlcWNCE%7C21bd7d456aa7d382d72dafc8fcd236e781677db7dd9b3c7628b0f487808f84bf; wordpress_test_cookie=WP%20Cookie%20check; wordpress_logged_in_53e0937787fe0b41d3a9e543f2bbf3a3=ronghuaxueleng%7C1651503503%7CEpye7jz0W1E6xRrBuSGPuDLvp5EIzd9ju0YjTlcWNCE%7C63158eb588bb7ca9ff09401ef14fb9429936e1ec763485a114a8a94c1ca47b55; PHPSESSID=3pgu69j76ftkmu3v8uqb8jvom7; wp-settings-time-13878=1650330794; PHPSESSID=71fgd1qf1h50s7i6h0bkdicfje; wp-settings-time-13878=1650330887'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)
