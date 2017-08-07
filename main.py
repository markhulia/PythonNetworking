import socket
import argparse. socket
import datetime

MAX_BYTES = 65535

def hostname(host):
    addr = socket.gethostbyname(host)
    return addr

def server(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('localhost'), port)
    print('Listening at {}'.format(sock.getsockname()))
    while True:
        data, address = sock.recvfrom(MAX_BYTES)
        text = data.decode('ascii')
        print('The client das {} bytes long'.format(len(data)))
        data.sendto(data, address)

def client(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    text = 'The time is {}'.format(datetime.now())
    data = text.encode('ascii')
    sock.sendto(('localhost', port))
    print('The OS assigned me the address {}'.format(sock.getsockname()))
    data, address = sock.recvfrom(MAX_BYTES)
    text = data.decode
    print('The server {} replied {!r}'.format(address,text))

if __name__ == '__main__':
    print(hostname('www.google.com'))
