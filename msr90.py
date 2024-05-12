#!/usr/bin/env python
# MSR90 Card Reader - Developed by acidvegas in Python (https://acid.vegas/msr90)

import re

# ANSI Escape Codes
YELLOW = '\033[93m'
RESET  = '\033[0m'

# Numeric values for the service code
service_code_values = {
	'0': 'No restrictions and PIN required.',
	'1': 'No restrictions.',
	'2': 'Goods and services only (no cash).',
	'3': 'ATM only and PIN required.',
	'4': 'Cash only.',
	'5': 'Goods and services only (no cash), PIN required.',
	'6': 'No restrictions, use of PIN depends on issuers requirements.',
	'7': 'Goods and services only, use of PIN depends on issuers requirements.'
}

# Description of the format code
format_code_values = {
	'A': 'Reserved for proprietary use of the card issuer.',
	'B': 'Used by financial and credit card systems.'
}

def parse_magnetic_stripe(data: str):
	'''
	Parse the raw data from the magnetic stripe of a card.

	:param data: Raw data from the magnetic stripe of a card.
	'''

	# Regex to match the track 1 and track 2 data
	track1 = re.search(r'%([AB])(\d+)\^([^?^]+)\^(\d{4})(\d{3}).*?\?', data)
	track2 = re.search(r';(\d+)=(\d{4})(\d{3}).*?\?', data)

	# Check if the data is valid
	if not track1 or not track2:
		raise ValueError('Invalid data format')

	# Parse the data from the track 1 and track 2
	format_code    = track1.group(1)
	account_number = track1.group(2)
	name           = track1.group(3).strip()
	expiry_date    = track1.group(4)
	expiry_date    = f'{expiry_date[2:4]}/{expiry_date[0:2]}'
	service_code   = track1.group(5)

	service_code_description = [
		f'{service_code[0]} - {service_code_values.get(service_code[0], 'Unknown')}',
		f'{service_code[1]} - {service_code_values.get(service_code[1], 'Unknown')}',
		f'{service_code[2]} - {service_code_values.get(service_code[2], 'Unknown')}'
	]

	format_code_description = format_code_values.get(format_code, 'Unknown')

	# Print the parsed data
	print(f'{YELLOW}Name            :{RESET} {name}')
	print(f'{YELLOW}Account Number  :{RESET} {account_number}')
	print(f'{YELLOW}Expiration Date :{RESET} {expiry_date}')
	print(f'{YELLOW}Service Code    :{RESET} {service_code}')
	for item in service_code_description:
		print(' '*18 + item)
	print(f'{YELLOW}Format Code     :{RESET} {format_code} ({format_code_description})')
	print(f'{YELLOW}Track 1         :{RESET} {track1.group(0)}')
	print(f'{YELLOW}Track 2         :{RESET} {track2.group(0)}')

def main():
	print('Please swipe the card...')
	data = input()
	parse_magnetic_stripe(data)

if __name__ == '__main__':
	main()
