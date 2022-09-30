# A container for running standalone Zeek network analyzer.
#
# Copyright (c) 2021, The ASTRID Consortium
# All rights reserved
#

from debian:testing

# Download latest binaries for Debian
RUN apt-get update && \
	apt-get -y install git cmake make gcc g++ flex bison libpcap-dev libssl-dev python3 python3-dev swig zlib1g-dev && \
	cd /root/ && \
	git clone --recursive https://github.com/zeek/zeek && \
	git clone --recursive https://github.com/mattereppe/zeek-stego.git && \
	cd zeek && \
	patch -p1 < ../zeek-stego/stego.patch && \
	./configure && make && make install && \
	cd ../zeek-stego/chelpers-plugin/ && \
	./configure --zeek-dist=../../zeek/ && make && make install && \
	rm -rf zeek && \
	apt-get -y purge git cmake make gcc g++ flex bison python3-dev zlib1g-dev && \
	apt-get -y autoremove && \
	rm -rf /var/lib/apt/lists/* 

RUN cd /root/ && \
	cp zeek-stego/stego.zeek . && rm -rf zeek-stego

# This is quite a strange way, but I didn't want to change the original script nor
# to duplicate the stego.zeek file.
RUN sed -e 's/\(global field[ ]*=\).*/\1 "MONITORED_FIELD";/' \
	-e 's/\(global N[ ]*=\).*/\1 BASEBIN;/'  \
	-e 's/\(global dump_interval[ ]*=\).*/\1 DUMP_INTERVAL;/' -i /root/stego.zeek
COPY defaults /etc/default/zeek-stego
COPY zeekconf.sh /root/

WORKDIR /root/

ENTRYPOINT ["/root/zeekconf.sh"]

CMD ["/usr/local/zeek/bin/zeek", "-C", "-ieth0", "stego.zeek"]
