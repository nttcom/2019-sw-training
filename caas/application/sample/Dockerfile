FROM alpine

# install software
RUN apk update && \
    apk upgrade && \
    apk add --no-cache \
    apache2

# run process
ENTRYPOINT httpd -D FOREGROUND