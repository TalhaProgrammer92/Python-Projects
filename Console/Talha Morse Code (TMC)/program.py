
# ? Encode
def encode(text: str, key: list[str] | str) -> list[str]:
	morse: list[str] = []
	base: int = len(key)

	# * Parse the text
	for char in text:
		num: int = ord(char)
		
		# * Conversion
		code: str = ""
		while num > 0:
			code = key[num % base] + code
			num = int(num / base)
		
		morse.append(code)

	return morse

# ? Decode
def decode(morse: list[str], key: list[str] | str) -> str:
	text: str = ""
	base: int = len(key)

	# * Prase the morse
	for code in morse:

		# * Conversion
		num: int = 0
		size: int = len(code)
		for i in range(size):
			num += key.index(code[i]) * pow(base, size - i - 1)

		text += chr(num)

	return text

# ? Testing
if '__main__' == __name__:
	text: str = "My name is Taha Ahmad."
	key: str = ['+', '-', '*', '/']
	morse: list[str] = encode(text, key)

	print('Morse: ', ' '.join(morse))
	print('Text: ', decode(morse, key))
