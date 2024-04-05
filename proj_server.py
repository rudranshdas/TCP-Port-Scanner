import socket
import ssl
import threading
import json


def get_local_ip():
    try:
        return socket.gethostbyname(socket.gethostname())
    except Exception as e:
        print(f"Error occurred while fetching local IP: {e}")
        return None

def handle_client(client_socket, ip_h, delay):
    open_ports={}
    in_use_ports={}

    def ports(port):
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.settimeout(delay)
        res = s.connect_ex((ip_h, port))
        if res==0:
            open_ports[port]='open'

        if res==1:
            in_use_ports[port]='in use'

        s.close()

    for port in range(0,4092):
        ports(port)

    vulnerabilities=[]
    for key in open_ports.keys():
        with open('vulnerabilities.txt', encoding='utf8') as file:
            for line in file:
                parts = line.split(':')
                if parts[0] == str(key):
                        vulnerabilities.append(parts[0]+": "+parts[1].strip())

    if not vulnerabilities:
        vulnerabilities.append("None")

    json_vul=json.dumps(vulnerabilities)

    client_socket.send(str(open_ports).encode())
    client_socket.send(json_vul.encode())
    client_socket.close()
    print("connection closed ")

def start_server(ip_h,port,delay,certfile,keyfile):
 
    server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server_socket.bind(("", port))  
    server_socket.listen(5)

    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile=certfile,keyfile=keyfile)
    server_socket_ssl = context.wrap_socket(server_socket,server_side=True)

    print(f"Server is listening on {ip_h}:{port}")  
    while True:
        client_socket, client_address = server_socket_ssl.accept()
        print(f"Connection from {client_address} has been established securely!")
        client_thread = threading.Thread(target=handle_client, args=(client_socket,ip_h,delay))
        client_thread.start()

ip_h = get_local_ip()
if ip_h:
    SERVER_PORT = 5050
    DELAY = 0.001  
    CERT_FILE='server.crt'
    KEY_FILE='server.key'
    start_server(ip_h,SERVER_PORT,DELAY,CERT_FILE,KEY_FILE)
else:
    print("Unable to retrieve local IP address. Exiting.")
