# libpcap Filter

This program leverages the libpcap C/C++ library and it allows to collect data and statistics for the protocols/fields that can be likely used for creating covert channels. Currently, the filter supports the following protocols/fields:

- ```IPv6```: ```Flow Label```, ```Traffic Class```, ```Hop Limit```, ```Next Header```, ```Payload Length```;
- ```IPv4```: ```Type of Service```, ```Identification Number```, ```Time To Live```, ```Fragment Offset```;
- ```TCP```: ```Acknowledgement Number```,  ```Reserved Bits```;
- ```UDP```: ```Checksum```. 

The program is designed to be easily extended for considering other protocols and fields by simply adding  cascading ```if-case``` conditions in the main function. 



The implementation is composed of a single C program, in charge of opening the network device for packet live capturing, retrieving packets, parsing them according to the parameters set by the user and updating a bin-based data structure. 

# Usage
To compile the filter:

```
sudo gcc libpcap_filter.c -lpcap -lm -o libpcap_filter
```

To run the filter:

```
sudo ./libpcap_filter [field] [#bins] [interface] [polling interval] [output.csv]
```

where:

-```[field]```: it specifies the field to inspect (```FL, TC, HL, NH, PL, ACK6, RES6, CHECK6, TOS, TTL, ID, FO, ACK4, RES4, CHECK4```);

-```[#bins]```: it specifies the number of bins to use (a power of 2); 

-```[interface]```: it specifies the interface to monitor;

-```[polling interval]```: it specifies the interval to provide the results;

-```[output.csv]```: it specifies the output file to store the results.


Example usage:

```
sudo ./libpcap_filter HL 8 eth1 1 output.csv
```

This command execute the libpcap_filter file to monitor the Hop Limit field using 2^8 bins on the eth1 interface. The results are stored every 1 second in the output.csv file.

# References

[1] M. Zuppelli, A. Carrega, M. Repetto, "An Effective and Efficient Approach to Improve Visibility Over Network Communications", Journal of Wireless Mobile Networks, Ubiquitous Computing, and Dependable Applications (JoWUA), Vol. 12, No. 4, pp. 89-108, December 2021.




# Acknowledgement 

This work has been supported by EU Projects [SIMARGL](https://simargl.eu) - Secure Intelligent Methods for Advanced Recognition of Malware and Stegomalware, Grant Agreement No. 833042,  [ASTRID](https://www.astrid-project.eu) Grant Agreement No. 786922,  [GUARD](https://guard-project.eu) Grant Agreement No. 833456.
