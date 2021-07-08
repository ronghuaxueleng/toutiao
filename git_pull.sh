#!/usr/bin/env bash
shopt -s extglob
## 文件路径、脚本网址、文件版本以及各种环境的判断
ShellDir=${MITM_DIR:-$(
    # shellcheck disable=SC2046
    # shellcheck disable=SC2164
    cd $(dirname "$0")
    pwd
)}
LogDir=${ShellDir}/logs
[ ! -d ${LogDir} ] && mkdir -p ${LogDir}
OwnActionsURL=https://gitee.com/getready/mitmproxy.git

## 更新Shell源码
function Git_PullShell() {
    echo -e "\n开始更新仓库 /jd\n"
    # shellcheck disable=SC2164
    cd ${ShellDir}
    git fetch --all
    # shellcheck disable=SC2034
    ExitStatusShell=$?
    git reset --hard origin/main
    git pull
}

## 在日志中记录时间与路径
echo -e ''
echo -e "+----------------- 开 始 执 行 更 新 脚 本 -----------------+"
echo -e ''
echo -e "   当前系统时间：$(date "+%Y-%m-%d %H:%M")"
echo -e ''
echo -e "+-----------------------------------------------------------+"

## 更新Shell源码
[ -d "${ShellDir}"/.git ] && Git_PullShell
crontab -r && crontab "${ShellDir}"/crontab.list

## 赋权
chmod 777 "${ShellDir}"/*
