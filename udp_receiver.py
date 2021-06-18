import socket
import requests
import pickle

UDP_IP = "127.0.0.1"
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))


address = {
    "ip": UDP_IP,
    "port": UDP_PORT
}

# set the receiver address to the server to receive data
server_url = 'http://127.0.0.1:8008'
res = requests.post(server_url + "/target_connection", json=address)
print("Res ", res.text)

while True:
    # buffer size in bytes
    data, addr = sock.recvfrom(4096)
    decoded_data = pickle.loads(data)
    print("received", decoded_data)

