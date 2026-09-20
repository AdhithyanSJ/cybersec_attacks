import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

TELEMETRY_FILE = (
    PROJECT_ROOT
    / "simulation"
    / "network"
    / "network_telemetry.json"
)

with open(TELEMETRY_FILE, "r") as f:
    telemetry = json.load(f)

authorized_ssid = telemetry["authorized_ssid"]
observed_ssid = telemetry["observed_ssid"]

authorized_gateway = telemetry["authorized_gateway"]
observed_gateway = telemetry["observed_gateway"]

ssid_mismatch = telemetry["ssid_mismatch"]
gateway_mismatch = telemetry["gateway_mismatch"]
unauthorized_ap = telemetry["unauthorized_ap"]

print("=" * 60)
print("SMARTCITY-X")
print("PUBLIC NETWORK ATTACK DETECTION ENGINE")
print("=" * 60)

print("\n[TARGET]")
print(f"Authorized SSID:     {authorized_ssid}")
print(f"Observed SSID:       {observed_ssid}")
print(f"Authorized Gateway:  {authorized_gateway}")
print(f"Observed Gateway:    {observed_gateway}")

indicators = []

if unauthorized_ap:
    indicators.append("Unauthorized access point")

if ssid_mismatch:
    indicators.append("Network identity mismatch")

if gateway_mismatch:
    indicators.append("Gateway identity mismatch")

print("\n" + "=" * 60)
print("ANOMALY INDICATORS")
print("=" * 60)

for indicator in indicators:
    print(f"[X] {indicator}")

score = len(indicators)

if score >= 2:
    severity = "HIGH"
elif score == 1:
    severity = "MEDIUM"
else:
    severity = "LOW"

print("\n" + "=" * 60)
print("DETECTION RESULT")
print("=" * 60)

if score > 0:
    print("[ALERT] Rogue access point detected")
    print()
    print("Threat: ROGUE ACCESS POINT")
    print(f"Severity: {severity}")
    print(f"Detection indicators: {score}/3")
else:
    print("[OK] No network anomaly detected")