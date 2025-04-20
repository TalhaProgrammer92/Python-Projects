size: int = 7
symbol: str = '*'

print('\n'.join(symbol * size if i % 2 != size % 2 else ' ' * size for i in range(size)))
