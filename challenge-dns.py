#!/usr/bin/env python3
#
# Simple script to perform Let's Encrypt dns challenge to Domeneshop using lego.
# 
# Documentation of functionality:  https://go-acme.github.io/lego/dns/exec/
# Domeneshop API documentation:    https://api.domeneshop.no/docs/
# 
# Copyright 2020 Einar S. Idsø
# License: Unlicense <https://unlicense.org>
# 

import os
import sys
from domeneshop import Client

def main():
    token = os.getenv("DOMENESHOP_TOKEN")
    secret = os.getenv("DOMENESHOP_SECRET")

    if token is None:
        raise RuntimeError("DOMENESHOP_TOKEN not in environment")
    if secret is None:
        raise RuntimeError("DOMENESHOP_SECRET not in environment")

    client = Client(token, secret)

    if len(sys.argv) != 4:
        raise ValueError(
            "Incorrect arguments. Correct syntax:\n"
            f"{sys.argv[0]} <present|cleanup> <fqdn> <value>\n"
            "or"
            f"{sys.argv[0]}"
        )

    action, fqdn, value = sys.argv[1:]

    fqdn = fqdn.rstrip(".")  # Remove fqdn trailing dot from lego call

    if action == "present":
        present(client, fqdn, value)
    elif action == "cleanup":
        cleanup(client, fqdn, value)
    elif action == "timeout":
        timeout()    
    else:
        raise ValueError('First argument must be "present", "cleanup" or "timeout"')


def present(c, fqdn, value):
    domain = get_domain(c, fqdn)
    host = fqdn.replace(domain["domain"], "", 1).rstrip(".")
    record = { "host": host, "ttl": 600, "type": "TXT", "data": value }
    c.create_record(domain["id"], record)


def cleanup(c, fqdn, value):
    domain = get_domain(c, fqdn)
    host = fqdn.replace(domain["domain"], "", 1).rstrip(".")
    record = get_record(c, domain["id"], host, value)
    c.delete_record(domain["id"], record["id"])


def get_domain(c, fqdn):
    domains = c.get_domains()
    domain = [d for d in domains if fqdn.endswith(d["domain"])]
    if len(domain) != 1:
        raise ValueError(
            f"{fqdn} does not exclusively match available domains "
            f"{[d['domain'] for d in domains]}"
        )
    return domain[0]


def get_record(c, domain_id, fqdn, value):
    records = c.get_records(domain_id)
    record = [r for r in records if r["host"] == fqdn and r["data"] == value]
    if len(record) != 1:
        raise ValueError(
            f"{fqdn}, {value} does not exclusively match available records:\n"
            f"{records}"
        )
    return record[0]


def timeout():
    propagation_timeout = os.getenv("EXEC_PROPAGATION_TIMEOUT")
    polling_interval = os.getenv("EXEC_POLLING_INTERVAL")
    if propagation_timeout and polling_interval:
        print(f'{{ "timeout": {propagation_timeout}, "interval": {polling_interval} }}')

if __name__ == "__main__":
    main()
