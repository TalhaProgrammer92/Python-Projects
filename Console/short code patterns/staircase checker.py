size: int = 5
symbol: tuple[str, str] = ('$', '%')

print('\n'.join(''.join(symbol[(i + j) % 2] for j in range(i + 1)) for i in range(size)))