import math
import matplotlib.pyplot as plt
import pandas as pd
import sys
import optparse


def process_command_line(argv):
	parser = optparse.OptionParser()
	parser.add_option('-r', '--csv', help='Specify the eBPF csv to read.', action='store', type='string', dest='csv')

	settings, args = parser.parse_args(argv)
		
	if not settings.csv:
		raise ValueError("The eBPF csv file must be specified.")

	return settings, args

settings, args = process_command_line(sys.argv)
read_data = pd.read_csv(settings.csv)
read_data = read_data.drop(read_data.columns[0], axis=1)
plt.imshow(read_data, cmap='plasma',interpolation='nearest')

plt.show()