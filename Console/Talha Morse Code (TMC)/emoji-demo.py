import program as tmc

key: str = ['😊', '😆', '😎', '🤔', '😐', '🙄', '🥱', '🤯']
text: str = 'Good Luck'

morse: list[str] = tmc.encode(text, key)

print(' '.join(morse), tmc.decode(morse, key), sep='\n')
