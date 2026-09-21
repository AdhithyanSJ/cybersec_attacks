import socket

HOST = "127.0.0.1"
PORT = 5002

print("=" * 60)
print("SMARTCITY-X PUBLIC NETWORK")
print("=" * 60)

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

    payload = connection.recv(4096).decode("ascii")
    metadata = {}
    lines = payload.splitlines()
    if not lines or lines[0] != "SMARTCITY-X NETWORK METADATA":
        response = "ERROR=INVALID_METADATA\n"
    else:
        for line in lines[1:]:
            key, separator, value = line.partition("=")
            if separator and key in {"SSID", "GATEWAY"}:
                metadata[key] = value

        if set(metadata) != {"SSID", "GATEWAY"}:
            response = "ERROR=INCOMPLETE_METADATA\n"
        else:
            response = (
                "METADATA_RECEIVED\n"
                f"SSID={metadata['SSID']}\n"
                f"GATEWAY={metadata['GATEWAY']}\n"
            )
            print("\n[NETWORK METADATA]")
            print(f"SSID:     {metadata['SSID']}")
            print(f"Gateway:  {metadata['GATEWAY']}")

    connection.sendall(response.encode("ascii"))

    connection.close()

    print("[+] Network metadata response sent")
    print()
    