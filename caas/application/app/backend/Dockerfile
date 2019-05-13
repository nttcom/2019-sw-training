FROM alpine

# install libs
RUN apk update && \
    apk upgrade && \
    apk add --no-cache \
    python \
    python-dev \
    py-pip \
    gcc \
    musl \
    musl-dev \
    libffi-dev \
    openssl-dev

# get resource
RUN mkdir /apps
COPY src /apps/src

# install tools
WORKDIR /apps/src
RUN pip install -r requirements.txt

# run program
ENTRYPOINT python run.py