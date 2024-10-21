import logging
import re
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
            # interval 滚动周期， when="MIDNIGHT", interval=1 表示每天0点为更新点，每天生成一个文件,backupCount  表示日志保存个数
            file_hander = handlers.TimedRotatingFileHandler(filename=self.filename, when='MIDNIGHT',
                                                            interval=1, backupCount=1, encoding='utf-8')
            # 设置生成日志文件名的格式，以年-月-日来命名
            # suffix设置，会生成文件名为log.2020-02-25.log
            file_hander.suffix = "%Y-%m-%d.log"
            # extMatch是编译好正则表达式，用于匹配日志文件名后缀
            # 需要注意的是suffix和extMatch一定要匹配的上，如果不匹配，过期日志不会被删除。
            file_hander.extMatch = re.compile(r"^\d{4}-\d{2}-\d{2}.log$")
            #往文件里写入#指定间隔时间自动生成文件的处理器
            #实例化TimedRotatingFileHandler
            #interval是时间间隔，backupCount是备份文件的个数，如果超过这个个数，就会自动删除，when是间隔的时间单位，单位有以下几种：
            # S 秒
            # M 分
            # H 小时、
            # D 天、
            # W 每星期（interval==0时代表星期一）
            # midnight 每天凌晨
            file_hander.setFormatter(format_str)  #设置文件里写入的格式
            logger.addHandler(sh)  #把对象加到logger里
            logger.addHandler(file_hander)
        return logger
