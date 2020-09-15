#!/usr/bin/env python3

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
            "Incorrect arguments. Correct syntax:"
            f"{sys.argv[0]} <present|cleanup> <fqdn> <value>"
        )

    action, fqdn, value = sys.argv[1:]
    # Lego appends a dot at the end. DS reports it as invalid, so remove.
    fqdn = fqdn.rstrip(".")

    if action == "present":
        present(client, fqdn, value)
    elif action == "cleanup":
        cleanup(client, fqdn, value)
    else:
        raise ValueError('First argument must be "present" or "cleanup"')


def present(c, fqdn, value):
    domain = get_domain(c, fqdn)
    # Seems like DS appends the domain to the fqdn. This causes the challenge
    # to fail, so better remove the domain from fqdn before creating the entry
    fqdn = fqdn.replace(domain["domain"], "", 1).rstrip(".")
    record = { "host": fqdn, "ttl": 600, "type": "TXT", "data": value }
    c.create_record(domain["id"], record)


def cleanup(c, fqdn, value):
    domain = get_domain(c, fqdn)
    fqdn = fqdn.replace(domain["domain"], "", 1).rstrip(".")
    record = get_record(c, domain["id"], fqdn, value)
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

if __name__ == "__main__":
    main()
