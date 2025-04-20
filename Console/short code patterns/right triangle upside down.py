size: int = 5
symbol: str = '*'

print('\n'.join(symbol * (size - i) for i in range(size)))