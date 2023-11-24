FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get update && apt-get install -y bash

WORKDIR /app/

COPY . /app/

RUN pip install -r requirements.txt

CMD ["bash", "/app/start.sh"]
