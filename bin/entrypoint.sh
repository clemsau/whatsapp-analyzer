#!/bin/sh

flask run --host 0.0.0.0 --port 5000

if [ ! -d "/etc/gunicorn" ]; then
    mkdir -p "/etc/gunicorn"
    elif [ ! -d "/var/log/gunicorn/access"]; then
    mkdir -p "/var/log/gunicorn/access"
    elif [ ! -d "/var/log/gunicorn/error"]; then
    mkdir -p "/var/log/gunicorn/error"
fi

mv /usr/src/app/gunicorn.conf.py /etc/gunicorn
mv /usr/src/app/gunicorn.log.conf /etc/gunicorn

gunicorn --config /etc/gunicorn/gunicorn.conf.py wsgi:app