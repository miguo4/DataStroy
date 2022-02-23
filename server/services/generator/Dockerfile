FROM python:3.7.4-slim

RUN apt-get update
COPY requirements.txt /

RUN pip install -i https://pypi.douban.com/simple/ --no-cache-dir -r requirements.txt

COPY /server /server
WORKDIR /server