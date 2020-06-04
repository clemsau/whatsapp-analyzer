FROM python:3.7.6-alpine as builder

LABEL maintainer="onlinejudge95@gmail.com"

WORKDIR /usr/src/app

COPY ./requirements.txt ./

RUN apk update && \
    apk add --no-cache g++

RUN pip wheel --no-cache-dir --no-deps --wheel-dir /wheels --requirement ./requirements.txt

FROM python:3.7.6-alpine

LABEL maintainer="onlinejudge95@gmail.com"

WORKDIR /usr/src/app

COPY --from=builder /wheels /wheels

RUN apk update && \
    apk add --no-cache g++

RUN pip install --no-cache-dir /wheels/*

COPY . .

CMD [ "flask", "run", "-h", "0.0.0.0" ]
