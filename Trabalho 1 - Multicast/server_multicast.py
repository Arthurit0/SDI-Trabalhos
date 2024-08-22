import socket
import struct
import time
import random

ip_multicast = "224.1.1.1"
port_multicast = 5007
TTL_multicast = 2

# Socket UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, TTL_multicast)

try:
    while True:
        number = random.randint(1, 10)
        message = str(number).encode("utf-8")

        sock.sendto(message, (ip_multicast, port_multicast))

        print(f"Mensagem enviada por {ip_multicast}:{port_multicast} => {number}")

        time.sleep(1)

except KeyboardInterrupt:
    print("Servidor encerrado.")
finally:
    sock.close()
