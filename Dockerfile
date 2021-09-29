FROM ronghuaxueleng/mitmproxy:7.0.3
LABEL maintainer="jishuixiansheng"
ARG APP_URL=https://gitee.com/getready/toutiao.git
ARG APP_BRANCH=main

ENV PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin \
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
RUN chmod 777 ${APP_DIR}/git_pull.sh \
    && chmod 777 ${APP_DIR}/docker-entrypoint.sh

# 使用清华源安装依赖
RUN pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
RUN pip install git+https://gitee.com/getready/supervisor-stdout.git
RUN pip install --force-reinstall h2==3.2.0

CMD ["/usr/local/bin/supervisord", "-c", "/etc/supervisord.conf"]
