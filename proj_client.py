import socket
import ssl

def start_client(host, port, certfile):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    context.load_verify_locations(CERT_FILE)
    context.check_hostname=False
    ssl_socket = context.wrap_socket(client_socket, server_hostname=host)
    

    ssl_socket.connect((host, port))
    print("Connected to server.")


    response = ssl_socket.recv(4096).decode()
    print("Port scan results:", response)

  
    ssl_socket.close()


SERVER_HOST = "192.168.43.232"
SERVER_PORT = 5050
CERT_FILE = 'server.crt'  

start_client(SERVER_HOST, SERVER_PORT, CERT_FILE)
