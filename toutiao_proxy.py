import functools
import logging
import logging.handlers

from toutiao.jisu.toutiao import save_toutiao_data, save_toutiao_task_data

# 日志配置

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
        if '/luckycat/news/v1/treasure/open_treasure_box' in flow.request.path:
            save_toutiao_task_data(flow, 'open_treasure_box')

        if '/luckycat/news/v1/task/done/excitation_ad' in flow.request.path:
            save_toutiao_task_data(flow, 'excitation_ad')

    @log_exception
    def response(self, flow):
        if 'toutiaoapi.com' in flow.request.host:
            if '/user/profile/homepage/v7' in flow.request.path:
                logger.info("更新/添加今日头条用户信息")
                save_toutiao_data(flow)


addons = [
    mproxy()
]
