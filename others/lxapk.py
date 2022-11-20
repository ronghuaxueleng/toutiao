import requests

from others.qinglong import QingLong

url = "https://www.lxapk.com/wp-admin/admin-ajax.php"

payload = "action=user_checkin"
headers = {
  'Connection': 'keep-alive',
  'sec-ch-ua': '"Chromium";v="21", " Not;A Brand";v="99"',
  'Accept': 'application/json, text/javascript, */*; q=0.01',
  'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
  'X-Requested-With': 'XMLHttpRequest',
  'sec-ch-ua-mobile': '?0',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
  'sec-ch-ua-platform': '"Windows"',
  'Origin': 'https://www.lxapk.com',
  'Sec-Fetch-Site': 'same-origin',
  'Sec-Fetch-Mode': 'cors',
  'Sec-Fetch-Dest': 'empty',
  'Referer': 'https://www.lxapk.com/message/',
  'Accept-Language': 'zh-CN,zh;q=0.9',
  'Cookie': 'wordpress_sec_6b6a752c3623b1d09888c726dc9108af=%E7%BB%92%E8%8A%B1%E9%9B%AA%E5%86%B7%7C1668733546%7CEVJ1dSt6byQiBrimzZLG0jUYzfY32yabfH3MuYrDTuM%7C1d97418a9a46e3596af6640ec8ca7ccccfc14431bcbb5d066d7c998bdcb0553a; showed_sign_modal=showed; PHPSESSID=6jq4rig7qutuct1hpo4gl3dju1; wordpress_logged_in_6b6a752c3623b1d09888c726dc9108af=%E7%BB%92%E8%8A%B1%E9%9B%AA%E5%86%B7%7C1668733546%7CEVJ1dSt6byQiBrimzZLG0jUYzfY32yabfH3MuYrDTuM%7Cddd2f4dfa1407953c44ce9324dcec31e1cf90a5779e872bfffd6e37dcc1ce65a'
}

response = QingLong().run('LXAPK_COOKIE')
if response['code'] == 200:
  cookies = response['data']
  for cookie in cookies:
    headers['Cookie'] = cookie['value']
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)
