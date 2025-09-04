FROM python:3.12-alpine

RUN apk add --update --no-cache bash

RUN mkdir /dima-tech

WORKDIR /dima-tech

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

ENV PATH=/usr/local/bin:$PATH

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0"]