#!/usr/bin/env python
# Luhn Algorithm Example - Developed by acidvegas in Python (https://git.acid.vegas/msr90)

def modulo10(card_number: str) -> str:
	'''
	Validate a card number using the Luhn Algorithm

	:param card_number: The card number to validate
	'''

	digits = [int(d) for d in card_number]
	total_sum = 0

	for i, digit in enumerate(reversed(digits)):
		if i % 2 == 0:
			digit = digit * 2

			if digit > 9:
				digit -= 9

		total_sum += digit

	check_digit = (10 - total_sum % 10) % 10
	full_card_number = card_number + str(check_digit)

	if (total_sum + check_digit) % 10 != 0:
		raise ValueError('failed luhn check (non-divisible by 10)')

	return full_card_number


if __name__ == '__main__':
	card_number = input('Enter your card number without the last digit: ')

	if not card_number.isdigit():
		raise ValueError('invalid card number')

	print(f'Full card number: {modulo10(card_number)}')
