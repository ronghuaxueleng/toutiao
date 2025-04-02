import json

import requests

url = "https://v1.hitokoto.cn/"

payload = {}
headers = {
    'authority': 'v1.hitokoto.cn',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'no-cache',
    'cookie': '_gid=GA1.2.423158519.1743557302; _ga=GA1.1.1109522635.1743557302; _ga_74ZZC03H3M=GS1.1.1743557301.1.1.1743557642.0.0.0; __gads=ID=56e1cb39f324bfd2:T=1743557286:RT=1743576697:S=ALNI_MbLjHktlGMdF5vPjTTM3bW6WOrJaQ; __gpi=UID=00001085c3cf09d2:T=1743557286:RT=1743576697:S=ALNI_MYFlXx44bH-PU1RuXLLICN39zUdcw; __eoi=ID=2b0ee7211b9b57e0:T=1743557286:RT=1743576697:S=AA-AfjaNKikHfZuenpLS7MUBnQ8a; _ga_QL2J611R9Q=GS1.1.1743576694.2.0.1743576703.0.0.0',
    'dnt': '1',
    'pragma': 'no-cache',
    'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.95 Safari/537.36'
}

response = requests.request("GET", url, headers=headers, data=payload)
res = json.loads(response.text)

url = "https://flomoapp.com/iwh/MjI1OTA3NA/27f19ad5ec2e73ccb93228e47b32c8f7"
payload = json.dumps({
    'content': f"{res['hitokoto']} --来自：{res['from']} \n#一言"
})
headers = {
    'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)
print(response.text)
