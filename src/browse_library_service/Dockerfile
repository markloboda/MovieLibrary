FROM python:3.9-slim

ENV FLASK_APP=browse_library_service.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=8080

WORKDIR /app

ADD src/browse_library_service /app

RUN pip install --upgrade pip \
  && pip install -r requirements.txt

EXPOSE 8080

CMD ["flask", "run"]