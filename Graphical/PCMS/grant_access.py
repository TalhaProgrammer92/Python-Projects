import uuid
from os.path import exists, join
from os import system as cmd
from shlex import quote
from subprocess import run

try:
    # Terminal's Operations
    cmd('color 02')
    cmd('title Grant Access v1.0')

    # Get Path
    while True:
        path: str = input('Enter path of your software file: ')
        if len(path) == 0:
            exit()
        if exists(path):
            break
        print('Invalid path! Try again')
    path = join(path, 'mac.txt')

    # Get MAC address of the machine
    mac: str = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(0, 2*6, 8)][::-1])

    # Save to file
    with open(path, 'w') as file:
        file.write(mac)

    # Hide the file
    run(f'Attrib +h +r +s "{path}"', shell=True)

    # Result
    print('Access Granted! Now you can run your software')
except Exception as e:
    # Exception prompt message
    print(f'Something went wrong!\nDebug: {e}')

a = input('\nPress \'Enter\' key to exit...')
