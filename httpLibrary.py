'''
author: Yang An 27878699 Bochuan An 27878745
'''
#########################
#    http Library       #

######GET operation########
'''
:param host: host
:param headers: {key:value} multiple headers through input
:param verbose: boolean value enables a verbose output from the command-line
:param path: file name
'''
def get(host, port, path, headers):

  # build http request method, query, host
  request = "GET " + path + "\r\n"
  if len(headers) != 0:
    for key, value in headers.items():
      request = request + key + ':' + value + '\r\n'
  request = request + "\r\n"

  return request

#########POST operation################
'''
:param host: host
# :param headers: {key:value} multiple headers through input
:param v: boolean value enables a verbose output from the command-line
:param data: in-line data
:param file: body of the HTTP Request with the data from a given file
'''
def post(host, port, path, data, file):
  # build http request method and host
  request = "POST " + path + "\r\n"

  # request body
  body = ''
  # inline data
  if data is not None:
    body = body + data
  # file
  elif file is not None:
    with open(file,'r') as f:
      for line in f:
        body = body + line.replace('\n','') +'&'

  # complete request
  request = request + "Content-Length: " + str(len(body)) + "\r\n\r\n"
  request = request + body +'\r\n'

  return request

