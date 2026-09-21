import socket
import os
import sys

HOST = "127.0.0.1"
PORT = 5002

AUTHORIZED_SSID = "SMARTCITY_PUBLIC"
AUTHORIZED_GATEWAY = "192.168.50.1"
ROGUE_SSID = "SMARTCITY_PUBLIC_FREE"
ROGUE_GATEWAY = "192.168.50.99"


def simulated_network() -> tuple[str, str]:
    state = os.environ.get("NETWORK_STATE", "normal").lower()
    if "--rogue" in sys.argv:
        state = "rogue"

    if state == "normal":
        return AUTHORIZED_SSID, AUTHORIZED_GATEWAY
    if state == "rogue":
        return ROGUE_SSID, ROGUE_GATEWAY
    raise ValueError("NETWORK_STATE must be 'normal' or 'rogue'")


print("=" * 60)
print("SMARTCITY-X CITIZEN NETWORK CLIENT")
print("=" * 60)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client.connect((HOST, PORT))

    ssid, gateway = simulated_network()
    payload = (
        "SMARTCITY-X NETWORK METADATA\n"
        f"SSID={ssid}\n"
        f"GATEWAY={gateway}\n"
    )
    client.sendall(payload.encode("ascii"))

    response = client.recv(4096).decode("ascii")

    print(f"\n[+] Sent simulated network metadata for {ssid}")
    print(response.rstrip())

except ConnectionRefusedError:
    print("[ERROR] Public network service is not running")
except ValueError as error:
    print(f"[ERROR] {error}")

finally:
    client.close()
    print("\n[+] Connection closed")