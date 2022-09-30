# BCCSIMARGLToolkit

BCCSIMARGLToolkit can be used to process data collected by [eBPF Framework](https://github.com/Ocram95/eBPF-Framework)[1] tool. Processed data can be used to spot the presence of network covert channels.
It consists of three different Python3 scripts, within "/sources" directory. 
Each script process data in a different manner:
- ```heatmap_generator.py```: it creates heatmaps according to the evolution of the bins filled by [eBPF Framework](https://github.com/Ocram95/eBPF-Framework)[1] tool. 
- ```process_data_bins_changed.py```: it processes data to obtain the number of bins changed between subsequent/adjacent bins.
- ```process_data_bins_diff_zero.py```: it processes data to obtain the number of bins different from zero, i.e., filled with at least one value. It is possible to define a window to split the data in terms of number of samples or a time period.


# Dependencies
- Pandas:
```pip3 install pandas```
- Numpy:
```pip3 install numpy```
- Matplotlib:
```pip3 install matplotlib```


# Basic Usage
Let's take a look at the parameters of the ```heatmap_generator.py``` script: 
```
$ python3 heatmap_generator.py [-h HELP] [-r CSV]
```

- ```-r CSV```: it specifies the raw .csv file to read and to convert into a heatmap.

The ```process_data_bins_changed.py``` script: 
```
$ python3 process_data_bins_changed.py [-h HELP] [-r CSV] [-w OUTPUT] 
```

- ```-r CSV```: it specifies the raw .csv file to read.
- ```-w OUTPUT```: it specifies the name of the output file.

The ```process_data_bins_diff_zero.py``` script: 
```
$ python3 process_data_bins_diff_zero.py [-h HELP] [-r CSV] [-s SAMPLE] [-t TIME] [-w OUTPUT] 
```

- ```-r CSV```: it specifies the raw .csv file to read.
- ```-s SAMPLE```: it specifies how many samples keep in the window.
- ```-t TIME```: it specifies the time period of the window.
- ```-w OUTPUT```: it specifies the name of the output file.

## Example Usages
```
$ python3 heatmap_generator.py -r ../csv_examples/heatmap_test.csv
```
This command reads the raw input data file and generates a heatmap. An example is showcased in the figure below. 

<p align="center">
  <img src="https://github.com/Ocram95/BCCSIMARGLToolkit/blob/main/charts_examples/heatmap.png" width="500" />
</p>

```
$ python3 process_data_bins_diff_zero.py -r ../csv_examples/number_of_bins_diff_zero.csv -t 30 -w example.csv
```
This command reads the raw input data and generates an "example.csv" file where each line represents a window of 30 seconds. For each window, the number of bins different from zero is specified. Data can be plotted to obtain useful charts. An example is showcased below.

<p align="center">
  <img src="https://github.com/Ocram95/BCCSIMARGLToolkit/blob/main/charts_examples/diff_zero.png" width="500" />
</p>

```
$ python3 process_data_bins_changed.py -r ../csv_examples/number_of_bins_changed.csv -w example.csv
```

This command reads the raw input data and generate am "example.csv" file. For each line, the number of bins changed between two consecutive/adjacent sampling interval is specified. Data can be plotted to obtain useful charts. An example is showcased below.

<p align="center">
  <img src="https://github.com/Ocram95/BCCSIMARGLToolkit/blob/main/charts_examples/changed_bins.png" width="500" />
</p>

The .csv files are generated with the [eBPF Framework](https://github.com/Ocram95/eBPF-Framework)[1]. The traffic was generated using IPv6 network covert channels via [IPv6CC](https://github.com/Ocram95/IPv6CC_SoftwareX)[2].

## Tools

[1] eBPF-Framework: https://github.com/Ocram95/eBPF-Framework <br>
[2] IPv6CC: https://github.com/Ocram95/IPv6CC_SoftwareX


# Acknowledgement 

This work has been supported by EU Project [SIMARGL](https://simargl.eu) - Secure Intelligent Methods for Advanced Recognition of Malware and Stegomalware, Grant Agreement No 833042 and [ASTRID](https://www.astrid-project.eu) - AddreSsing ThReats for virtualIseD services, Grant Agreement No. 786922.
