#!/usr/bin/env bash
shopt -s extglob
## 文件路径、脚本网址、文件版本以及各种环境的判断
ShellDir=${MITM_DIR:-$(
    # shellcheck disable=SC2046
    # shellcheck disable=SC2164
    cd $(dirname "$0")
    pwd
)}
ScriptsDir=${ShellDir}/jd_scripts
DockerDir=${ScriptsDir}/docker
[ ! -d "${DockerDir}" ] && mkdir -p "${DockerDir}"
# shellcheck disable=SC2034
ListCronSh=${DockerDir}/crontab_list.sh
OwnActionsURL=https://gitee.com/getready/my_actions.git

## 更新Shell源码
function Git_PullShell() {
    echo -e "\n开始更新仓库 /jd\n"
    # shellcheck disable=SC2164
    cd ${ShellDir}
    git fetch --all
    # shellcheck disable=SC2034
    ExitStatusShell=$?
    git reset --hard origin/source
    git pull
}

## 克隆scripts
function Git_CloneScripts() {
    echo -e "克隆${OwnActionsURL} main分支脚本\n"
    git clone -b main ${OwnActionsURL} "${ScriptsDir}"
    ExitStatusScripts=$?
    echo
}

## 更新scripts
function Git_PullScripts() {
    echo -e "更新${OwnActionsURL} main分支脚本\n"
    # shellcheck disable=SC2164
    cd "${ScriptsDir}"
    git fetch --all
    # shellcheck disable=SC2034
    ExitStatusScripts=$?
    git reset --hard origin/main
    echo
}

## 在日志中记录时间与路径
echo -e ''
echo -e "+----------------- 开 始 执 行 更 新 脚 本 -----------------+"
echo -e ''
echo -e "   活动脚本目录：${ScriptsDir}"
echo -e ''
echo -e "   当前系统时间：$(date "+%Y-%m-%d %H:%M")"
echo -e ''
echo -e "+-----------------------------------------------------------+"

## 更新Shell源码
[ -d "${ShellDir}"/.git ] && Git_PullShell
[ -d ${ScriptsDir}/.git ] && Git_PullScripts || Git_CloneScripts

## 赋权
chmod 777 "${ShellDir}"/*
