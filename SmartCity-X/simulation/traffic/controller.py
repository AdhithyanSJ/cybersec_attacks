import os
import time
import traci

# ============================================================
# SMARTCITY-X
# Phase 2C - Authorized Traffic Light Controller
# ============================================================

SUMO_HOME = os.environ.get("SUMO_HOME")

if not SUMO_HOME:
    raise EnvironmentError("SUMO_HOME is not configured.")

sumo_binary = os.path.join(
    SUMO_HOME,
    "bin",
    "sumo-gui.exe"
)

config_file = "intersection.sumocfg"

# ============================================================
# Start SUMO
# ============================================================

sumo_cmd = [
    sumo_binary,
    "-c",
    config_file,
    "--start"
]

print("[+] Starting SUMO...")
traci.start(sumo_cmd)

# ============================================================
# Discover traffic lights
# ============================================================

traffic_lights = traci.trafficlight.getIDList()

print("\n[+] Traffic-light controllers:")

for tl in traffic_lights:
    print(f"    - {tl}")

if not traffic_lights:
    print("[!] No traffic lights found.")
    traci.close()
    raise SystemExit

tl_id = traffic_lights[0]

print(f"\n[+] Connected to controller: {tl_id}")

# ============================================================
# Monitor + authorized control test
# ============================================================

for step in range(300):

    traci.simulationStep()

    current_phase = traci.trafficlight.getPhase(tl_id)
    remaining = traci.trafficlight.getNextSwitch(tl_id) - traci.simulation.getTime()

    vehicle_count = len(
        traci.vehicle.getIDList()
    )

    print(
        f"Step={step:03d} | "
        f"Phase={current_phase} | "
        f"NextSwitch={remaining:.1f}s | "
        f"Vehicles={vehicle_count}"
    )

    # --------------------------------------------------------
    # AUTHORIZED CONTROLLER OVERRIDE
    # --------------------------------------------------------

    if step == 100:
        print("\n[CONTROL] Authorized override initiated")
        print("[CONTROL] Switching junction to phase 0")

        traci.trafficlight.setPhase(
        tl_id,
        0
    )

    if step == 160:
        print("\n[CONTROL] Authorized override initiated")
        print("[CONTROL] Switching junction to phase 2")

        traci.trafficlight.setPhase(
        tl_id,
        2
    )

    # Slow down simulation for visual observation
    time.sleep(0.2)

# ============================================================
# Shutdown
# ============================================================

print("\n[+] Simulation complete.")
print("[+] Closing TraCI connection...")

traci.close()

print("[+] Controller shutdown complete.")