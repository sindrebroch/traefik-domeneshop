# traefik-domeneshop
This docker image amends the official [traefik](https://hub.docker.com/_/traefik) 
image to enable LetsEncrypt DNS-01 challenges for Domeneshop so that system such as 
[this](https://www.smarthomebeginner.com/traefik-2-docker-tutorial) can be created 
for Domeneshop customers without having to transfer name servers to e.f. CloudFlare.

## Usage
Clone the repo to your docker host and build image:

```
cd traefik-domeneshop
docker build --tag traefik-ds .
```

Obtain a token and secret from [Domeneshop API keys page](https://domene.shop/admin?view=api). 

Create a container with the new image according to e.g. 
[these instructions](https://www.smarthomebeginner.com/traefik-2-docker-tutorial)
and ensure the following environment variables are set:
- DOMENESHOP_TOKEN
- DOMENESHOP_SECRET
