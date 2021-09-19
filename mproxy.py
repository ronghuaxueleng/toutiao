import functools
import json
import logging
import logging.handlers

# 日志配置
import re

from toutiao.toutiao import save_task_data, save_request_data, save_jd_pin, save_abb_header

logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s')
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)
file_handler = logging.handlers.RotatingFileHandler("mproxy.log", maxBytes=10485760, backupCount=5, encoding="utf-8")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

'''
    异常捕捉
'''


def log_exception(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            fn(*args, **kwargs)
        except Exception as e:
            logging.exception("[Error in {}] msg: {}".format(__name__, str(e)))
            raise

    return wrapper


'''
    抓包监听
'''


class mproxy:

    @log_exception
    def request(self, flow):
        if '/luckycat/lite/v1/activity/done_whole_scene_task' in flow.request.path:
            save_task_data(flow, 'done_whole_scene_task')

        if '/score_task/v1/task/new_excitation_ad' in flow.request.path:
            save_task_data(flow, 'new_excitation_ad')

        if '/score_task/v1/task/open_treasure_box' in flow.request.path:
            save_task_data(flow, 'open_treasure_box')

        if '/luckycat/lite/v1/sleep/done_task' in flow.request.path:
            save_task_data(flow, 'sleep_done_task')

        if '/luckycat/lite/v1/eat/done_eat' in flow.request.path:
            save_task_data(flow, 'eat_done_task')

        if '/luckycat/lite/v1/article/done_score_task' in flow.request.path:
            save_task_data(flow, 'done_score_task')

        if '/luckycat/lite/v1/task/done_universal_task' in flow.request.path:
            save_task_data(flow, 'done_universal_task')

        if '/luckycat/lite/v1/task/done/excitation_ad' in flow.request.path:
            save_task_data(flow, 'excitation_ad')

        if 'api.m.jd.com' in flow.request.host:
            save_jd_pin(flow)

    @log_exception
    def response(self, flow):
        if "snssdk.com" in flow.request.host:
            if '/passport/account/info/v2/?' in flow.request.path:
                save_request_data(flow)

        if 'front15.ncziliyun.com' in flow.request.host and '/user/person.html' in flow.request.path:
            save_abb_header(flow)


addons = [
    mproxy()
]
