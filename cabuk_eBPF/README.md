# Cabuk et al. Algorithm - eBPF Version

The algorithm developed by Cabuk et al. [1] calculates two different network traffic regularity measures, which can reveal the presence of network timing covert channels.
This repository contains the implementation of the first regularity measure in an online flavor using eBPF (through [BCC](https://github.com/iovisor/bcc)) .


# Basic Information and Usage
The first version of the implementation requires to tune different parameters, hard-coded within the python script:
- ```dev```: it specifies the interface to attack the eBPF filter.
- ```direction```: it specifies the direction (ingress, egress).
- ```WINDOW```: it specifies amount of packet per window.
- ```NUMBER_STD_CONSIDERED```: it specifies the amount of intermediate standard deviations to calculate before giving the final regularity measure.

After setting all the parameters, simply run the filter: 
```
python3 cabuk_eBPF
```

The regularity measure can be seen by checking the ```trace_pipe```:
```
cat /sys/kernel/debug/tracing/trace_pipe
```

# References

[1] S. Cabuk, C. E. Brodley, and C. Shields, “IP covert timing channels: Design and detection,” in Proceedings of the 11th ACM Conference on Computer and Communications Security. Association for Computing Machinery, 2004, pp. 178–187.




# Acknowledgement 

This work has been supported by EU Project [SIMARGL](https://simargl.eu) - Secure Intelligent Methods for Advanced Recognition of Malware and Stegomalware, Grant Agreement No 833042.
