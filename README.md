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

and that's pretty much it! You are now ready to connect to it. Set your computer's primary DNS server to your server's
IP, and you can watch all the Netflix you want.

Caveats
-------
There are two problems with this setup:

1) Running a DNS server exposed to the entire internet is a very bad idea.
2) Setting your primary DNS to a server in the US will slow your internet down significantly.

To avoid these problems, you can change your hosts file to point everything to your netproxy IP (this is outside the
scope of this document), and you can omit forwarding port 53. That means you should run docker like so:

    docker run -p 80:80 -p 443:443 -d skorokithakis/netproxy

which should be much safer and faster.
