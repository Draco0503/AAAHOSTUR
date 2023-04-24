FROM ubuntu:jammy

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update \
    && apt install -y python3 python3-pip libmysqlclient-dev \
    && python3 -m pip install -U pip

COPY . /aaahostur
WORKDIR /aaahostur

RUN pip install -r requirements.txt

CMD ["python3", "./APIrest/app.py"]