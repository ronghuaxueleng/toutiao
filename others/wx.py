import hashlib
import io
import json
import os
import re
import sys
import time

import requests

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='gb18030')


def save_image_urls():
    with open('鱼羊史记.json', 'r', encoding='UTF-8') as f:
        data_list = json.load(f)
        pattern = r"data-src=\"(?P<url>https:\/\/mmbiz\.qpic\.cn\S+)\""
        regex = re.compile(pattern)
        all_urls = []
        for data in data_list:
            url = data.get('链接')
            print(url)
            res = requests.get(url)
            text = res.text
            urls = regex.findall(text)
            if len(urls) > 0:
                all_urls.extend(urls)
        with open('data.json', 'w') as f1:
            # 使用json.dump()函数将序列化后的JSON格式的数据写入到文件中
            json.dump(all_urls, f1, ensure_ascii=False)


def request_get(url, ret_type="text", timeout=5, encoding="GBK"):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"
    }
    res = requests.get(url=url, headers=headers, timeout=timeout)
    res.encoding = encoding
    if ret_type == "text":
        return res.text
    elif ret_type == "image":
        return res.content


def save_image(image_src):
    md = hashlib.md5()     #获取一个md5加密算法对象
    md.update(image_src.encode('utf-8'))                   #制定需要加密的字符串
    file_local_path = f"./img/{md.hexdigest()}.jpg"
    if not os.path.exists(file_local_path):
        content = request_get(image_src, "image")
        with open(file_local_path, "wb") as f:
            f.write(content)
            print("图片保存成功")


if __name__ == '__main__':
    with open('data.json', 'r', encoding='UTF-8') as f:
        data_list = json.load(f)
        for image_src in data_list:
            save_image(image_src)
