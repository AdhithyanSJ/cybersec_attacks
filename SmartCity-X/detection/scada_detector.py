import json
from pathlib import Path

# ---------------------------------------------------------
# PATHS
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

TELEMETRY_FILE = (
    PROJECT_ROOT
    / "simulation"
    / "scada"
    / "scada_telemetry.json"
)

# ---------------------------------------------------------
# LOAD TELEMETRY
# ---------------------------------------------------------

with open(TELEMETRY_FILE, "r") as f:
    telemetry = json.load(f)

normal_value = telemetry["normal_value"]
observed_value = telemetry["observed_value"]
unauthorized_write = telemetry["unauthorized_write"]

# ---------------------------------------------------------
# DISPLAY
# ---------------------------------------------------------

print("=" * 60)
print("SMARTCITY-X")
print("SCADA ATTACK DETECTION ENGINE")
print("=" * 60)

print("\n[TARGET]")
print(f"Device:       {telemetry['target']}")
print(f"IP Address:   {telemetry['ip']}")
print(f"Protocol:     {telemetry['protocol']}")
print(f"Register:     {telemetry['register']}")
print(f"PLC Variable: {telemetry['variable']}")

print("\n[NORMAL STATE]")
print(f"Authorized Breaker Command: {normal_value}")

print("\n[OBSERVED STATE]")
print(f"Observed Breaker Command:    {observed_value}")

# ---------------------------------------------------------
# DETECTION INDICATORS
# ---------------------------------------------------------

indicators = []

if unauthorized_write:
    indicators.append("Unauthorized Modbus write")

if observed_value != normal_value:
    indicators.append("Unexpected breaker state change")

if telemetry["register"] == 1024:
    indicators.append("Critical control register modified")

print("\n" + "=" * 60)
print("ANOMALY INDICATORS")
print("=" * 60)

for indicator in indicators:
    print(f"[X] {indicator}")

# ---------------------------------------------------------
# DETECTION RESULT
# ---------------------------------------------------------

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
    print("[ALERT] SCADA control anomaly detected")
    print()
    print("Threat: SCADA CONTROL MANIPULATION")
    print(f"Severity: {severity}")
    print(f"Detection indicators: {score}/3")
else:
    print("[OK] No SCADA anomaly detected")