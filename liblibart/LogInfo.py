import logging
from logging import handlers

from dotenv import load_dotenv, find_dotenv
from pathlib import Path

# 指定env文件
env_path = Path.cwd().joinpath('env').joinpath('os.env')
env_path.parent.mkdir(exist_ok=True)
load_dotenv(find_dotenv(str(env_path)))


class LogInfo(object):
    def __init__(self, filename=None):
        Path(filename).parent.mkdir(exist_ok=True)
        self.filename = filename

    def getLogger(self):
        logger = logging.getLogger(self.filename)
        if not logger.handlers:
            LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
            DATE_FORMAT = "%Y-%m-%d %H:%M:%S %p"
            format_str = logging.Formatter(LOG_FORMAT, DATE_FORMAT)  #设置日志格式
            logger.setLevel(logging.INFO)  #设置日志级别
            sh = logging.StreamHandler()  #往屏幕上输出
            sh.setFormatter(format_str)  #设置屏幕上显示的格式
            th = handlers.TimedRotatingFileHandler(filename=self.filename, backupCount=1, encoding='utf-8')
            #往文件里写入#指定间隔时间自动生成文件的处理器
            #实例化TimedRotatingFileHandler
            #interval是时间间隔，backupCount是备份文件的个数，如果超过这个个数，就会自动删除，when是间隔的时间单位，单位有以下几种：
            # S 秒
            # M 分
            # H 小时、
            # D 天、
            # W 每星期（interval==0时代表星期一）
            # midnight 每天凌晨
            th.setFormatter(format_str)  #设置文件里写入的格式
            logger.addHandler(sh)  #把对象加到logger里
            logger.addHandler(th)
        return logger
