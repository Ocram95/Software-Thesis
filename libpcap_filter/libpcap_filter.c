#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <stdio.h>
#include <pcap.h>
#include <arpa/inet.h>
#include <linux/if_ether.h>
//https://sites.uclouvain.be/SystInfo/usr/include/netinet/ip6.h.html
#include <netinet/ip6.h> 
//https://sites.uclouvain.be/SystInfo/usr/include/netinet/ip.h.html
#include <netinet/ip.h>

#include <netinet/tcp.h>
#include <netinet/udp.h>

#include <signal.h>
#include <string.h>
#include <sys/time.h>



#define MAX_NUMBER_OF_BINS 524288

int strcmp (const char* str1, const char* str2);

struct bin
{
    int lo;
    int hi;
    int counter;
};

int generate_bins(int max, int number_of_bins, struct bin bins[])
{
    int i;
    int min = 0;
    int bins_size[number_of_bins];

    int even_length = (max-min+1)/number_of_bins;

    for(i=0; i<number_of_bins; ++i)
        bins_size[i] = even_length;

    int surplus = (max-min+1)%number_of_bins;
    for(i=0; surplus>0; --surplus, i=(i+1)%number_of_bins)
        bins_size[i] += 1; 

    int n=0, k=min;
    for(i=0; i<number_of_bins && k<=max; ++i, ++n){
        bins[i].lo=k;
        bins[i].hi=k+bins_size[i]-1;
        k += bins_size[i];
        bins[i].counter = 0;
    }
    return n;
}

int increment_bin(unsigned int number, int number_of_bins, struct bin bins[]) {
    int i;
    for(i=0; i<number_of_bins; ++i)
        if(number >= bins[i].lo && number <= bins[i].hi){
            bins[i].counter = bins[i].counter + 1;
            return bins[i].counter;
        }
    return number_of_bins;
}

void print_bins(int number_of_bins, struct bin bins[]){
    for (int i = 0; i < number_of_bins; ++i)
    {
        printf("bins number: %d, counter: %d\n", i, bins[i].counter);
    }
}


struct sigaction old_action;
struct bin bins[MAX_NUMBER_OF_BINS];
int number_of_bins;
FILE *fpt;

void sigint_handler(int sig_no)
{
    printf("CTRL-C pressed\n");
    print_bins(number_of_bins, bins);
    fclose(fpt);
    sigaction(SIGINT, &old_action, NULL);
    kill(0, SIGINT);
}



void write_csv(float elapsed, int number_of_bins, struct bin bins[]){
    
    fprintf(fpt, "%f", elapsed);
    for (int i = 0; i < number_of_bins; ++i)
    {
        fprintf(fpt, ",%d", bins[i].counter);
    }
    fprintf(fpt, "\n");
}




int main(int argc, char *argv[]) {
    int i;
    char *target_field = argv[1];
    //int
    double field_size = 0;
    char *version = "0";

    //****************IPv6********************
    if(strcmp(target_field, "FL") == 0){
        field_size = pow(2, 20);
        version = "6";
    }
    else if(strcmp(target_field, "TC") == 0){
        field_size = pow(2, 8);
        version = "6";
    }
    else if(strcmp(target_field, "HL") == 0){
        field_size = pow(2, 8);
        version = "6";
    }
    else if(strcmp(target_field, "NH") == 0){
        field_size = pow(2, 8);
        version = "6";
    }
    else if(strcmp(target_field, "PL") == 0){
        field_size = pow(2, 16);
        version = "6";
    }
    else if(strcmp(target_field, "ACK6") == 0){
        field_size = pow(2, 32);
        version = "6";
    }
    else if(strcmp(target_field, "RES6") == 0){
        field_size = pow(2, 3);
        version = "6";
    }
    else if(strcmp(target_field, "CHECK6") == 0){
        field_size = pow(2, 16);
        version = "6";
    }
    //****************IPv4********************
    if(strcmp(target_field, "TOS") == 0){
        field_size = pow(2, 8);
        version = "4";
    }
    else if(strcmp(target_field, "TTL") == 0){
        field_size = pow(2, 8);
        version = "4";
    }
    else if(strcmp(target_field, "ID") == 0){
        field_size = pow(2, 16);
        version = "4";
    }
    else if(strcmp(target_field, "FO") == 0){
        field_size = pow(2, 13);
        version = "4";
    }
    else if(strcmp(target_field, "ACK4") == 0){
        field_size = pow(2, 32);
        version = "4";
    }
    else if(strcmp(target_field, "RES4") == 0){
        field_size = pow(2, 3);
        version = "4";
    }
    else if(strcmp(target_field, "CHECK4") == 0){
        field_size = pow(2, 16);
        version = "4";
    }

    number_of_bins = atoi(argv[2]);
    int n = generate_bins(field_size-1, number_of_bins, bins);

    struct sigaction action;
    memset(&action, 0, sizeof(action));
    action.sa_handler = &sigint_handler;
    sigaction(SIGINT, &action, &old_action);

    char *device = argv[3];

    int sampling_interval = atoi(argv[4]);

    char error_buffer[PCAP_ERRBUF_SIZE];
    int timeout_limit = 1000; //ms
    pcap_t *handle;

    handle = pcap_open_live(device, BUFSIZ, 1, timeout_limit, error_buffer);

    if (handle == NULL) {
        printf("Something went wrong:\n%s\n", error_buffer);
        return 1; // exit
    }

    unsigned char *packet;
    struct pcap_pkthdr header;
    unsigned int field = 0;

    char *output_file = argv[5];
    fpt = fopen(output_file, "w+");


    struct timeval begin, end;
    long seconds, microseconds = 0;
    double elapsed = 0;
    gettimeofday(&begin, 0);

    const struct tcphdr* tcpHeader;
    const struct udphdr* udpHeader;
    int ip6_header_length = 40;

    while (1){
        packet = (unsigned char *)pcap_next(handle, &header);
        if (packet != NULL){
            struct ethhdr *eth_h = (struct ethhdr*) packet;
            //IPv6
            if (strcmp(version, "6") == 0){
                if (ntohs(eth_h->h_proto) == ETH_P_IPV6) {
                    struct ip6_hdr *ipv6_h = (struct ip6_hdr*)(packet + sizeof(struct ethhdr));

                    if (strcmp(target_field, "FL") == 0){
                        field = (unsigned int)ntohl(ipv6_h->ip6_flow) & 0xfffff;
                    }
                    else if (strcmp(target_field, "TC") == 0){
                        int tmp =(unsigned int)ntohl(ipv6_h->ip6_flow) & 0xfffffff;
                        field = tmp>>20;
                    }
                    else if (strcmp(target_field, "HL") == 0){
                        field = ipv6_h->ip6_hlim;
                    }
                    else if (strcmp(target_field, "NH") == 0){
                        field = ipv6_h->ip6_nxt;
                    }
                    else if (strcmp(target_field, "PL") == 0){
                        field =(unsigned int)ntohs(ipv6_h->ip6_plen);
                    }
                    else if (strcmp(target_field, "ACK6") == 0){
                        if (ipv6_h->ip6_nxt == IPPROTO_TCP){
                            //https://www.programmersought.com/article/84345094178/
                            tcpHeader = (struct tcphdr*)(packet + 
                                sizeof(struct ethhdr) + ip6_header_length);
                            field = (unsigned int)ntohl(tcpHeader->ack_seq);
                        }
                    }
                    else if (strcmp(target_field, "RES6") == 0){
                        if (ipv6_h->ip6_nxt == IPPROTO_TCP){
                            tcpHeader = (struct tcphdr*)(packet + 
                                sizeof(struct ethhdr) + ip6_header_length);
                            field = tcpHeader->res1;
                        }
                    }
                    else if (strcmp(target_field, "CHECK6") == 0){
                        if (ipv6_h->ip6_nxt == IPPROTO_UDP){
                            udpHeader = (struct udphdr*)(packet + 
                                sizeof(struct ethhdr) + ip6_header_length);
                            field = (unsigned int)ntohs(udpHeader->check);
                        }
                    }
                    increment_bin(field, number_of_bins, bins); 
                }
            }
            //IPv4
            else if (strcmp(version, "4") == 0){
                if (ntohs(eth_h->h_proto) == ETH_P_IP) {

                    struct iphdr *ip_h = (struct iphdr*)(packet + sizeof(struct ethhdr));

                    if (strcmp(target_field, "TOS") == 0){
                        field = ip_h->tos;
                    }
                    else if (strcmp(target_field, "TTL") == 0){
                        field = ip_h->ttl;
                    }
                    else if (strcmp(target_field, "ID") == 0){
                        field = (unsigned int)ntohs(ip_h->id);
                    }
                    else if (strcmp(target_field, "FO") == 0){
                        field = (unsigned int)ntohs(ip_h->frag_off) & 0x1fff; //first 13 bits
                    }
                    else if (strcmp(target_field, "ACK4") == 0){
                        if (ip_h->protocol == IPPROTO_TCP){
                            //https://www.programmersought.com/article/84345094178/
                            printf("TCP packet\n");
                            tcpHeader = (struct tcphdr*)(packet + 
                                sizeof(struct ethhdr) + sizeof(struct ip));
                            field = (unsigned int)ntohl(tcpHeader->ack_seq);
                        }
                    }
                    else if (strcmp(target_field, "RES4") == 0){
                        if (ip_h->protocol == IPPROTO_TCP){
                            printf("TCP packet\n");
                            tcpHeader = (struct tcphdr*)(packet + 
                                sizeof(struct ethhdr) + sizeof(struct ip));
                            field = tcpHeader->res1;
                        }
                    }
                    else if (strcmp(target_field, "CHECK4") == 0){
                        if (ip_h->protocol == IPPROTO_UDP){
                            printf("UDP packet\n");
                            udpHeader = (struct udphdr*)(packet + 
                                sizeof(struct ethhdr) + sizeof(struct ip));
                            field = (unsigned int)ntohs(udpHeader->check);
                        }
                    }
                    increment_bin(field, number_of_bins, bins); 
                }
            }
        }

        seconds = end.tv_sec - begin.tv_sec;
        microseconds = end.tv_usec - begin.tv_usec;
        elapsed = (seconds + microseconds*1e-6);
        if((elapsed) >= (sampling_interval))
        {
            printf("DeltaT: %.5f\n", elapsed);
            write_csv(elapsed, number_of_bins, bins);
            begin.tv_sec = end.tv_sec;
            begin.tv_usec = end.tv_usec;
        }

        gettimeofday(&end,0);

    }

    return 0;
}