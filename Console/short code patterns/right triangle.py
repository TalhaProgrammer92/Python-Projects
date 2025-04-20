size: int = 5
symbol: str = '*'

print('\n'.join(symbol * (i + 1) for i in range(size)))