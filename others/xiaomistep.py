import requests

url = "https://api.kit9.cn/api/milletmotion/?mobile=15901254680&password=xinyan1203&step=49999"

payload={}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)

url = "https://api.kit9.cn/api/milletmotion/?mobile=15901296902&password=sxy116816&step=49999"

payload={}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)
