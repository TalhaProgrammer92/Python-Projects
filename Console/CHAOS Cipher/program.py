import layers

# ! Used to shift characters in a message
shift: int = 3

if '__main__' == __name__:
	encoded: str = layers.Ceaser.parse('Hello, World! abc XYZ | ABC xyz', shift)
	decoded: str = layers.Ceaser.parse(encoded, -shift)
	print(decoded, encoded, sep='\n')
	# print(chr(65), ord('A'))
