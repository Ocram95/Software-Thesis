import csv
import optparse
import sys
import json
from datetime import datetime


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

def CSV_to_JSON(csv_file):
	timestamps = []
	values = []
	with open(csv_file) as file:
		reader = csv.reader(file, delimiter=',')
		for rows in reader:
			timestamps.append(round(float(rows[0]), 2))
			values.append(rows[1:])
	return timestamps, values


def save_JSON(timestamps, data):
	field = "N/A"
	if "fl" in settings.csv:
		field = "Flow Label"
	elif "tc" in settings.csv:
		field = "Traffic Class"
	elif "hl" in settings.csv:
		field = "Hop Limit"

	test_dict = { "TOOL": "BCCSIMARGL Toolkit",
		"Analysis": "Heatmap values",
		"File parsed": settings.csv,
		"Analysis Timestamp": str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
		"Field" : field, 
		"Data": { 
			"timestamp [s]": timestamps,
			"number of changed bins": data
		}
	 }

	with open(settings.output_file, 'w') as json_file:
		json.dump(test_dict, json_file)


settings, args = process_command_line(sys.argv)
timestamps, data = CSV_to_JSON(settings.csv)
save_JSON(timestamps, data)


