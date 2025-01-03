FROM ronghuaxueleng/mitmproxy:6.0.2
LABEL maintainer="jishuixiansheng"
ARG APP_URL=https://proxy.v2gh.com/https://github.com/ronghuaxueleng/toutiao.git
ARG APP_BRANCH=main

ENV PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin \
    PYTHONPATH="${PYTONPATH}:/mitmproxy:/mitmproxy/toutiao" \
    LANG=zh_CN.UTF-8 \
    SHELL=/bin/bash \
    PS1="\u@\h:\w \$ " \
    APP_DIR=/mitmproxy

RUN apk update && \
  #设置时区
  apk add --no-cache tzdata && \
  cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && \
  echo "Asia/Shanghai" > /etc/timezone && \
  apk del tzdata

RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories \
    && apk update -f \
    && apk upgrade \
    && apk --no-cache ca-certificates add -f bash git g++ gcc libxslt-dev libxml2-dev python3-dev \
    && rm -rf /var/cache/apk/* \
    && git clone -b ${APP_BRANCH} ${APP_URL} ${APP_DIR}

WORKDIR ${APP_DIR}
COPY git_pull.sh ${APP_DIR}/
COPY docker-entrypoint.sh ${APP_DIR}/
COPY requirements.txt ${APP_DIR}/
COPY supervisord.conf /etc/
RUN ln -sf ${APP_DIR}/git_pull.sh /usr/local/bin/git_pull \
    && cp -f ${APP_DIR}/docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh \
    && chmod 777 /usr/local/bin/docker-entrypoint.sh

# 使用清华源安装依赖
RUN pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

CMD ["/usr/local/bin/supervisord", "-c", "/etc/supervisord.conf"]
