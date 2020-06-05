FROM python:3.7.6-slim as builder

LABEL maintainer="onlinejudge95@gmail.com"

WORKDIR /usr/src/app

COPY ./requirements.txt ./

RUN pip wheel --no-cache-dir --no-deps --wheel-dir /wheels --requirement ./requirements.txt

FROM python:3.7.6-slim

LABEL maintainer="onlinejudge95@gmail.com"

WORKDIR /usr/src/app

COPY --from=builder /wheels /wheels

RUN pip install --no-cache-dir /wheels/*

COPY . .

RUN chmod +x bin/entrypoint.sh

CMD [ "bin/entrypoint.sh" ]
