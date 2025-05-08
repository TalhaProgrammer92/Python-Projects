import layers.ceaser as ceaser

# ! Used to shift characters in a message
shift: int = 3

if '__main__' == __name__:
	encoded: str = ceaser.Cipher.parse('Hello, World!', shift)
	decoded: str = ceaser.Cipher.parse(encoded, -shift)
	print(decoded, encoded, sep='\n')
	# print(chr(65), ord('A'))
