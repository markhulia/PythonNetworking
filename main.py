import socket

def hostname(host):
    addr = socket.gethostbyname(host)
    return addr


if __name__ == '__main__':
    print(hostname('www.google.com'))