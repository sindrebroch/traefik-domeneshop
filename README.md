# traefik-domeneshop
Extension to traefik docker image with script to enable LetsEncrypt DNS-01 challenges for Domeneshop

## Usage
1. Clone repo to your docker host.
2. `cd traefik-domeneshop`
3. `docker build --tag traefik-ds .`
4. Run docker with the following environment variables set:
  - DOMENESHOP_TOKEN
  - DOMENESHOP_SECRET

