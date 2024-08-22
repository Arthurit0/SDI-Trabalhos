import socket
import struct
import time
from collections import Counter

ip_multicast = "224.1.1.1"
port_multicast = 5007
timeout = 10

# Socket UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.bind(("", port_multicast))

# Entra no grupo multicast
mreq = struct.pack("4sl", socket.inet_aton(ip_multicast), socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

counter = Counter()
nr_msg = 1

try:
    while True:
        sock.settimeout(timeout)

        while True:
            data, addr = sock.recvfrom(1024)
            number = int(data.decode("utf-8"))

            print(f"Mensagem nº {nr_msg} recebida de {addr[0]}:{addr[1]} => {number}")

            nr_msg += 1
            counter[number] += 1

            most_common = counter.most_common(1)[0]
            print(
                f"\n=== Número mais frequente === \n * {most_common[0]} com {most_common[1]} ocorrência(s)\n"
            )

except KeyboardInterrupt:
    print("Cliente encerrado.")
finally:
    sock.close()
