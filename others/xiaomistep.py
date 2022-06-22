import requests

url = "https://api.kit9.cn/api/milletmotion/?mobile=15901254680&password=xinyan1203&step=100000"

payload={}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)
