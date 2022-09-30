import math
import matplotlib.pyplot as plt
import pandas as pd
import sys
import optparse
from matplotlib.colors import TwoSlopeNorm
from mpl_toolkits.axes_grid1 import make_axes_locatable


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

settings, args = process_command_line(sys.argv)
read_data = pd.read_csv(settings.csv)
read_data = read_data.drop(read_data.columns[0], axis=1)
norm = TwoSlopeNorm(vmin=0, vcenter=50, vmax=100)
fig = plt.figure()
ax1 = fig.add_subplot(1, 1, 1) #rows, column, index
im1 = ax1.imshow(read_data, cmap='plasma',interpolation='nearest', norm=norm)
divider = make_axes_locatable(ax1)
cax = divider.append_axes("right", size="5%", pad=0.1)
cbar = plt.colorbar(im1, cax=cax)

#plt.imshow(read_data, cmap='plasma',interpolation='nearest', norm=norm)

plt.show()