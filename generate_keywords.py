# -*- coding: utf-8 -*-
import requests
import json
import time
from datetime import datetime
import random

# 配置区 ================================================
DEEPSEEK_API_KEY = "4YpnBSETwahD6URC87HHgpAsK/gr9q9BOfvzYDDsX9Dh+4zcOljr6xyhQc3qrDVM"  # 替换为你的API密钥
API_URL = "http://www.ronghuaxueleng.top:8901/v1/chat/completions"
CATEGORIES = [
    "情感冲突",
    "悬疑推理",
    # "科幻幻想",
    # "意象隐喻",
    # "荒诞喜剧",
    # "日常观察",
    # "情感疗愈",
    # "商业写作",
    # "教育成长",
    # "节日场景",
    # "职场生存",
    # "自然科普",
    # "文化评论",
    # "旅行探索",
    # "跨界实验",
    "新媒体虐文",
    "校园暗恋",
    "民俗惊悚",
    "高智商犯罪",
    "时空悖论",
    "物种变异",
    "职场生存",
    "家庭伦理",
    "复仇逆袭",
    "暗黑童话",
    "朝堂博弈",
    "后宫生存法则",
    "职场禁忌恋",
    "契约婚姻博弈",
    "日常物品异化",
    "时空循环谜题",
    "非遗活化题材",
    # "赛博玄学",
    "直播事故现场",
    "密闭空间杀局",
    "教育焦虑",
    "职场PUA自救",
]
MAX_RETRIES = 3  # 失败重试次数


# 关键词生成函数 ========================================
def generate_keywords():
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }

    # 动态生成提示词
    category = random.sample(CATEGORIES, 3)
    print(f'写作类型【{category}】')
    prompt = f"""请生成一组用于创意写作的{category}类关键词组合，要求：
    1. 包含10个不重复的具象词汇（如：机械苔藓、未寄信、暴雨夜）
    2. 词汇间需存在潜在逻辑关联
    3. 符合{category}类型的特点
    4. 非赛博类型不要出现超现实和AI
    5. 如果有引用的网页，请将网页内容总结后展示出来
    6. 返回格式:关键词组合\n逻辑关联
    """
    print(prompt)

    payload = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }

    # 带重试机制的请求
    for attempt in range(MAX_RETRIES):
        try:
            response = requests.post(API_URL, headers=headers, json=payload)
            if response.status_code == 200:
                result = json.loads(response.text)
                content = result['choices'][0]['message']['content'].strip()
                return process_content(content, category)
            else:
                print(f"API请求失败: {response.status_code}")
        except Exception as e:
            print(f"发生异常: {str(e)}")
        time.sleep(2 ** attempt)  # 指数退避重试
    return None


# 结果处理函数 ==========================================
def process_content(content, category):
    # 生成记录文本
    timestamp = datetime.now().strftime("%Y-%m-%d  %H:%M:%S")
    log_entry = f"{category}类\n{content}\n"
    # print(log_entry)

    url = "https://flomoapp.com/iwh/MjI1OTA3NA/27f19ad5ec2e73ccb93228e47b32c8f7"
    payload = json.dumps({
        'content': f"{log_entry} --来自：deepseek \n#创意写作"
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    print(json.dumps(response.json(), indent=2))


if __name__ == "__main__":
    print("关键词生成服务已启动...")
    generate_keywords()
