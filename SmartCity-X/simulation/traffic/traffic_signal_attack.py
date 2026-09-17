import traci
import json
import os


# ============================================================
# SMARTCITY-X
# Traffic Signal Manipulation Attack
# ============================================================

# SUMO configuration
SUMO_CONFIG = "intersection.sumocfg"

# Simulation settings
SIMULATION_STEPS = 300

# Traffic light being targeted
TRAFFIC_LIGHT_ID = "junction"

# Attack window
ATTACK_START = 100
ATTACK_END = 180

# Malicious phase
# The attacker continuously forces the traffic light
# to remain in this phase.
MALICIOUS_PHASE = 0


# ============================================================
# Start SUMO
# ============================================================

sumo_binary = "sumo-gui"

sumo_cmd = [
    sumo_binary,
    "-c",
    SUMO_CONFIG,
    "--start",
    "--quit-on-end"
]

print("=" * 60)
print("SMARTCITY-X")
print("TRAFFIC SIGNAL MANIPULATION ATTACK")
print("=" * 60)

print("\n[INFO] Starting SUMO simulation...")
traci.start(sumo_cmd)


# ============================================================
# Telemetry storage
# ============================================================

telemetry = []

max_queue = 0
max_average_wait = 0

attack_active = False


# ============================================================
# Simulation
# ============================================================

for step in range(SIMULATION_STEPS):

    traci.simulationStep()

    # --------------------------------------------------------
    # Get traffic information
    # --------------------------------------------------------

    vehicle_ids = traci.vehicle.getIDList()

    active_vehicles = len(vehicle_ids)

    waiting_vehicles = 0
    total_waiting_time = 0

    for vehicle_id in vehicle_ids:

        waiting_time = traci.vehicle.getAccumulatedWaitingTime(
            vehicle_id
        )

        total_waiting_time += waiting_time

        if waiting_time > 0:
            waiting_vehicles += 1

    if active_vehicles > 0:
        average_wait = (
            total_waiting_time / active_vehicles
        )
    else:
        average_wait = 0


    # --------------------------------------------------------
    # Get current traffic signal phase
    # --------------------------------------------------------

    current_phase = traci.trafficlight.getPhase(
        TRAFFIC_LIGHT_ID
    )


    # ========================================================
    # ATTACK
    # ========================================================

    if ATTACK_START <= step < ATTACK_END:

        # Print attack start message
        if not attack_active:

            attack_active = True

            print("\n" + "!" * 60)
            print("[ATTACK STARTED]")
            print("Target:", TRAFFIC_LIGHT_ID)
            print("Attack: Traffic Signal Manipulation")
            print("Malicious phase:", MALICIOUS_PHASE)
            print("!" * 60)

        # ----------------------------------------------------
        # Malicious controller command
        # ----------------------------------------------------

        traci.trafficlight.setPhase(
            TRAFFIC_LIGHT_ID,
            MALICIOUS_PHASE
        )

        current_phase = MALICIOUS_PHASE

    else:

        # Detect end of attack
        if attack_active:

            attack_active = False

            print("\n" + "!" * 60)
            print("[ATTACK ENDED]")
            print("Traffic controller released.")
            print("!" * 60)


    # ========================================================
    # Track attack impact
    # ========================================================

    if waiting_vehicles > max_queue:
        max_queue = waiting_vehicles

    if average_wait > max_average_wait:
        max_average_wait = average_wait


    # ========================================================
    # Store telemetry
    # ========================================================

    telemetry.append(
        {
            "time": step,
            "phase": current_phase,
            "active_vehicles": active_vehicles,
            "waiting_vehicles": waiting_vehicles,
            "average_wait": round(average_wait, 2),
            "attack_active": (
                ATTACK_START <= step < ATTACK_END
            )
        }
    )


    # ========================================================
    # Display telemetry
    # ========================================================

    if step % 10 == 0:

        status = (
            "ATTACK"
            if ATTACK_START <= step < ATTACK_END
            else "NORMAL"
        )

        print(
            f"[{status}] "
            f"Time: {step:3d} | "
            f"Phase: {current_phase} | "
            f"Active: {active_vehicles:2d} | "
            f"Waiting: {waiting_vehicles:2d} | "
            f"Avg Wait: {average_wait:6.2f}s"
        )

    time.sleep(0.2)


# ============================================================
# Stop SUMO
# ============================================================

traci.close()


# ============================================================
# Save attack telemetry
# ============================================================

project_root = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        ".."
    )
)

telemetry_path = os.path.join(
    os.path.dirname(__file__),
    "attack_telemetry.json"
)


with open(
    telemetry_path,
    "w"
) as file:

    json.dump(
        telemetry,
        file,
        indent=4
    )


# ============================================================
# Final Attack Report
# ============================================================

print("\n")
print("=" * 60)
print("TRAFFIC SIGNAL ATTACK COMPLETE")
print("=" * 60)

print(
    f"Maximum queue: "
    f"{max_queue} vehicles"
)

print(
    f"Maximum average wait: "
    f"{max_average_wait:.2f} seconds"
)

print(
    f"\n[TELEMETRY] Saved to:"
)

print(telemetry_path)

print("=" * 60)