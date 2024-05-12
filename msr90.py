#!/usr/bin/env python
# MSR90 Magnetic Stripe Reader - Developed by acidvegas in Python (https://git.acid.vegas/msr90)

import getpass
import re
import sys


def format_pan(pan: str) -> str:
	'''
	Format the Primary Account Number (PAN) by grouping the digits in sets of 4

	:param pan: The Primary Account Number (PAN) to format
	'''

	return ' '.join(pan[i:i+4] for i in range(0, len(pan), 4))


def format_exp_date(exp_date: str) -> str:
	'''
	Format the expiration date by to be MM/YY

	:param exp_date: The expiration date to format'''

	return exp_date[2:4] + '/' + exp_date[0:2]


def service_code_descriptions(digit, code):
	'''
	Get the description for the service code digit

	:param digit: The digit number (1, 2, or 3)
	:param code: The code value for the digit
	'''

	descriptions = {
		'1': {
			'1': 'International interchange OK',
			'2': 'International interchange, use IC (chip) where feasible',
			'5': 'National interchange only except under bilateral agreement',
			'6': 'National interchange only, use IC (chip) where feasible',
			'7': 'No interchange except under bilateral agreement (closed loop)',
			'9': 'Test'
		},
		'2': {
			'0': 'Normal',
			'2': 'Contact issuer via online means',
			'4': 'Contact issuer via online means except under bilateral agreement'
		},
		'3': {
			'0': 'No restrictions, PIN required',
			'1': 'No restrictions',
			'2': 'Goods and services only (no cash)',
			'3': 'ATM only, PIN required',
			'4': 'Cash only',
			'5': 'Goods and services only (no cash), PIN required',
			'6': 'No restrictions, use PIN where feasible',
			'7': 'Goods and services only (no cash), use PIN where feasible'
		}
	}

	return descriptions[str(digit)].get(code, 'Unknown')


def parse_magnetic_stripe(data: str):
	'''
	Parse the magnetic stripe data and print the results

	:param data: The raw magnetic stripe data to parse
	'''

	# Patterns for specific track data parsing
	track1_pattern = r'^%([AB])(\d{1,19})\^([^\^]{2,26})\^(\d{4})(\d{3})([^\?]*?)\?(\w?)'
	track2_pattern = r';(\d{1,19})=(\d{4})(\d{3})(.*?)\?$'

	# Generic patterns to capture raw data if specific parsing fails
	generic_track1_pattern = r'(%[AB][^\?]+\?)'
	generic_track2_pattern = r'(;[^\?]+\?)'
	generic_track3_pattern = r'(\+[^\?]+\?)'

	# Attempt to match the track data
	track1_match = re.search(track1_pattern, data)
	track2_match = re.search(track2_pattern, data)
	track3_match = re.search(generic_track3_pattern, data)

	# Track 1 specific parsing
	if track1_match:
		format_code, pan, name, exp_date, service_code, discretionary_data, lrc = track1_match.groups()
		if format_code == 'A':
			print('Error: Unsupported format code \'A\'. Exiting.')
			sys.exit(1)
		formatted_pan = format_pan(pan)
		formatted_exp_date = format_exp_date(exp_date)
		desc1 = service_code_descriptions(1, service_code[0])
		desc2 = service_code_descriptions(2, service_code[1])
		desc3 = service_code_descriptions(3, service_code[2])
		print_fields('Track 1 Data', [
			('Format Code', f'{format_code} - Financial cards (ISO/IEC 7813)'),
			('Primary Account Number (PAN)', formatted_pan),
			('Cardholder Name', name),
			('Expiration Date', formatted_exp_date),
			('Service Code Digit 1', f'{service_code[0]}: {desc1}'),
			('Service Code Digit 2', f'{service_code[1]}: {desc2}'),
			('Service Code Digit 3', f'{service_code[2]}: {desc3}'),
			('Discretionary Data', discretionary_data),
			('LRC (optional)', lrc),
			('Raw Track Data', track1_match.group(0))
		], '\033[93m')

	# Fallback generic track 1
	elif re.search(generic_track1_pattern, data):
		print('Track 1 Data:')
		print('Raw: ' + re.search(generic_track1_pattern, data).group(1))

	print('\n')

	# Track 2 specific parsing
	if track2_match:
		pan, exp_date, service_code, discretionary_data = track2_match.groups()
		formatted_pan = format_pan(pan)
		formatted_exp_date = format_exp_date(exp_date)
		print_fields('Track 2 Data', [
			('Primary Account Number (PAN)', formatted_pan),
			('Expiration Date', formatted_exp_date),
			('Service Code', service_code),
			('Discretionary Data', discretionary_data),
			('Raw Track Data', track2_match.group(0))
		], '\033[96m')

	# Fallback generic track 2
	elif re.search(generic_track2_pattern, data):
		print('Track 2 Data:')
		print('Raw: ' + re.search(generic_track2_pattern, data).group(1))

	print('\n')

	# Track 3 generic data if found
	if track3_match:
		print('Track 3 Data:')
		print('Raw: ' + track3_match.group(1))
	else:
		print('Track 3 Data: No data found.')


def print_fields(title: str, fields: list, color_code: str):
	'''
	Print the fields in a formatted table

	:param title: The title of the table
	:param fields: The fields to print
	:param color_code: The color code to use for the table
	'''

	max_len = max(len(name) for name, _ in fields)

	print(title)

	for name, value in fields:
		print(color_code + name.ljust(max_len) + '\033[90m | \033[0m' + value)



if __name__ == '__main__':
	try:
		swipe_data = getpass.getpass(prompt='Please swipe the card: ')
		parse_magnetic_stripe(swipe_data)
	except Exception as e:
		print('Error:', e)
