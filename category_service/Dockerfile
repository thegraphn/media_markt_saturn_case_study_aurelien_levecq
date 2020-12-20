FROM ubuntu:18.04

ENV PORT 8888

RUN apt-get update \
  && apt-get install -y python3-pip python3-dev \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip



COPY ./service service/
COPY ./service category_model/
COPY service/category_model service/
WORKDIR service


RUN pip3 install -r requirements.txt

ENTRYPOINT python main.py

EXPOSE ${PORT}