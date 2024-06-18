import logging
from logging import handlers


class LogInfo(object):
    def __init__(self, filename=None):
        self.logger = logging.getLogger('liblibart')
        if not self.logger.handlers:
            LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
            DATE_FORMAT = "%Y-%m-%d %H:%M:%S %p"
            format_str = logging.Formatter(LOG_FORMAT, DATE_FORMAT)  #设置日志格式
            self.logger.setLevel(logging.INFO)  #设置日志级别
            sh = logging.StreamHandler()  #往屏幕上输出
            sh.setFormatter(format_str)  #设置屏幕上显示的格式
            th = handlers.TimedRotatingFileHandler(filename=filename, backupCount=1, encoding='utf-8')
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
            self.logger.addHandler(sh)  #把对象加到logger里
            self.logger.addHandler(th)


