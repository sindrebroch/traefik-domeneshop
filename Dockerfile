FROM traefik:2.2.1

RUN apk --no-cache upgrade \
    && apk --no-cache add python3 \
    && pip3 install --upgrade pip \
    && pip3 install domeneshop

COPY challenge-dns.py /

ENV EXEC_PATH=/challenge-dns.py

