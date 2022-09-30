#!/usr/bin/python3
from bcc import BPF
from pyroute2 import IPRoute
from pr2modules.netlink.exceptions import NetlinkError
import time


dev = "your_dev"
ipr = IPRoute()
idx = ipr.link_lookup(ifname=dev)[0]
#direction = "ingress"
direction = "egress"
try:
    ipr.tc("add", "clsact", idx, "ffff:")
    print("adding")
except NetlinkError as err:
    if err.code == 17:
        print("Skipping creation of clsact qdisc on " + dev)

bpfprog = """
#include <linux/pkt_cls.h>
#define WINDOW 100
#define NUMBER_STD_CONSIDERED 8
#define INDEX (NUMBER_STD_CONSIDERED*(NUMBER_STD_CONSIDERED-1))/2

BPF_ARRAY(packet_counter, u64, 1);
BPF_ARRAY(arrival_times, u64, WINDOW);
BPF_ARRAY(interarrival_times, u64, WINDOW);
BPF_ARRAY(std_array, u64, 100);
BPF_ARRAY(std_counter, u64, 100);
BPF_ARRAY(std_differences, long long, INDEX);

static unsigned long long square_root(unsigned long long x)
{
    unsigned long long guess = 1;
    for (int i = 0; i < 100; i++){
        guess = (x/guess + guess)/2;
    }
    return guess;
}

int cabuk(struct __sk_buff *skb){
    u64 now;
    now = bpf_ktime_get_ns();
    int index_zero = 0;
    u64 zero_value_u64 = 0;
    unsigned long long* packet_index = packet_counter.lookup(&index_zero);
    //If the pointer exists
    if (packet_index){
        arrival_times.update((int*)packet_index, &now);
    }
    packet_counter.increment(index_zero);

    if (packet_index){
        if((*packet_index) % WINDOW == 0){
            packet_counter.update(&index_zero, &zero_value_u64);

            int general_index = 1;
            int interarrival_time_index = 0;
            unsigned long long sum = 0;

            for (int i = 0; i < WINDOW; i++){
                unsigned long long* packet_time1 = arrival_times.lookup(&general_index);
                general_index--;
                unsigned long long* packet_time2 = arrival_times.lookup(&general_index);
                general_index = general_index + 2;
                if (packet_time1 && packet_time2){
                    unsigned long long interarrival_time = *packet_time1-*packet_time2;
                    interarrival_times.update(&interarrival_time_index, &interarrival_time);
                    interarrival_time_index++;
                    sum += interarrival_time;
                }
            }
            
            unsigned long long average = sum / (WINDOW-1);
            unsigned long long sum_for_dev = 0;
            unsigned long long* tmp = 0;
            unsigned long long difference = 0;
            unsigned long long difference_difference = 0;
            int general_index_interarrival_times = 0;
            for (int j = 0; j < WINDOW - 1; j++){
                tmp = interarrival_times.lookup(&general_index_interarrival_times);
                general_index_interarrival_times++;
                if (tmp){
                    difference = *tmp-average;
                    difference_difference = difference*difference;
                    sum_for_dev += difference_difference;
                }
            }
            unsigned long long var = sum_for_dev/(WINDOW-1);
            unsigned long long  sqm = square_root(var);
            unsigned long long* sqm_index = std_counter.lookup(&index_zero);
            if (sqm_index){
                std_array.update((int*)sqm_index, &sqm);
                std_counter.increment(index_zero);

                if ((*sqm_index % NUMBER_STD_CONSIDERED) == 0){
                    std_counter.update(&index_zero, &zero_value_u64);
                    int general_index_sqm1 = 0;
                    int general_index_sqm2 = 0;
                    int general_index_differences = 0;
                    
                    unsigned long long average_differences = 0;
                    for (int i = 0; i < NUMBER_STD_CONSIDERED; i++){
                        long long difference = 0;
                        general_index_sqm1 = i;

                        unsigned long long* sqm_tmp1 = std_array.lookup(&general_index_sqm1);
                        if (sqm_tmp1) {
                            for (int j = i+1; j < NUMBER_STD_CONSIDERED; j++){
                                general_index_sqm2 = j;
                                unsigned long long* sqm_tmp2 = std_array.lookup(&general_index_sqm2);
                                if (sqm_tmp2) {
                                    difference = *sqm_tmp1 - *sqm_tmp2;
                                    if (difference < 0)
                                        difference = -difference;
                                    std_differences.update(&general_index_differences, &difference);
                                    general_index_differences++;
                                    average_differences += difference;
                                }
                            }  
                        }
                    }
                    
                    average_differences = average_differences/INDEX;
                    unsigned long long final_sum = 0;
                    unsigned long long* tmp_final = 0;
                    unsigned long long tmp_diff_final = 0;
                    unsigned long long tmp_diff_tmp_diff_final = 0;
                    int general_index_final = 0;
                    
                    for (int i = 0; i < INDEX; i++){
                        tmp_final = std_differences.lookup(&general_index_final);
                        general_index_final++;
                        if (tmp_final){
                            tmp_diff_final = *tmp_final-average_differences;
                            tmp_diff_tmp_diff_final = tmp_diff_final*tmp_diff_final;
                            final_sum += tmp_diff_tmp_diff_final;
                        }
                    }
                    unsigned long long final_var = final_sum/INDEX;
                    unsigned long long final_sqm = square_root(final_var);
                    bpf_trace_printk("Regularity Measure: %llu", final_sqm);
                }
            }
        }
    }
    return TC_ACT_OK;
}
"""

prog = BPF(text=bpfprog)
fn = prog.load_func("cabuk", BPF.SCHED_CLS)
if direction == "ingress":
    ipr.tc("add-filter", "bpf", idx, ":1", fd=fn.fd, name=fn.name,
            parent="ffff:fff2", classid=1, direct_action=True)
else:
    ipr.tc("add-filter", "bpf", idx, ":1", fd=fn.fd, name=fn.name,
            parent="ffff:fff3", classid=1, direct_action=True)

try:
    while True:
        time.sleep(5)
except KeyboardInterrupt:
    ipr.tc("del", "clsact", idx, "ffff:")
    print("removing")
    exit()

