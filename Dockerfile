FROM ronghuaxueleng/jd:latest as base

FROM mitmproxy/mitmproxy
LABEL maintainer="jishuixiansheng"
ARG APP_URL=https://gitee.com/getready/mitmproxy.git
ARG APP_BRANCH=main

ENV PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin \
    LANG=zh_CN.UTF-8 \
    SHELL=/bin/bash \
    PS1="\u@\h:\w \$ " \
    APP_DIR=/mitmproxy

RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories \
    && apk update -f \
    && apk upgrade \
    && apk --no-cache ca-certificates add -f bash git \
    && rm -rf /var/cache/apk/* \
    && git clone -b ${APP_BRANCH} ${APP_URL} ${APP_DIR} \
    && wget -O /tmp/shadowsocksr-3.2.2.tar.gz https://ghproxy.com/https://github.com/shadowsocksrr/shadowsocksr/archive/3.2.2.tar.gz \
	&& tar zxf /tmp/shadowsocksr-3.2.2.tar.gz -C /tmp \
	&& mv /tmp/shadowsocksr-3.2.2/shadowsocks /usr/local/ \
	&& rm -fr /tmp/shadowsocksr-3.2.2 \
	&& rm -f /tmp/shadowsocksr-3.2.2.tar.gz

COPY ./config_sample.json /etc/shadowsocks-r/config.json

WORKDIR ${APP_DIR}
COPY git_pull.sh ${APP_DIR}/
COPY docker-entrypoint.sh ${APP_DIR}/
COPY requirements.txt ${APP_DIR}/
RUN ln -sf ${APP_DIR}/git_pull.sh /usr/local/bin/git_pull \
    && cp -f ${APP_DIR}/docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh \
    && chmod 777 /usr/local/bin/docker-entrypoint.sh

# 使用清华源安装依赖
RUN pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

COPY --from=base /usr/share/zoneinfo /usr/share/zoneinfo/
RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo "Asia/Shanghai" > /etc/timezone
RUN ln -sf /usr/bin/python3 /usr/bin/python

ENV MY_PROXY_URL="http://127.0.0.1:8080"
ENV HTTP_PROXY=$MY_PROXY_URL \
    HTTPS_PROXY=$MY_PROXY_URL \
    FTP_PROXY=$MY_PROXY_URL \
    http_proxy=$MY_PROXY_URL \
    https_proxy=$MY_PROXY_URL \
    ftp_proxy=$MY_PROXY_URL

ENTRYPOINT docker-entrypoint.sh
