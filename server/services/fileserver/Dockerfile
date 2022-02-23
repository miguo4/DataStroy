FROM python:3.7.4-slim

RUN apt-get update
RUN apt-get install libquadmath0
RUN apt-get install -y libgomp1 
COPY requirements.txt /
RUN pip3 install -r /requirements.txt

COPY /server /server
WORKDIR /server
