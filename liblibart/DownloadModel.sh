#!/bin/bash

#随机数,表示随机一个30以内的数
randNum=$(($RANDOM%30))

#user 表示当前登陆的用户
#path /var/spool/cron/crontabs
#生成crontab 任务配置文件
#表示在 每周一到周五早上3点到3点30之间，随机一个时间执行一次数据备份
cp /mitmproxy/crontab.list /mitmproxy/liblibart/crontab.list1
echo $[randNum]" */4 * * * /mitmproxy/liblibart/DownloadModel.sh" >> /mitmproxy/liblibart/crontab.list1
crontab /mitmproxy/liblibart/crontab.list1
python3 /mitmproxy/liblibart/DownloadModel.py >> /mitmproxy/logs/download_model.log 2>&1