# -*- coding: utf-8 -*-
import os

from dotenv import load_dotenv, find_dotenv
from pathlib import Path
# 指定env文件
load_dotenv(find_dotenv(Path.cwd().joinpath('os.env')))

print(os.getenv('RUN_OS_NAME'))
