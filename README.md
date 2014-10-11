netproxy
========

netproxy is a Netflix/Hulu/Pandora/etc proxy in a box. Simply build the Docker image on a US server and set your
computer's DNS server IP to it, and enjoy your favorite US-only sites.

Running
--------

Running netproxy is easy. If you have Docker installed, just clone the repository and run:

    docker build -t skorokithakis/netproxy .

This will build the image. Once it's done, run:

    docker run -p 53:53/udp -p 80:80 -p 443:443 -d skorokithakis/netproxy

and that's pretty much it! You are now ready to connect to it.
