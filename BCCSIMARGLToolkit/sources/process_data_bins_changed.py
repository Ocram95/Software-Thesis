import pandas as pd
import math
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.font_manager import FontProperties
import csv
import sys
import optparse
import json
from datetime import datetime

def read_and_process(data):
    read_data = pd.read_csv(data, header=None)
    time_column = read_data.iloc[:,0].round(2)
    pre_processed_data = read_data.drop(read_data.columns[0], axis=1)
    data_diff = pre_processed_data.diff()
    data_diff['DIFF'] = data_diff.gt(0).sum(axis=1)
    data_diff.insert(0, "time", time_column, True)
    return data_diff


def tmp_plot(data):
	fig, ax = plt.subplots()
	ax.plot(data["time"].values, data['DIFF'], label='your label')
	ax.set_ylim(ymin=0)
	#ax.set_xlim(xmin=0, right=900)
	ax.set_ylabel('no. of bins changed')
	ax.set_xlabel('time [s]')
	ax.legend()
	plt.grid()
	plt.show()

def save_CSV(data, output_file_path):
	with open(output_file_path + ".csv", mode='w') as file:
	    writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
	    writer.writerow(['time', 'no. of bins changed'])
	    for x in range(len(data["time"].values)):
	        writer.writerow([str(data["time"].values[x]), str(data['DIFF'][x])])

def save_JSON(settings, data):
	field = "N/A"
	if "fl" in settings.csv:
		field = "Flow Label"
	elif "tc" in settings.csv:
		field = "Traffic Class"
	elif "hl" in settings.csv:
		field = "Hop Limit"

	test_dict = { "TOOL": "BCCSIMARGL Toolkit",
		"Analysis": "Number of changed bins",
		"File parsed": settings.csv,
		"Analysis Timestamp": str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
		"Field" : field, 
		"Data": { 
			"timestamp [s]": data["time"].to_list(),
			"number of changed bins": data["DIFF"].to_list()
		}
	 }

	with open(settings.output_file + ".json", 'w') as json_file:
		json.dump(test_dict, json_file)


def process_command_line(argv):
	parser = optparse.OptionParser()
	parser.add_option('-r', '--csv', help='Specify the eBPF csv to read.', action='store', type='string', dest='csv')
	parser.add_option('-w', '--output_file', help='Specify the path of the output file.', action='store', type='string', dest='output_file')

	settings, args = parser.parse_args(argv)
		
	if not settings.csv:
		raise ValueError("The eBPF csv file must be specified.")
	if not settings.output_file:
		raise ValueError("The output file path must be specified.")


	return settings, args

#MAIN
settings, args = process_command_line(sys.argv)
processed_data = read_and_process(settings.csv)
#save_CSV(processed_data, settings.output_file)
save_JSON(settings, processed_data)
#tmp_plot(processed_data)