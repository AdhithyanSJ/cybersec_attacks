import os
import time
import json
import traci

# ============================================================
# SMARTCITY-X
# Normal Traffic Baseline
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
# Traffic-light controller
# ============================================================

traffic_lights = traci.trafficlight.getIDList()

if not traffic_lights:
    print("[!] No traffic-light controller found.")
    traci.close()
    raise SystemExit

tl_id = traffic_lights[0]

print(f"[+] Traffic-light controller: {tl_id}")
print("[+] Collecting normal traffic baseline...\n")

# ============================================================
# Baseline metrics
# ============================================================

max_queue = 0
max_average_wait = 0.0
total_average_wait = 0.0
samples = 0

phase_counts = {}

# ============================================================
# Simulation
# ============================================================

for step in range(300):

    traci.simulationStep()

    vehicle_ids = traci.vehicle.getIDList()

    active_vehicles = len(vehicle_ids)

    waiting_vehicles = 0
    current_total_wait = 0.0

    for vehicle_id in vehicle_ids:

        speed = traci.vehicle.getSpeed(vehicle_id)
        waiting_time = traci.vehicle.getAccumulatedWaitingTime(vehicle_id)

        if speed < 0.1:
            waiting_vehicles += 1

        current_total_wait += waiting_time

    if active_vehicles > 0:
        average_wait = current_total_wait / active_vehicles
    else:
        average_wait = 0.0

    current_phase = traci.trafficlight.getPhase(tl_id)

    # Track phase frequency
    phase_counts[str(current_phase)] = (
        phase_counts.get(str(current_phase), 0) + 1
    )

    # Update statistics
    max_queue = max(max_queue, waiting_vehicles)
    max_average_wait = max(max_average_wait, average_wait)

    total_average_wait += average_wait
    samples += 1

    print(
        f"Time={step:03d}s | "
        f"Phase={current_phase} | "
        f"Active={active_vehicles:02d} | "
        f"Waiting={waiting_vehicles:02d} | "
        f"AvgWait={average_wait:6.2f}s"
    )

    time.sleep(0.2)

# ============================================================
# Calculate final statistics
# ============================================================

overall_average_wait = (
    total_average_wait / samples
    if samples > 0
    else 0.0
)

# ============================================================
# Create baseline
# ============================================================

baseline = {
    "simulation": {
        "duration_steps": 300,
        "traffic_light": tl_id
    },

    "normal_traffic": {
        "maximum_queue": max_queue,
        "maximum_average_wait": round(max_average_wait, 2),
        "overall_average_wait": round(overall_average_wait, 2)
    },

    "traffic_light": {
        "phase_frequency": phase_counts
    }
}

# ============================================================
# Save baseline
# ============================================================

with open("baseline.json", "w") as file:
    json.dump(
        baseline,
        file,
        indent=4
    )

# ============================================================
# Display summary
# ============================================================

print("\n" + "=" * 65)
print("SMARTCITY-X NORMAL TRAFFIC BASELINE")
print("=" * 65)

print(f"Traffic controller:     {tl_id}")
print(f"Maximum queue:          {max_queue} vehicles")
print(f"Maximum average wait:   {max_average_wait:.2f} seconds")
print(f"Overall average wait:   {overall_average_wait:.2f} seconds")

print("\nPhase frequency:")

for phase, count in phase_counts.items():
    print(f"    Phase {phase}: {count} steps")

print("=" * 65)

# ============================================================
# Shutdown
# ============================================================

traci.close()

print("[+] TraCI connection closed.")
print("[+] Baseline collection complete.")
print("[+] Saved baseline.json")