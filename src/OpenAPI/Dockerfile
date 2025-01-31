FROM python:3.10.0-alpine

WORKDIR /app

ADD src/OpenAPI /app

RUN pip install --upgrade pip \
  && pip install -r requirements.txt

EXPOSE 8080

CMD ["python", "main.py"]