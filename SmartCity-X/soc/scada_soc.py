from pymodbus.client import ModbusTcpClient
import json
from pathlib import Path
from datetime import datetime

# ---------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

TELEMETRY_FILE = (
    PROJECT_ROOT
    / "simulation"
    / "scada"
    / "scada_telemetry.json"
)

PLC_IP = "127.0.0.1"
PLC_PORT = 502

BREAKER_REGISTER = 1024

AUTHORIZED_STATE = 0

# ---------------------------------------------------------
# LOAD DETECTION EVIDENCE
# ---------------------------------------------------------

with open(TELEMETRY_FILE, "r") as f:
    telemetry = json.load(f)

observed_value = telemetry["observed_value"]
unauthorized_write = telemetry["unauthorized_write"]

# ---------------------------------------------------------
# SOC ALERT
# ---------------------------------------------------------

print("=" * 60)
print("SMARTCITY-X SOC")
print("=" * 60)

print("\n🚨 SMARTCITY-X SOC ALERT")

print("\n[INCIDENT]")
incident_id = datetime.now().strftime("SCX-%Y%m%d-%H%M%S")

print(f"Incident ID: {incident_id}")
print("Target:      OpenPLC")
print("PLC Variable: %MW0")

print("\n[DETECTION EVIDENCE]")

if unauthorized_write:
    print("[X] Unauthorized Modbus write")

if observed_value != AUTHORIZED_STATE:
    print("[X] Unexpected breaker state change")

print("\n[THREAT CLASSIFICATION]")
print("Threat: SCADA CONTROL MANIPULATION")
print("Severity: HIGH")
print("Detection score: 3/3")

# ---------------------------------------------------------
# AUTOMATED RESPONSE
# ---------------------------------------------------------

print("\n" + "=" * 60)
print("AUTOMATED RESPONSE")
print("=" * 60)

print("\n[RESPONSE] SCADA control manipulation confirmed.")
print("[RESPONSE] Unauthorized control state contained.")
print("[RESPONSE] Automatic restoration intentionally disabled.")

client = ModbusTcpClient(
    PLC_IP,
    port=PLC_PORT
)

if not client.connect():
    print("[ERROR] Could not connect to OpenPLC")
    raise SystemExit

print("[RESPONSE] Connected to OpenPLC.")
print("[RESPONSE] Verifying the manipulated breaker state...")

verify = client.read_holding_registers(
    address=BREAKER_REGISTER,
    count=1
)

if verify.isError():
    print("[ERROR] Could not verify PLC state.")
    client.close()
    raise SystemExit

final_value = verify.registers[0]

if final_value != observed_value:
    print(
        f"[ERROR] PLC state changed unexpectedly during containment: "
        f"{final_value}"
    )
    client.close()
    raise SystemExit

print(f"[RESPONSE] Breaker Command remains: {final_value}")

client.close()

# ---------------------------------------------------------
# INCIDENT LOG
# ---------------------------------------------------------

incident = {
    "incident_id": incident_id,
    "timestamp": datetime.now().isoformat(),
    "target": "OpenPLC",
    "threat": "SCADA CONTROL MANIPULATION",
    "severity": "HIGH",
    "detection_score": "3/3",
    "observed_state": final_value,
    "authorized_state": AUTHORIZED_STATE,
    "response": "CONTROL_STATE_CONTAINED",
    "final_state": final_value
}

INCIDENT_FILE = (
    PROJECT_ROOT
    / "soc"
    / "scada_incident_log.json"
)

with open(INCIDENT_FILE, "w") as f:
    json.dump(incident, f, indent=4)

print("[RESPONSE] Incident logged.")
print(f"\nIncident log: {INCIDENT_FILE}")

print("\n" + "=" * 60)
print("SOC INCIDENT SUMMARY")
print("=" * 60)

print(f"Incident ID: {incident_id}")
print("Threat:      SCADA CONTROL MANIPULATION")
print("Severity:    HIGH")
print("Response:    CONTROL_STATE_CONTAINED")
print(f"Final state: {final_value}")

print("=" * 60)