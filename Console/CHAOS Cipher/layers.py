from string import ascii_letters

def shifted_character_index(char: str, _list: list | tuple, shift: int) -> str:
	""" Get index of the shifted character """
	index: int = _list.index(char)
	for i in range(abs(shift)):
		pass


class ceaser:
	"""
	? Layer 1 - Ceaser Cipher

	* Encode: Shift +ve
	* Decode: Shift -ve
	"""

	@staticmethod
	def parse(text: str, shift: int) -> str:
		result: str = ''

		print(text)		# ? Debug

		# * Iterate through each character of the text
		for c in text:
			print(f'{c} -> ', end='')	# ? Debug

			# * If the character is an ascii letter
			if c in ascii_letters:
				# * Index of the character in ascii_letters list
				index = ascii_letters.index(c)
				
				# * Do shift
				for i in range(abs(shift)):
					# ! If shift is positive
					if shift > 0:
						# * If the index reached limit of the list ascii_letters' size
						if index == len(ascii_letters) - 1:
							index = 0
							continue
						index += 1
					
					# ! If shift is negative
					elif shift < 0:
						# * If the index reached the starting index of the list of ascii_letters
						if index == 0:
							index = len(ascii_letters) - 1
							continue
						index -= 1
				
				# ! Assign new shifted character
				c = ascii_letters[index]
			
			print(c)	# ? Debug
			c += result
		
		return result

