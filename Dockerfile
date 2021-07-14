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

ENV LIBEV_VER 3.2.5
ENV LIBEV_NAME shadowsocks-libev-${LIBEV_VER}
ENV LIBEV_RELEASE https://github.com/shadowsocks/shadowsocks-libev/releases/download/v${LIBEV_VER}/${LIBEV_NAME}.tar.gz

RUN runDeps="\
		tar \
		git \
		wget \
		build-base \
		c-ares-dev \
		autoconf \
		automake \
		libev-dev \
		libtool \
		libsodium-dev \
		linux-headers \
		mbedtls-dev \
		pcre-dev \
	"; \
    sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories \
    && apk update -f \
    && apk upgrade \
    && apk add --no-cache --virtual .build-deps ${runDeps} \
    && mkdir -p /tmp/libev \
	&& cd /tmp/libev \
	&& git clone --depth=1 https://github.com/shadowsocks/simple-obfs.git . \
	&& git submodule update --init --recursive \
	&& ./autogen.sh \
	&& ./configure --prefix=/usr --disable-documentation \
	&& make install \
	&& rm -rf * \
	&& wget -qO ${LIBEV_NAME}.tar.gz ${LIBEV_RELEASE} \
	&& tar zxf ${LIBEV_NAME}.tar.gz \
	&& cd ${LIBEV_NAME} \
	&& ./configure --prefix=/usr --disable-documentation \
	&& make install \
    && apk add --no-cache rng-tools bash git \
		$(scanelf --needed --nobanner /usr/bin/ss-* \
		| awk '{ gsub(/,/, "\nso:", $2); print "so:" $2 }' \
		| xargs -r apk info --installed \
		| sort -u) \
	&& apk del .build-deps \
	&& cd /tmp \
	&& rm -rf /tmp/libev \
    && rm -rf /var/cache/apk/* \
    && git clone -b ${APP_BRANCH} ${APP_URL} ${APP_DIR}

COPY ./config_sample.json /etc/shadowsocks-libev/config.json

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

ENTRYPOINT docker-entrypoint.sh
