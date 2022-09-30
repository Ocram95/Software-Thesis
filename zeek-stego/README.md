# zeek-stego
Zeek extensions to detect covert channels in the IPv6 header. This work includes a patch to create events for each IP packet that report the value of header fields that could be used to bear covert channels, and a script to analyse them. In addition, a plugin is also provided with a few helper functions to analyse data. Zeek-stego currently reports statistics about Flow Label (IPv6 only), Traffic Class/Type of Service, Hop Limit/Time To Live fields of IPv4/IPv6 packets, Ack numbers (TCP). The output consists of the number of packets seen for given interval ranges. More in detail, the full range of possible values for a given field is partioned in a given number of intervals, and a counter keeps track of the number of packets which field value falls in each partition. It works the same way as <A href="https://github.com/mattereppe/bccstego">bccstego</A>, which is an alternative implementation of the same concept.

Zeek-stego is designed as a proof-of-concept for detecting covert channels in network protocol headers, but it is not conceived for running in production environments, because of the overhead in triggering events for each packet. If you are looking for a more efficient way of monitoring network packet headers, have a look at <A href="https://github.com/mattereppe/bccstego">bccstego</A>.

## Patch zeek source code

Clone the git repository of zeek.
See <A href="https://docs.zeek.org/en/master/install.html">instuctions</A>.

Enter the zeek folder and patch the code:
```Shell
% cd <zeek dir>/
% patch -p1 < stego.patch 
```

(Patch build from zeek commit 3dac5ed80.)

Configure, compile and install zeek as explained in the <A href="https://docs.zeek.org/en/master/install.html">documentation</A>.

## Install the plugins with utils

Enter the plugin directory and simply compile everything:
```Shell
% ./configure --zeek-dist=<path to zeek sources>
% make
% sudo make install
```

The last step is optional, but it avoids to specify the additional plugin with a shell variable

## Run zeek-stego

Configure the stego.zeek file according to the monitored IP header field. There is no specific configuration framework available, but some options can be changed directly in the stego.zeek script:
```Shell
#################################
# Configuration goes here!!!    #
#################################
# Possible values: "fl=Flow Label; tc=Traffic Class; hl=Hop Limit; ack=TCP Ack num"
global field="fl";
# Number of bins to use (namely, the number of bins will be 2^N)
global N = 8;
# Interval for printing the results (in seconds)
global dump_interval = 3sec;
#################################
```
The following parameters can be changed:
<ul>
  <li> <i>field</i> This is the name of the field to be monitored. See the above example for allowed values.
  <li> <i>N</i> affects the number of bins, namely the interval in which the whole value range for the monitored field is partitioned to create the statistical histogram. The real number of partions equals to 2^N. Mind that a larger number of bins improves the likelihood of detecting anomalies in field usage, but also increase the size of logs.
  <li> <i>dump_interval</i> is the number of seconds for updating the statistics.
</ul>

Run the provided script that creates statistics:
```Shell
% /usr/local/zeek/bin/zeek -C -i <interface> stego.zeek 
```
Note that the script could also be installed alongside the zeek installation tree, so it is executed every time zeek is started. 

Look for data in the stego-counters.log file. The name of the file can be changed in the stego.zeek script.

## Docker image

To facilitate the setup of the patched version, a docker image can be build with the scripts in the Docker folder. Enter the folder and run 
```Shell 
sudo docker build -t <image name:version> .
```
Once the image is built, configuration is possible through the following environmental variables:
```Shell
MONITORED_FIELD: allowed values: "fl", "tc", "hl"
BASEBIN: any value from 0 to field length (20 for Flow Label, 8 for Traffic Class and Hop Limit)
DUMP_INTERVAL: the interval for dumping data to the log file
```

The docker image saves data to the stego-counter.log file in the internal /root folder.

Note: building the docker image from scratch requires a long time (due to compilation of zeek).
