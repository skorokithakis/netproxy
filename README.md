netproxy
========

netproxy is a Netflix/Hulu/Pandora/etc proxy in a box. Simply build the Docker image on a US server, set your
computer's DNS IP to it, and enjoy your favorite US-only sites.

netproxy uses the excellent `tunlr-style-dns-unblocking` script to do the heavy lifting, calling it behind the scenes
to set up a Docker container:

https://github.com/trick77/tunlr-style-dns-unblocking/

Running
--------

Running netproxy is easy. If you have Docker installed, just clone the repository *on your server*, run the
`preprocess.py` script:

    python preprocess.py

What this will do is download TSDU's config.json file, change a few entries and write it out, for the Dockerfile to
use. It will also autodetect your server's IP and write it in the config file, so make sure you double-check that and
change it if it's wrong, before building the image with:

    docker build -t skorokithakis/netproxy .

Once building is done, run:

    docker run -p 53:53/udp -p 80:80 -p 443:443 -d skorokithakis/netproxy

and that's pretty much it! You are now ready to connect to it. Set your computer's primary DNS server to your server's
IP, and you can watch all the Netflix you want.

Caveats
-------
There are two problems with this setup:

1) Running a DNS server exposed to the entire internet is a very bad idea.
2) Setting your primary DNS to a server in the US will slow your internet down significantly.

To avoid these problems, you can change your hosts file to point everything to your netproxy IP, and you can omit
forwarding port 53. That means you should run docker like so:

    docker run -p 80:80 -p 443:443 -d skorokithakis/netproxy

which should be much safer and faster. The hosts file entries will be generated when you run `preprocess.py` in the
directory of the script, so just append them to your normal hosts file *on your local machine* (the one you want to
watch on) like so:

    sudo cat hosts >> /etc/hosts

And everything should now go through the proxy.
