'''
author: Yang An 27878699 Bochuan An 27878745
Reference: Lab handout echoclient.py
'''
import socket
from httpLibrary import *
import sys
import argparse

def run_client(host, port):
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        conn.connect((host, port))
        print("Type any command. Press Ctrl+C to terminate")
        print('"get /" --return the current list of files in the directory ')
        print('"get /[file name]"  --return the content of the file named file')
        print('"post /[file name] [-d <inline data>] [-f <input file>]"  --overwrite the file with the content')
        while True:
            line = sys.stdin.readline(1024)
            line = line.split()
            method = line[0]
            rest = line[1:]

            if method == 'get':
                path = rest[0]
                headers = {}
                if '-h' in rest:
                    header = rest[(rest.index('-h')+1):]
                    for h in header:
                        key = h.split(':')[0]
                        value = h.split(':')[1]
                        headers[key] = value
                request = get(host, port, path, headers)
                # print(request)
                conn.sendall(request.encode("utf-8"))
                response = conn.recv(1024).decode("utf-8")
                print('Response: \r\n', response)
            elif method == 'post':
                path = rest[0]
                if '-d' in rest:
                    value = rest[(rest.index('-d')+1):]

                    data = ''
                    for v in value:
                        data = data + v + ' '
                    request = post(host, port, path, data, None)
                    # print(request)
                    conn.sendall(request.encode("utf-8"))
                    response = conn.recv(1024).decode("utf-8")
                    print('Response: \r\n', response)
                elif '-f' in rest:
                    file = rest[rest.index('-f')+1]
                    request = post(host, port, path, None, file)
                    # print(request)
                    conn.sendall(request.encode("utf-8"))
                    response = conn.recv(1024).decode("utf-8")
                    print('Response: \r\n', response)
            else:
                print('Method can only be get or post')

    finally:
        conn.close()


# Usage: python httpc.py --host host --port port
parser = argparse.ArgumentParser()
parser.add_argument("--host", help="server host", default="localhost")
parser.add_argument("--port", help="server port", type=int, default=8080)
args = parser.parse_args()
run_client(args.host, args.port)


