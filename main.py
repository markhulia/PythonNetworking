import argparse, socket, random, sys
from datetime import datetime

MAX_BYTES = 65535


def server(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('localhost', port))
    print('Listening at {}'.format(sock.getsockname()))
    while True:
        data, address = sock.recvfrom(MAX_BYTES)
        if random.random()<0.5:
            print('Pretending to drop packet fromP{}'.format(address))
            continue
        text = data.decode('ascii')
        print('The client at {} says {!r}'.format(address, text))
        # text = 'Your data was {} bytes long'.format(len(data))
        reply = input('Type your message: ')
        data = reply.encode('ascii')
        sock.sendto(data, address)


def client(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    hostname = sys.argv[2]
    sock.connect((hostname, port))
    print('Client socket name is {}'.format(sock.getsockname()))

    delay = 0.1
    text = 'This is another message'
    data = text.encode('ascii')
    while True:
        # text = input('Type your message: ')
        # data = text.encode('ascii')
        sock.send(data)
        print('Waiting up to {} seconds for a reply'.format(delay))
        sock.settimeout(delay)
        try:
            data = sock.recv(MAX_BYTES)
        except socket.timeout:
            delay*=2 # wait even longer for the next request
            if delay>2.0:
                raise RuntimeError('Server is down')
        else:
            break;  # stop looping
        print('The OS assigned me the address {}'.format(sock.getsockname()))
        data, address = sock.recvfrom(MAX_BYTES)
        text = data.decode('ascii')
        print(text)


if __name__ == '__main__':
    choices = {'client': client, 'server': server}
    parser = argparse.ArgumentParser(description='Send and receive UDP locally')

    parser.add_argument('role', choices=choices, help='Which role to play')
    parser.add_argument('-p', metavar='PORT', type=int, default=1060,
                        help='UDP port (default 1060)')
    parser.add_argument('host', help='interface server listens at;''host the client sends to')
    args = parser.parse_args()
    function = choices[args.role]
    function(args.p)
