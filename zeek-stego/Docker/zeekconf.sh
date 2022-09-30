#!/bin/bash
set -e

# List of variables managed for this configuration file
variables="MONITORED_FIELD BASEBIN DUMP_INTERVAL"

if test -f /etc/default/zeek-stego; then
	. /etc/default/zeek-stego

	# Use default values for variables not instantiated at runtime
	for var in $variables; do
		if [ -z ${!var} ]; then
			default=d$var
			eval "$var"=${!default}
		fi
	done
	
	# Update the configuration file/app
	for var in $variables; do
		sed -ie "s/$var/${!var}/g" /root/stego.zeek
	done
	
fi

#echo "Current ue settings: "
#for var in $variables; do
#	echo $var ": " ${!var}
#done
#echo 

exec $@

