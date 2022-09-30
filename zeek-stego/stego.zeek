module ipstego;

export {
	redef enum Log::ID += { LOG };
	
	type Counters: record {
		ts:		time &log;
		values:	string &log;
	};
}

#################################
# Configuration goes here!!!    #
#################################
# Possible values: "fl=Flow Label; tc=Traffic Class; hl=Hop Limit; ack=TCP Ack num"
global field="ack";
# Number of bins to use (namely, the number of bins will be 2^N)
global N = 8;
# Interval for printing the results (in seconds)
global dump_interval = 3sec;
#################################

# For now, I use a single counter to be directly comparable with bccstego
#global fl_counters: vector of count;
#global tos_counters: vector of count;
#global hl_counters: vector of count;
global field_counters: vector of count;

global FL: count;
global n_bins: count;
global first: bool;

event dump_counters() 
{
	schedule dump_interval { dump_counters() };

	# Skip the first event because it is not correctly synchronized
	if ( first == T ) {
		first = F;
		return;
	}

#	print field_counters;
	local dump: string;
	dump = cat(field_counters);
	Log::write(ipstego::LOG, [$ts=current_time(), $values=dump]);
}

function update_counters(f: count)
{
	#print "oh: ", f;

	if( FL >= N ) {
		local b = CNR::shift_right(f, FL-N);
		++field_counters[b];
		print "Current bin: ", b, "Value: ", field_counters[b]; 
	}
}

event zeek_init()
{
	first=T;

	switch field {
		case "fl":
			FL=20;
			break;
		case "tc":
			fallthrough;
		case "hl":
			FL=8;
			break;
		case "ack":
			FL=32;
			break;
		default:
			FL=0;
			print "Invalid field name -- reporting is disabled!";
			break;
	}
		
	n_bins=CNR::cpow(2,N);
	local b=0;
	while (b<n_bins) {
#		fl_counters[b]=0;
#		tos_counters[b]=0;
#		hl_counters[b]=0;
		field_counters[b]=0;
		++b;
	}

	# Create the logging stream
	Log::create_stream(LOG, [$columns=Counters, $path="stego-counters"]);
	schedule dump_interval { dump_counters() };

}


event tcp_ack(c: connection, ack: count) {
	if( field=="ack" ) 
		update_counters(ack);
}

event ip_packet(fl: count, tos: count, hl: count) {
	# Uncomment this line to debug
	# print "fl: ", fl, "tos: ", tos, "hl: ", hl;
	local f: count;

	switch field {
		case "fl":
			f=fl;
			break;
		case "tc":
			f=tos;
			break;
		case "hl":
			f=hl;
			break;
		case "ack":
			break;
		default:
			print "Invalid field name -- reporting is disabled!";
			break;
	}

	if( field != "ack" )
		update_counters(f);
}

