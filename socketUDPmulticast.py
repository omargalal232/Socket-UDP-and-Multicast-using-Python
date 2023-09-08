import socket
import time

multicast_group = '224.1.1.1'
multicast_port = 5000

udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket.bind(('', multicast_port))

mreq = socket.inet_aton(multicast_group) + socket.inet_aton('0.0.0.0')
udp_socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

def receive_data():
    while True:
        data, address = udp_socket.recvfrom(1024)
        print(f"Received message from {address}: {data.decode('utf-8')}")

def send_data():
    while True:
        message = input("Enter a message to send (or 'q' to quit): ")
        if message.lower() == 'q':
            break
        udp_socket.sendto(message.encode('utf-8'), (multicast_group, multicast_port))

import threading

receiver_thread = threading.Thread(target=receive_data)
sender_thread = threading.Thread(target=send_data)

receiver_thread.start()
sender_thread.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Exiting...")
finally:
    udp_socket.close()
