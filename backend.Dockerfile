FROM python:3.12-alpine

LABEL maintainer="mihai@developerakademie.com"
LABEL version="1.0"
LABEL description="Python 3.12 Alpine"

WORKDIR /app

COPY . .
COPY norton.crt /usr/local/share/ca-certificates/norton.crt
RUN apk update && \
    apk add --no-cache --upgrade \
        bash \
        postgresql-client \
        ffmpeg \
        ca-certificates && \
    update-ca-certificates && \
    apk add --no-cache --virtual .build-deps \
        gcc \
        musl-dev \
        postgresql-dev && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    apk del .build-deps && \
    chmod +x backend.entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["./backend.entrypoint.sh"]