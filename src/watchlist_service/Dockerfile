FROM python:3.9-slim

RUN apt-get update \
    && apt-get install -y pkg-config gcc default-libmysqlclient-dev

ENV MYSQLCLIENT_INCLUDE_DIRS=/usr/include/mariadb
ENV MYSQLCLIENT_LIB_DIRS=/usr/lib/x86_64-linux-gnu

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip \
    && pip install -r requirements.txt

COPY . .

ENV FLASK_APP=watchlist_service.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=8080

EXPOSE 8080

CMD ["flask", "run"]