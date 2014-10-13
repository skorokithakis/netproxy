#!/usr/bin/env python

import json
import re
import urllib2

print("Downloading configuration...")

# Download TSDU's config.json.
json_config = urllib2.urlopen("https://raw.githubusercontent.com/trick77/tunlr-style-dns-unblocking/master/config.json").read()

# Remove comments.
json_config = re.sub("//.*", "", json_config, re.MULTILINE)
config = json.loads(json_config)

# Add our IP.
try:
    external_ip = urllib2.urlopen("http://checkip.dyndns.org/").read()
    external_ip = re.search("IP Address: (.*?)<", external_ip).group(1)
    print("Detected external IP as %s, using that. If it's wrong, please replace it in config.json before building." % external_ip)
    config["haproxy_bind_ip"] = external_ip
except:
    print("Could not detect external IP. Please change the haproxy_bind_ip setting in config.json before building.")

# Write it out.
open("config.json", "w").write(json.dumps(config, sort_keys=True, indent=2))

print("Creating hosts file...")

# Create the hosts file lines.
lines = ["%s %s\n" % (config["haproxy_bind_ip"], proxy["dest_addr"]) for proxy in config["proxies"]]

hosts = open("hosts", "w")
hosts.write("\n\n# netproxy IP section\n")
hosts.writelines(lines)
hosts.close()

print("Done!")
