FROM ubuntu:trusty

RUN apt-get update -qq && apt-get install -y software-properties-common
RUN add-apt-repository -y ppa:vbernat/haproxy-1.5
RUN apt-get update -qq && apt-get install -y haproxy dnsmasq iptables git php5-cli supervisor

RUN git clone https://github.com/trick77/tunlr-style-dns-unblocking.git tunlr

WORKDIR /tunlr/

ADD config.json /tunlr/
RUN php5 genconf.php pure-sni

RUN sed -i "s/\/dev\/log/127.0.0.1/" haproxy.conf
RUN sed -i "s/bind [0-9\.]\+/bind */" haproxy.conf
RUN sed -i "s/daemon//" haproxy.conf
RUN mv haproxy.conf /etc/haproxy/haproxy.cfg

RUN echo "user=root" >> /etc/dnsmasq.conf
RUN cat dnsmasq-haproxy.conf >> /etc/dnsmasq.conf

ADD supervisord/haproxy.conf /etc/supervisor/conf.d/
ADD supervisord/dnsmasq.conf /etc/supervisor/conf.d/

EXPOSE 53 80 443

CMD /usr/bin/supervisord -nc /etc/supervisor/supervisord.conf
