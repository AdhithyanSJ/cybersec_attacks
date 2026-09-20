import socket
import json
from datetime import datetime

HOST = "127.0.0.1"
PORT = 5002

AUTHORIZED_NETWORK = "SMARTCITY_PUBLIC"
AUTHORIZED_GATEWAY = "192.168.50.1"

print("=" * 60)
print("SMARTCITY-X PUBLIC NETWORK")
print("=" * 60)

print(f"\nNetwork:  {AUTHORIZED_NETWORK}")
print("Status:   ONLINE")
print(f"Gateway:  {AUTHORIZED_GATEWAY}")
print(f"Service:  {HOST}:{PORT}")

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server.bind((HOST, PORT))
server.listen(5)

print("\n[+] Public network service started")
print("[+] Waiting for citizen connections...\n")

while True:
    connection, address = server.accept()

    print("[CLIENT CONNECTED]")
    print(f"Client address: {address}")

    response = {
        "network": AUTHORIZED_NETWORK,
        "gateway": AUTHORIZED_GATEWAY,
        "status": "AUTHORIZED",
        "timestamp": datetime.now().isoformat()
    }

    connection.sendall(
        json.dumps(response).encode()
    )

    connection.close()

    print("[+] Authorized network information sent")
    print()
    