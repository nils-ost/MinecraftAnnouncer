import socket
import time
import os
import sys

server_ip = os.environ.get('SERVER_IP', None)
server_port = os.environ.get('SERVER_PORT', 25565)
server_motd = os.environ.get('SERVER_MOTD', 'A Minecraft Dedicated Server')
broadcast = bool(os.environ.get('BROADCAST', False))
d_ip = '255.255.255.255' if broadcast else '224.0.2.60'
d_port = 4445
msg = f'[MOTD]{server_motd}[/MOTD][AD]{server_port}[/AD]'.encode()

if not broadcast and server_ip is None:
    print('ERROR: multicast needs SERVER_IP to announce', file=sys.stderr)
    sys.exit(1)


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(1)

if broadcast:
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    print(f'Starting to announce "{server_motd}" via broadcast')
else:
    sock.bind((server_ip, 0))
    print(f'Starting to announce "{server_motd}" via multicast')

try:
    while True:
        sock.sendto(msg, (d_ip, d_port))
        time.sleep(1.5)
except KeyboardInterrupt:
    print('Exiting...')
    sys.exit(0)
finally:
    sock.close()
