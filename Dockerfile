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

WORKDIR ${APP_DIR}

RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories \
    && apk update -f \
    && apk upgrade

COPY ./config_sample.json /etc/shadowsocks-r/config.json

RUN set -ex \
	&& apk add --no-cache tar libsodium-dev openssl \
	&& wget -O /tmp/shadowsocksr-3.2.2.tar.gz https://ghproxy.com/https://github.com/shadowsocksrr/shadowsocksr/archive/3.2.2.tar.gz \
	&& tar zxf /tmp/shadowsocksr-3.2.2.tar.gz -C /tmp \
	&& mv /tmp/shadowsocksr-3.2.2/shadowsocks /usr/local/ \
	&& rm -fr /tmp/shadowsocksr-3.2.2 \
	&& rm -f /tmp/shadowsocksr-3.2.2.tar.gz

RUN apk add --no-cache rng-tools bash git \
		$(scanelf --needed --nobanner /usr/bin/ss-* \
		| awk '{ gsub(/,/, "\nso:", $2); print "so:" $2 }' \
		| xargs -r apk info --installed \
		| sort -u) \
	&& cd /tmp \
	&& rm -rf /tmp/libev \
    && rm -rf /var/cache/apk/* \
    && git clone -b ${APP_BRANCH} ${APP_URL} ${APP_DIR}

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

ENTRYPOINT docker-entrypoint.sh
