#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import struct

# We want to save the row and column amount
def grab_shape(line):
	matrix = []
	count = 0
	for value in line.split(","):
		matrix.append(remove_extra_characters(value))
		count += 1
	return matrix[0], matrix[count-1]

# Removes unwanted characters from the string
def remove_extra_characters(value):
	value = value.translate({ord(i): None for i in "dtshpeary[]():' ''\n'"})
	return value

# Turns e+/-xx into its numerical format
def create_multiplier(multiplier):
	values = list(multiplier)
	power = values[2].join(values[1])
	if values[0] == "-":
		return 10**-int(power)
	if values[0] == "+":
		return 10**int(power)

def float_to_hex(f):
  return hex(struct.unpack('<I', struct.pack('<f', f))[0])

# Write the final hexadecimal value to the specified file
def write_to_file(value, multiplier, dest):
	value = float(value)
	multiplier = float(create_multiplier(remove_extra_characters(multiplier)))
	final_value = value * multiplier
	hex_value = float_to_hex(final_value)
	dest.write("%s "%(hex_value))

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('--file', dest='file', type=str,
                      default='file', help='File to be converted.')
	parser.add_argument('--dest', dest ='dest', type = str,
											default='dest', help='Where to write converted values')
	args = parser.parse_args()
	file = open(args.file, "r")
	dest = open(args.dest, "w+")
	fileLines = file.readlines()
	count = 0

	# Go through each line
	for line in fileLines:

		# First two lines are not useful
		if count == 0 or count == 1:
			count += 1
			continue

		# Grab shape of matrix
		if count == 2:
			row, column = grab_shape(line)
			dest.write("%s\n" %(row))
			dest.write("%s\n" %(column))
			count += 1
			continue

		# Grab values, convert to hex and save to file
		for values in line.split(","):
			if values not in ['\n', '\r\n']:
				value, multiplier = values.split("e")
				value = remove_extra_characters(value)
				if value != '':
					write_to_file(value, multiplier, dest)

	file.close()
	dest.close()

if __name__ == '__main__':
   main()
