import requests

session = requests.session()

url = "http://www.51twx.com/wp-login.php"

payload='log=ronghuaxueleng&pwd=xinyan1203&wp-submit=%E7%99%BB%E5%BD%95&redirect_to=http%3A%2F%2Fwww.51twx.com%2Fwp-admin%2F&testcookie=1'
headers = {
  'Connection': 'keep-alive',
  'Pragma': 'no-cache',
  'Cache-Control': 'no-cache',
  'Upgrade-Insecure-Requests': '1',
  'Origin': 'http://www.51twx.com',
  'Content-Type': 'application/x-www-form-urlencoded',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
  'Referer': 'http://www.51twx.com/wp-login.php?loggedout=true&wp_lang=zh_CN',
  'Accept-Language': 'zh-CN,zh;q=0.9'
}

session.request("POST", url, headers=headers, data=payload)

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
}

response = session.request("GET", url, headers=headers, data=payload)

print(response.text)
