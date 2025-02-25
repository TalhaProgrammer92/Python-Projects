from PyMisc.system import get_mac_address
from os.path import exists, join
from os import system as cmd

try:
    # Terminal's Operations
    cmd('color 02')
    cmd('title Grant Access v1.0')

    # Get Path
    while True:
        path = input('Enter path of your software file: ')
        if len(path) == 0:
            exit()
        if exists(path):
            break
        print('Invalid path! Try again')
    path = join(path, 'mac.txt')

    # Get MAC address of the machine
    mac: str = get_mac_address()

    # Save to file
    with open(path, 'w') as file:
        file.write(mac)

    # Hide the file
    cmd(f'Attrib +h +r +s \'{path}\'')

    # Result
    print('Access Granted! Now you can run your software')
except Exception as e:
    print(f'Something went wrong!\nDebug: {e}')
