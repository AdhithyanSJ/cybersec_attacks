from pymodbus.client import ModbusTcpClient

PLC_IP = "127.0.0.1"
PLC_PORT = 502

client = ModbusTcpClient(PLC_IP, port=PLC_PORT)

print("=" * 50)
print("SMARTCITY-X SCADA CLIENT")
print("=" * 50)

if not client.connect():
    print("[ERROR] Could not connect to OpenPLC")
    raise SystemExit

print("[+] Connected to OpenPLC")

# %MW0 maps to Modbus holding register 1024
result = client.read_holding_registers(
    address=1024,
    count=1
)

if result.isError():
    print("[ERROR] Modbus read failed")
else:
    breaker_command = result.registers[0]

    print(f"[SCADA] Breaker Command: {breaker_command}")

client.close()

print("[+] Connection closed")