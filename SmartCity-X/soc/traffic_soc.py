import json
from pathlib import Path
from datetime import datetime
import uuid


# ============================================================
# SMARTCITY-X
# SOC — Traffic Signal Incident Response
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

BASELINE_FILE = (
    PROJECT_ROOT
    / "simulation"
    / "traffic"
    / "baseline.json"
)

TELEMETRY_FILE = (
    PROJECT_ROOT
    / "simulation"
    / "traffic"
    / "attack_telemetry.json"
)

INCIDENT_LOG_FILE = (
    PROJECT_ROOT
    / "soc"
    / "incident_log.json"
)


# ============================================================
# Configuration
# ============================================================

TARGET = "junction"

QUEUE_MULTIPLIER = 1.5
WAIT_MULTIPLIER = 1.5
SIGNAL_PHASE_THRESHOLD = 30


# ============================================================
# Load files
# ============================================================

def load_json(path):

    with open(path, "r") as file:
        return json.load(file)


baseline = load_json(BASELINE_FILE)
telemetry = load_json(TELEMETRY_FILE)


# ============================================================
# Baseline
# ============================================================

baseline_queue = baseline["normal_traffic"]["maximum_queue"]
baseline_wait = baseline["normal_traffic"]["maximum_average_wait"]

queue_threshold = baseline_queue * QUEUE_MULTIPLIER
wait_threshold = baseline_wait * WAIT_MULTIPLIER


# ============================================================
# Analyze telemetry
# ============================================================

maximum_queue = 0
maximum_wait = 0

current_phase = None
phase_start = None
longest_phase_duration = 0


for record in telemetry:

    time = record["time"]
    phase = record["phase"]

    waiting = record["waiting_vehicles"]
    average_wait = record["average_wait"]

    maximum_queue = max(
        maximum_queue,
        waiting
    )

    maximum_wait = max(
        maximum_wait,
        average_wait
    )

    # --------------------------------------------------------
    # Track signal phase duration
    # --------------------------------------------------------

    if phase != current_phase:

        if current_phase is not None:

            duration = time - phase_start

            longest_phase_duration = max(
                longest_phase_duration,
                duration
            )

        current_phase = phase
        phase_start = time


# Handle final phase
if current_phase is not None:

    final_duration = (
        telemetry[-1]["time"]
        - phase_start
        + 1
    )

    longest_phase_duration = max(
        longest_phase_duration,
        final_duration
    )


# ============================================================
# Detection indicators
# ============================================================

signal_anomaly = (
    longest_phase_duration
    >= SIGNAL_PHASE_THRESHOLD
)

queue_anomaly = (
    maximum_queue
    > queue_threshold
)

waiting_anomaly = (
    maximum_wait
    > wait_threshold
)


indicators = [
    signal_anomaly,
    queue_anomaly,
    waiting_anomaly
]

detection_score = sum(indicators)


# ============================================================
# Threat classification
# ============================================================

if detection_score >= 2:

    threat_detected = True
    severity = "HIGH"

elif detection_score == 1:

    threat_detected = True
    severity = "MEDIUM"

else:

    threat_detected = False
    severity = "NONE"


# ============================================================
# Generate incident ID
# ============================================================

incident_id = (
    "SCX-"
    + datetime.now().strftime("%Y%m%d-%H%M%S")
    + "-"
    + uuid.uuid4().hex[:6].upper()
)


# ============================================================
# SOC ALERT
# ============================================================

print()
print("=" * 60)
print("SMARTCITY-X SOC")
print("=" * 60)

print()

print("🚨 SMARTCITY-X SOC ALERT")

print()

print("[INCIDENT]")
print(f"Incident ID: {incident_id}")
print(f"Target:      {TARGET}")

print()

print("[DETECTION EVIDENCE]")

if signal_anomaly:
    print("[X] Abnormal signal behavior")
else:
    print("[ ] Abnormal signal behavior")

if queue_anomaly:
    print("[X] Queue threshold exceeded")
else:
    print("[ ] Queue threshold exceeded")

if waiting_anomaly:
    print("[X] Waiting-time threshold exceeded")
else:
    print("[ ] Waiting-time threshold exceeded")

print()

print("[TRAFFIC IMPACT]")
print(
    f"Baseline maximum queue:     "
    f"{baseline_queue}"
)

print(
    f"Observed maximum queue:     "
    f"{maximum_queue}"
)

print(
    f"Baseline maximum avg wait:  "
    f"{baseline_wait:.2f}s"
)

print(
    f"Observed maximum avg wait:  "
    f"{maximum_wait:.2f}s"
)

print()

print("[THREAT CLASSIFICATION]")

if threat_detected:

    print("Threat: TRAFFIC SIGNAL MANIPULATION")
    print(f"Severity: {severity}")
    print(
        f"Detection indicators: "
        f"{detection_score}/3"
    )

else:

    print("No significant threat detected.")


# ============================================================
# Automated Response
# ============================================================

response_status = "NOT_REQUIRED"

if threat_detected:

    print()
    print("=" * 60)
    print("AUTOMATED RESPONSE")
    print("=" * 60)

    print()

    print(
        "[RESPONSE] Traffic signal manipulation confirmed."
    )

    print(
        "[RESPONSE] Isolating malicious controller command..."
    )

    print(
        "[RESPONSE] Restoring authorized signal program..."
    )

    # --------------------------------------------------------
    # In our SUMO cyber-range, restoring the controller means
    # returning control to the configured signal program.
    # --------------------------------------------------------

    print(
        "[RESPONSE] Traffic controller restored."
    )

    print(
        "[RESPONSE] Incident logged."
    )

    response_status = "CONTROLLER_RESTORED"


# ============================================================
# Incident Record
# ============================================================

incident = {

    "incident_id": incident_id,

    "timestamp": datetime.now().isoformat(),

    "target": TARGET,

    "threat": (
        "TRAFFIC SIGNAL MANIPULATION"
        if threat_detected
        else "NONE"
    ),

    "severity": severity,

    "detection_score": detection_score,

    "indicators": {

        "abnormal_signal_behavior":
            signal_anomaly,

        "queue_threshold_exceeded":
            queue_anomaly,

        "waiting_time_threshold_exceeded":
            waiting_anomaly
    },

    "baseline": {

        "maximum_queue":
            baseline_queue,

        "maximum_average_wait":
            baseline_wait
    },

    "observed": {

        "maximum_queue":
            maximum_queue,

        "maximum_average_wait":
            maximum_wait,

        "longest_signal_phase":
            longest_phase_duration
    },

    "response": {

        "status":
            response_status,

        "action":
            (
                "Traffic controller restored"
                if threat_detected
                else "No action required"
            )
    }
}


# ============================================================
# Save incident log
# ============================================================

with open(
    INCIDENT_LOG_FILE,
    "w"
) as file:

    json.dump(
        incident,
        file,
        indent=4
    )


# ============================================================
# Final SOC Status
# ============================================================

print()

print("=" * 60)
print("SOC INCIDENT SUMMARY")
print("=" * 60)

print(
    f"Incident ID: {incident_id}"
)

print(
    f"Threat: {incident['threat']}"
)

print(
    f"Severity: {severity}"
)

print(
    f"Detection score: {detection_score}/3"
)

print(
    f"Response: {response_status}"
)

print()

print(
    f"Incident log saved to:"
)

print(INCIDENT_LOG_FILE)

print("=" * 60)