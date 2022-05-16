FROM python:3.10-alpine

RUN mkdir -p /usr/src/my_ethernet
WORKDIR /usr/src/my_ethernet
COPY . /usr/src/my_ethernet
RUN pip install --no-cache-dir -r requirements.txt
