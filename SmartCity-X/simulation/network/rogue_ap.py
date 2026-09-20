import json
from datetime import datetime

AUTHORIZED_SSID = "SMARTCITY_PUBLIC"
AUTHORIZED_GATEWAY = "192.168.50.1"

ROGUE_SSID = "SMARTCITY_PUBLIC_FREE"
ROGUE_GATEWAY = "192.168.50.99"

print("=" * 60)
print("SMARTCITY-X ROGUE ACCESS POINT SIMULATION")
print("=" * 60)

print("\n[AUTHORIZED NETWORK]")
print(f"SSID:     {AUTHORIZED_SSID}")
print(f"Gateway:  {AUTHORIZED_GATEWAY}")
print("Status:   AUTHORIZED")

print("\n" + "=" * 60)
print("ATTACK PHASE")
print("=" * 60)

print("\n[ATTACK] Unauthorized access point detected")
print(f"[ATTACK] Rogue SSID: {ROGUE_SSID}")
print(f"[ATTACK] Rogue gateway: {ROGUE_GATEWAY}")

telemetry = {
    "timestamp": datetime.now().isoformat(),
    "authorized_ssid": AUTHORIZED_SSID,
    "observed_ssid": ROGUE_SSID,
    "authorized_gateway": AUTHORIZED_GATEWAY,
    "observed_gateway": ROGUE_GATEWAY,
    "ssid_mismatch": ROGUE_SSID != AUTHORIZED_SSID,
    "gateway_mismatch": ROGUE_GATEWAY != AUTHORIZED_GATEWAY,
    "unauthorized_ap": True,
    "attack": "ROGUE_ACCESS_POINT"
}

with open("network_telemetry.json", "w") as f:
    json.dump(telemetry, f, indent=4)

print("\n[IMPACT]")
print("[!] Client network identity has changed")
print("[!] Gateway identity mismatch detected")

print("\n[+] Network telemetry saved")