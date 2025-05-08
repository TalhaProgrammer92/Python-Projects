from string import ascii_letters

class ceaser:
	"""
	? Layer 1 - Ceaser Cipher

	* Encode: Shift +ve
	* Decode: Shift -ve
	"""

	@staticmethod
	def parse(text: str, shift: int) -> str:
		result: str = ''

		# * Iterate through each character of the text
		print(text)
		for c in text:
			print(f'{c} -> ', end='')
			# * If the character is an ascii letter
			if c in ascii_letters:
				# * Index of the character in ascii_letters list
				index = ascii_letters.index(c)
				
				# * Do shift
				for i in range(abs(shift)):
					# ! If shift is positive
					if shift > 0:
						if index == len(ascii_letters) - 1:
							index = 0
							continue
						index += 1
					
					# ! If shift is negative
					else:
						if index < 0:
							index = len(ascii_letters) - 1
							continue
						index -= 1
				
				# ! Assign new shifted character
				c = ascii_letters[index]
			
			print(c)
			c += result
		
		return result

