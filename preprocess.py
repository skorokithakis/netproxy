#!/usr/bin/env python

import argparse
import json
import re
import string
import random
import urllib2


def main(external_ip=None):
    print("Downloading configuration...")

    # Download TSDU's config.json.
    json_config = urllib2.urlopen("https://raw.githubusercontent.com/trick77/tunlr-style-dns-unblocking/master/config.json").read()

    # Remove comments.
    json_config = re.sub("//.*", "", json_config, re.MULTILINE)
    config = json.loads(json_config)

    if external_ip is None:
        # Add our IP.
        try:
            print("Autodetecting external IP address...")
            external_ip = urllib2.urlopen("http://checkip.dyndns.org/").read()
            external_ip = re.search("IP Address: (.*?)<", external_ip).group(1)
            print("Detected external IP as %s, using that. If it's wrong, please replace it in config.json before building." % external_ip)
        except:
            print("Could not detect external IP. Please change the haproxy_bind_ip setting in config.json before building.")
            external_ip = "YOUR IP HERE"

    config["haproxy_bind_ip"] = external_ip

    # Change the stats password.
    config["stats"]["password"] = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(8))

    print("HAProxy stats password is %s, please make a note of it." % config["stats"]["password"])

    # Write it out.
    open("config.json", "w").write(json.dumps(config, sort_keys=True, indent=2, separators=(',', ': ')))

    print("Creating hosts file...")

    # Create the hosts file lines.
    lines = ["%s %s\n" % (config["haproxy_bind_ip"], proxy["dest_addr"]) for proxy in config["proxies"]]

    hosts = open("hosts", "w")
    hosts.write("\n\n# netproxy IP section\n")
    hosts.writelines(lines)
    hosts.close()

    print("Done!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Preprocess the netproxy config.")
    parser.add_argument("-e", "--externalip", metavar="IP", type=str, help="The external IP of the server (autodetected if not specified)")
    args = parser.parse_args()
    main(external_ip=args.externalip)
