import socket
import json

HOST = "127.0.0.1"
PORT = 5002

print("=" * 60)
print("SMARTCITY-X CITIZEN NETWORK CLIENT")
print("=" * 60)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client.connect((HOST, PORT))

    print("\n[+] Connected to SMARTCITY_PUBLIC")

    data = client.recv(4096).decode()

    network_info = json.loads(data)

    print("\n[NETWORK INFORMATION]")

    print(f"Network:  {network_info['network']}")
    print(f"Gateway:  {network_info['gateway']}")
    print(f"Status:   {network_info['status']}")

except ConnectionRefusedError:
    print("[ERROR] Public network service is not running")

finally:
    client.close()
    print("\n[+] Connection closed")