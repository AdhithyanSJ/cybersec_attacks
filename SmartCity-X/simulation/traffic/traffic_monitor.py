import os
import time
import traci

# ============================================================
# SMARTCITY-X
# Traffic Telemetry Monitor
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
# Discover traffic-light controller
# ============================================================

traffic_lights = traci.trafficlight.getIDList()

if not traffic_lights:
    print("[!] No traffic-light controller found.")
    traci.close()
    raise SystemExit

tl_id = traffic_lights[0]

print(f"[+] Traffic-light controller: {tl_id}")
print("[+] Traffic telemetry monitor started.\n")

# ============================================================
# Telemetry
# ============================================================

total_waiting_time = 0.0
max_queue = 0
max_waiting_time = 0.0

for step in range(300):

    traci.simulationStep()

    vehicle_ids = traci.vehicle.getIDList()

    active_vehicles = len(vehicle_ids)

    waiting_vehicles = 0
    current_total_wait = 0.0

    for vehicle_id in vehicle_ids:

        speed = traci.vehicle.getSpeed(vehicle_id)
        waiting_time = traci.vehicle.getAccumulatedWaitingTime(vehicle_id)

        # Vehicle considered waiting if speed is below 0.1 m/s
        if speed < 0.1:
            waiting_vehicles += 1

        current_total_wait += waiting_time

    # Average waiting time for vehicles currently in simulation
    if active_vehicles > 0:
        average_wait = current_total_wait / active_vehicles
    else:
        average_wait = 0.0

    max_queue = max(max_queue, waiting_vehicles)
    max_waiting_time = max(max_waiting_time, average_wait)

    current_phase = traci.trafficlight.getPhase(tl_id)

    print(
        f"Time={step:03d}s | "
        f"Phase={current_phase} | "
        f"Active={active_vehicles:02d} | "
        f"Waiting={waiting_vehicles:02d} | "
        f"AvgWait={average_wait:6.2f}s"
    )

    time.sleep(0.2)

# ============================================================
# Final statistics
# ============================================================

print("\n" + "=" * 65)
print("TRAFFIC SIMULATION SUMMARY")
print("=" * 65)

print(f"Maximum queue:          {max_queue} vehicles")
print(f"Maximum average wait:   {max_waiting_time:.2f} seconds")

print("=" * 65)

traci.close()

print("[+] TraCI connection closed.")
print("[+] Traffic telemetry monitor stopped.")