#!/bin/bash
set -e
set -o errexit
set -o pipefail
set -o nounset

## 项目使用需知：
function UseNotes() {
  echo -e "\033[32m=========================================== 容   器   启   动   成   功 ===========================================\033[0m"
  echo -e ''
  echo -e "\033[32m+-----------------------------------------------------------------------------------------------------------------+\033[0m"
  echo -e "\033[32m|                                                                                                                 |\033[0m"
  echo -e "\033[32m| 注意：1. git_pull.sh 为一键更新脚本，run_all.sh 为一键执行所有活动脚本                                          |\033[0m"
  echo -e "\033[32m|                                                                                                                 |\033[0m"
  echo -e "\033[32m|       2. 本项目可以通过定时的方式全天候自动运行活动脚本，具体运行记录可通过日志查看                             |\033[0m"
  echo -e "\033[32m|                                                                                                                 |\033[0m"
  echo -e "\033[32m|       3. 项目已配置好 Crontab 定时任务，定时配置文件 crontab.list 会通过活动脚本的更新而同步更新                |\033[0m"
  echo -e "\033[32m|                                                                                                                 |\033[0m"
  echo -e "\033[32m|       4. 您可以通过容器外的主机挂载目录来编辑配置文件、查看活动运行日志、查看脚本文件                           |\033[0m"
  echo -e "\033[32m|                                                                                                                 |\033[0m"
  echo -e "\033[32m+-----------------------------------------------------------------------------------------------------------------+\033[0m"
  echo -e ''
}

echo -e "\n========================1. 更新源代码========================\n"
crond >/dev/null 2>&1
bash git_pull
echo

UseNotes
/usr/sbin/nginx -c /usr/local/nginx/conf/nginx.conf
/usr/local/shadowsocks/server.py -c /etc/shadowsocks-r/config.json &
/usr/bin/mitmdump -s mproxy.py --set block_global=false --mode socks5
exec "$@"