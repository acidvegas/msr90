#!/usr/bin/env python
# MSR90 Magnetic Stripe Reader - Developed by acidvegas in Python (https://git.acid.vegas/msr90)

import getpass
import re
import sys


# Define ANSI color codes
YELLOW = '\033[93m'
CYAN   = '\033[96m'
GRAY   = '\033[90m'
RESET  = '\033[0m'


def format_pan(pan: str) -> str:
	'''
	Format the Primary Account Number (PAN) by grouping the digits in sets of 4

	:param pan: The Primary Account Number (PAN) to format
	'''

	return ' '.join(pan[i:i+4] for i in range(0, len(pan), 4))


def format_exp_date(exp_date: str) -> str:
	'''
	Format the expiration date to be MM/YY

	:param exp_date: The expiration date to format
	'''

	return exp_date[2:4] + '/' + exp_date[0:2]


def service_code_descriptions(digit: int, code: str) -> str:
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

	track1_match = re.search(r'^%([AB])(\d{1,19})\^([^\^]{2,26})\^(\d{4})(\d{3})([^\?]*?)\?(\w?)', data)
	track2_match = re.search(r';(\d{1,19})=(\d{4})(\d{3})(.*?)\?$', data)
	track3_match = re.search(r'(\+[^\?]+\?)', data)

	if track1_match:
		format_code, pan, name, exp_date, service_code, discretionary_data, lrc = track1_match.groups()
		if format_code == 'A':
			raise ValueError('Track 1 data is using format code A which is not supported')
		formatted_pan = format_pan(pan)
		formatted_exp_date = format_exp_date(exp_date)
		desc1 = service_code_descriptions(1, service_code[0])
		desc2 = service_code_descriptions(2, service_code[1])
		desc3 = service_code_descriptions(3, service_code[2])
		print('Track 1 Data:')
		print(YELLOW + 'Format Code' + GRAY + '                  | ' + RESET + f'{format_code} - Financial cards (ISO/IEC 7813)')
		print(YELLOW + 'Primary Account Number (PAN)' + GRAY + ' | ' + RESET + formatted_pan)
		print(YELLOW + 'Cardholder Name' + GRAY + '              | ' + RESET + name)
		print(YELLOW + 'Expiration Date' + GRAY + '              | ' + RESET + formatted_exp_date)
		print(YELLOW + 'Service Code Digit 1' + GRAY + '         | ' + RESET + f'{service_code[0]}: {desc1}')
		print(YELLOW + 'Service Code Digit 2' + GRAY + '         | ' + RESET + f'{service_code[1]}: {desc2}')
		print(YELLOW + 'Service Code Digit 3' + GRAY + '         | ' + RESET + f'{service_code[2]}: {desc3}')
		print(YELLOW + 'Discretionary Data' + GRAY + '           | ' + RESET + discretionary_data)
		print(YELLOW + 'LRC (optional)' + GRAY + '               | ' + RESET + lrc)
		print(YELLOW + 'Raw Track Data' + GRAY + '               | ' + RESET + track1_match.group(0))
	else:
		generic_track1 = re.search(r'(%[AB][^\?]+\?)', data)
		print('Track 1 Data:')
		print('Raw                          | ' + (generic_track1.group(1) if generic_track1 else 'No data found'))

	if track2_match:
		pan, exp_date, service_code, discretionary_data = track2_match.groups()
		formatted_pan = format_pan(pan)
		formatted_exp_date = format_exp_date(exp_date)
		print('Track 2 Data:')
		print(CYAN + 'Primary Account Number (PAN)' + GRAY + ' | ' + RESET + formatted_pan)
		print(CYAN + 'Expiration Date' + GRAY + '              | ' + RESET + formatted_exp_date)
		print(CYAN + 'Service Code' + GRAY + '                 | ' + RESET + service_code)
		print(CYAN + 'Discretionary Data' + GRAY + '           | ' + RESET + discretionary_data)
		print(CYAN + 'Raw Track Data' + GRAY + '               | ' + RESET + track2_match.group(0))
	else:
		generic_track2 = re.search(r'(;[^\?]+\?)', data)
		print('Track 2 Data:')
		print('Raw                          | ' + (generic_track2.group(1) if generic_track2 else 'No data found'))

	if track3_match:
		print('Track 3 Data:')
		print(f'Raw                          | {track3_match.group(1)}')
	else:
		print('Track 3 Data: No data found.')



if __name__ == '__main__':
	try:
		swipe_data = getpass.getpass(prompt='Please swipe the card: ')
		parse_magnetic_stripe(swipe_data)
	except Exception as e:
		print('Error:', e)
