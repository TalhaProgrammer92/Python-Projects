import uuid
from os.path import exists

def get_mac_address() -> str:
    """ Get MAC Address of current machine """
    mac = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(0, 2*6, 8)][::-1])
    return mac

def authorized_mac(path: str) -> bool:
    """ Check if the machine is authorized or not """
    if exists(path):
        with open(path, 'r') as file:
            mac: str = file.read()
        if mac == get_mac_address():
            return True
    return False

if __name__ == '__main__':
    print(get_mac_address())