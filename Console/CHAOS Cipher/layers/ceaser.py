"""
 ? Layer 1 - Ceaser Cipher

 * Modes: 2
 * Encode: Shift +ve
 * Decode: Shift -ve
"""
from string import ascii_letters

class Cipher:
	@staticmethod
	def parse(text: str, shift: int) -> str:
		return ''.join([chr(ord(c) + shift) if c in ascii_letters else c for c in text])
