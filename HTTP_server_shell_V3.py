# HTTP Server Shell
# Author: Barak Gonen
# Purpose: Provide a basis for Ex. 4.4
# Note: The code is written in a simple way, without classes, log files or other utilities, for educational purpose
# Usage: Fill the missing functions and constants

# TO DO: import modules
import socket
import os
# TO DO: set constants

IP = '0.0.0.0'
PORT = 5656
requestedUrl = ''
DEFAULT_URL = 'C:/Users/Ethan/Desktop/Python/Server/http_server_gvahim/index.html'
url=''
http_response=''
http_header=''
filetype=''
filetype=''


def get_file_data(filename):
    """ Get data from file """
    my_file = open(filename)
    file_read = my_file.read()
    my_file.close()
    return file_read


def handle_client_request(resource, client_socket, nom_demande):
    """ Check the required resource, generate proper HTTP response and send to client"""
    # TO DO : add code that given a resource (URL and parameters) generates the proper response
    if resource == '':
        url = DEFAULT_URL
    else:
        url = resource

    #Check if the url requested exist

    if nom_demande=='/calculate-next':
        http_header = "HTTP/1.1 200 OK\r\n"
        data = '5'
        http_response = http_header+data
        http_response = http_response.encode("utf8")
        client_socket.send(http_response)
        return
    elif not os.path.exists(url):
        http_response = r"HTTP/1.1 404 Not Found\r\n"
        http_response = http_response.encode("utf8")
        client_socket.send(http_response)
        return
    else:
        http_header = "HTTP/1.1 200 OK\r\n"

    # TO DO: extract requested file tupe from URL (html, jpg etc)
    if "." in url:
        filetype = url[url.index(".") + 1:]
        print("FileType: "+ filetype)
    
    else:
        http_response = r"HTTP/1.1 404 Not Found\r\n"
        print ("NOOOOOOOOOOOOOOO")
        http_response = http_response.encode("utf8")

        client_socket.send(http_response)
        return

    filetype=''
    if filetype == 'html':
        http_header += "Content-Type: text/html; charset=utf-8\r\n" # TO DO: generate proper HTTP header
    elif filetype == 'jpg':
        http_header += "Content-Type: image/jpg\r\n" # TO DO: generate proper jpg header
    elif filetype == 'js':
            http_header += "Content-Type: text/javascript; charset=utf-8\r\n"
    elif filetype == 'css':
        http_header += "Content-Type: text/css\r\n"
    else:
        pass

    
    # TO DO: handle all other headers

    # TO DO: read the data from the file
    filename = url
    data = get_file_data(filename)
    http_response = http_header + data
    http_response = http_response.encode('utf8')
    client_socket.send(http_response)


def validate_http_request(request):
    """ Check if request is a valid HTTP request and returns TRUE / FALSE and the requested URL """
    # TO DO: write function
    reqSpliting = request.split(" ")
    typeOf = reqSpliting[0]
    print("TYPE OF REQUEST :"+ typeOf)
    if(typeOf != "GET"):
        return (False,None)
    srcOf = reqSpliting[1]
    demande = srcOf
    print("SOURCE: "+ srcOf)
    protocol_version = reqSpliting[2]
    print("PROTOCOL VERSION: "+protocol_version)
    if srcOf == r'/':
        requestedUrl = ''
        print("Rien dans le requestedUrl")
    else:
        requestedUrl = "C:/Users/Ethan/Desktop/Python/Server/http_server_gvahim"
        srcOf = srcOf.split("/")

        for st in srcOf:
            print(st)
            if st!='':
                requestedUrl+="/"
                requestedUrl+=st
        print("REQUESTED URL AFTER: "+ requestedUrl)
    return (True, requestedUrl, demande)

    
def handle_client(client_socket):
    """ Handles client requests: verifies client's requests are legal HTTP, calls function to handle the requests """
    print ("Client connected")
    while True:
        # TO DO: insert code that receives client request
        # ...
        client_request = client_socket.recv(1024)
        client_request = client_request.decode("utf8")
        print("client request: "+client_request)
        valid_http, resource, nom_demande = validate_http_request(client_request)
        if valid_http:
            print("Got a valid HTTP request")
            handle_client_request(resource, client_socket, nom_demande)
        else:
            print("Error: Not a valid HTTP request")
            break
    print ("Closing connection")
    client_socket.close()


def main():
    # Open a socket and loop forever while waiting for clients
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((IP, PORT))
    server_socket.listen(10)
    print("Listening for connections on port %d" % PORT)

    while True:
        client_socket, client_address = server_socket.accept()
        print ("New connection received")
        client_socket.settimeout(60)
        handle_client(client_socket)


if __name__ == "__main__":
    # Call the main handler function
    main()
