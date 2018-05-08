'''
author: Yang An 27878699 Bochuan An 27878745
Reference: Lab handout echoserver.py
'''
import socket
import threading
import argparse
import os


def run_server(host, port, v, directory):
    if directory is None:
        directory = os.path.dirname(os.path.realpath(__file__))
    # welcoming socket
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        listener.bind((host, port))
        # server being listening for incoming TCP request
        listener.listen(5)
        print('The server is ready to receive ', port, 'directory ', directory)
        while True:
            # server waits on accept() fro incoming request, new socket created on return
            conn, addr = listener.accept()
            threading.Thread(target=handle_client, args=(conn, addr, directory, v)).start()
    finally:
        listener.close()


def handle_client(conn, addr, directory, v):
    directory = directory
    print('New client from', addr)
    try:
        while True:
            allContent = os.listdir(directory)
            # only show files not folders
            files = [f for f in allContent if os.path.isfile(f)]
            data = conn.recv(1024).decode('utf_8')
            if not data:
                break
            print('Request: \r\n', data)
            # split data to header and body
            data = data.split('\r\n\r\n')
            header = data[0]
            body = data[1]
            statusLine = header.split('\r\n')[0]
            method = statusLine.split()[0]
            path = statusLine.split()[1]

            restHeader = header.split('\r\n')[1:]

            response = ''
            # handel get
            if method == 'GET':
                # handel get /
                if path == '/':
                    for f in files:
                      response = response + f + '\r\n'
                    response = 'HTTP 200 OK \r\n' + response
                    if v:
                        print('OK! returns the current list of files in the data directory. ')
                # handel get /filename
                # check current directory contain the filename or not, if filename be found, return the content of the file
                # else return file not found
                else:
                    if path[0] =='/':
                       fileFound = False
                       path = path[1:]
                       for f in files:
                           name = os.path.splitext(f)[0]
                           if path == name:
                               fileFound = True
                               fileOpen = open(directory + '/' + f, 'r')
                               response = fileOpen.read()
                               fileOpen.close()

                               for h in restHeader:
                                   if 'Content-Disposition' in h:
                                       firstPara = h.split(';')[0]
                                       secondPara = h.split(';')[1]
                                       if firstPara.split(':')[1] == 'inline':
                                           response = 'HTTP 200 OK \r\n' + response
                                       if firstPara.split(':')[1] == 'attachment':

                                           output = secondPara.split('=')[1]
                                           fileOpen = open(directory + '/' + output, 'w')
                                           fileOpen.write(response)
                                           fileOpen.close()
                                           response = 'HTTP 200 OK \r\n'
                                       break

                               if v:
                                   print('OK returns the content of the file named' + name +'in the data directory.')
                               break
                       if fileFound == False:
                           response = 'HTTP 404  file not found'
                           if v:
                               print('file not exist ', path)
                    else:
                        if v:
                            print('No authorization')
                        response = 'HTTP 403  action refused'
            # handel post
            elif method == 'POST':
                if path[0] == '/':
                    fileFound = False
                    path = path[1:]
                    # if file in directory, rewrite
                    for f in files:
                        name = os.path.splitext(f)[0]
                        extension = os.path.splitext(f)[1]
                        if path == name and extension != '.py':
                            fileOpen = open(directory + '/' + f, 'w')
                            fileOpen.write(body)
                            fileOpen.close()
                            fileFound = True
                            if v:
                                print('overwrite the file named ' + name +' in the data directory')
                            break
                        response = 'HTTP 200 OK \r\n' + body

                    if fileFound == False:
                        response = 'HTTP 403  action refused'
                        if v:
                            print('No such file or No authorization!')
                else:
                    if v:
                        print('No authorization!')
                    response = 'HTTP 403  action refused'

            conn.sendall(response.encode("utf-8"))
    except ConnectionResetError:
        print('connection closed', addr)
    finally:
        conn.close()


# Usage python httpfs [-v] [-p PORT] [-d PATH-TO-DIR]
parser = argparse.ArgumentParser()
parser.add_argument("-p", help="port number", type=int, default=8080)
parser.add_argument("-v", help="print debugging message", action="store_true")
parser.add_argument("-d", help="specifies the directory", type = str)
args = parser.parse_args()
run_server('localhost', args.p, args.v, args.d)