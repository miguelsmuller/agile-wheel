#!/bin/sh

envsubst '${INTERNAL_PORT}' < /etc/nginx/nginx.conf.template > /etc/nginx/nginx.conf

exec /docker-entrypoint.sh \
    nginx -g "daemon off;"
