FROM python:3.6-alpine

MAINTAINER shenmishajing <shenmishajing@gmail.com>

ENV LIBRARY_PATH=/lib:/usr/lib
ENV USER_NAME=''
ENV USER_PASSWORD=''
ENV TZ=Asia/Shanghai

WORKDIR /app
RUN apk add --no-cache tzdata
RUN apk add --no-cache --virtual bili build-base python-dev py-pip jpeg-dev zlib-dev
RUN apk add --no-cache git
RUN git clone https://github.com/shenmishajing/bilibili-live-tools.git /app
RUN pip install --no-cache-dir -r requirements.txt
RUN rm -r /var/cache/apk
RUN rm -r /usr/share/man
RUN apk del bili

ENTRYPOINT git pull && \
    pip install --no-cache-dir -r requirements.txt && \
    sed -i ''"$(cat conf/bilibili.conf -n | grep "username =" | awk '{print $1}')"'c '"$(echo "username = ${USER_NAME}")"'' conf/bilibili.conf && \
    sed -i ''"$(cat conf/bilibili.conf -n | grep "password =" | awk '{print $1}')"'c '"$(echo "password = ${USER_PASSWORD}")"'' conf/bilibili.conf && \
    python ./run.py
