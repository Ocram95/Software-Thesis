import pandas as pd
import math
import matplotlib.pyplot as plt
import csv
import sys
import optparse


def process_command_line(argv):
	parser = optparse.OptionParser()
	parser.add_option(
		'-r',
		'--csv',
		help='Specify the eBPF csv to read.',
		action='store',
		type='string',
		dest='csv')


	settings, args = parser.parse_args(argv)
		
	if not settings.csv:
		raise ValueError("The eBPF csv file must be specified.")


	return settings, args

def read_and_process(data):
	read_data = pd.read_csv(data, header=None)
	time_col = read_data.pop(read_data.columns[0])
	data_diff = read_data.diff()
	data_diff['DIFF'] = data_diff.gt(0).sum(axis=1)
	data_diff.insert(0, "timestamp", time_col, True)
	return data_diff


def tmp_plot(data):
	fig, ax = plt.subplots()
	ax.plot(data["timestamp"], data["DIFF"], label='your label')
	ax.set_ylabel('no. of bins changed')
	ax.set_xlabel('time [s]')
	ax.legend()
	plt.grid()
	plt.show()


settings, args = process_command_line(sys.argv)
processed_data = read_and_process(settings.csv)
tmp_plot(processed_data)