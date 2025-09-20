from time import sleep

limit = 20
for count in range(1, limit + 1):
    print('#' * (count), '-' * (limit - count), f' {int((count / limit) * 100)}%', sep='', end=chr(13))
    sleep(1)
