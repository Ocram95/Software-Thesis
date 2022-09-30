import math
import matplotlib.pyplot as plt
import pandas as pd
import sys
import optparse


def process_command_line(argv):
	parser = optparse.OptionParser()
	parser.add_option(
		'-r',
		'--csv',
		help='Specify the csv to read.',
		action='store',
		type='string',
		dest='csv')

	settings, args = parser.parse_args(argv)
		
	if not settings.csv:
		raise ValueError("The csv file must be specified.")

	return settings, args


def tmp_plot(number_of_bins_different_from_zero, ):
	fig, ax = plt.subplots()
	
	ax.plot(number_of_bins_different_from_zero["timestamp"], number_of_bins_different_from_zero["!=0"], label='your label')

	ax.set_ylabel('no. of bins != 0')
	ax.set_xlabel('time [s]')
	ax.legend()
	plt.grid()
	plt.show()


settings, args = process_command_line(sys.argv)
read_data = pd.read_csv(settings.csv, header=None)
#pop method remove and return a column
time_col = read_data.pop(read_data.columns[0])
number_of_bins_different_from_zero = read_data.astype(bool).sum(axis=1).to_frame(name="!=0")
number_of_bins_different_from_zero.insert(loc=0, column='timestamp', value=time_col)

tmp_plot(number_of_bins_different_from_zero)




