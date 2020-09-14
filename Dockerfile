FROM traefik:2.2.1 as base

FROM base as builder

WORKDIR /wheels

RUN apk --no-cache upgrade \
    && apk --no-cache add \
    alpine-sdk \
    python3 \
    python3-dev \
    libffi-dev \
    openssl-dev 

RUN pip3 install --upgrade pip \
    && pip3 install wheel \
    && pip3 wheel cryptography

FROM base

COPY --from=builder /wheels /wheels
COPY challenge-dns.py /

RUN apk --no-cache upgrade \
    && apk --no-cache add python3 \
    && pip3 install --upgrade pip \
    && pip3 install -f /wheels cryptography \
    && rm -rf /var/cache/apk/* /wheels /root/.cache \
    && pip3 install domeneshop

ENV EXEC_PATH /challenge-dns.py

