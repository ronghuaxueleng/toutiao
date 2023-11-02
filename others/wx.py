import io
import json
import re
import sys

import requests
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')
with open('鱼羊史记.json', 'r', encoding='UTF-8') as f:
    data_list = json.load(f)
    pattern = r"data-src=\"https:\/\/mmbiz\.qpic\.cn\S+\""
    all_urls = []
    for data in data_list:
        url = data.get('链接')
        print(url)
        res = requests.get(url)
        text = res.text
        urls = re.findall(pattern, text)
        if len(urls) > 0:
            all_urls.extend(urls)
    with open('data.json', 'w') as f1:
        # 使用json.dump()函数将序列化后的JSON格式的数据写入到文件中
        json.dump(all_urls, f1, ensure_ascii=False)
