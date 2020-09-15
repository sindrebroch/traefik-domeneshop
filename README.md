# Traefik-Domeneshop

![Docker Cloud Build Status](https://img.shields.io/docker/cloud/build/kybber/traefik-domeneshop)
![Docker Cloud Automated build](https://img.shields.io/docker/cloud/automated/kybber/traefik-domeneshop)
![Docker Image Size (latest by date)](https://img.shields.io/docker/image-size/kybber/traefik-domeneshop)
![Docker Stars](https://img.shields.io/docker/stars/kybber/traefik-domeneshop)
![Docker Pulls](https://img.shields.io/docker/pulls/kybber/traefik-domeneshop)

This docker image amends the official [Traefik](https://hub.docker.com/_/traefik) image to enable LetsEncrypt [DNS challenges](https://docs.traefik.io/user-guides/docker-compose/acme-dns/) for [Domeneshop](https://domene.shop/) customers. 

The challenge is performed by a Python script, which means that the dnsChallenge [provider](https://docs.traefik.io/v2.0/https/acme/#providers) must be set to `exec` ([External Program](https://go-acme.github.io/lego/dns/exec/)).

## Usage:
Obtain a token and secret from your [Domeneshop API keys page](https://domene.shop/admin?view=api) 
and place them in the following environment variables:
```
  DOMENESHOP_TOKEN
  DOMENESHOP_SECRET
```
Run the container like your would use the official [Traefik](https://hub.docker.com/_/traefik) image, but ensure that your Traefik configuration sets
`certificatesResolvers.myresolver.acme.dnsChallenge.provider` to `exec`. If you have issues with timeouts, you can try to increase `certificatesResolvers.myresolver.acme.dnsChallenge.delayBeforeCheck` from its default value `0`.
