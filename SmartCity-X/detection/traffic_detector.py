import json
from pathlib import Path


# ============================================================
# SMARTCITY-X
# Traffic Signal Attack Detection Module
# ============================================================

# ------------------------------------------------------------
# Locate project files
# ------------------------------------------------------------

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


# ============================================================
# Configuration
# ============================================================

TARGET = "junction"

# How long a traffic signal staying in the same phase
# is considered suspicious.
SIGNAL_PHASE_THRESHOLD = 30

# Detection thresholds are based on the normal baseline.
QUEUE_MULTIPLIER = 1.5
WAIT_MULTIPLIER = 1.5


# ============================================================
# Load JSON files
# ============================================================

def load_json(file_path):

    with open(file_path, "r") as file:
        return json.load(file)


baseline = load_json(BASELINE_FILE)
telemetry = load_json(TELEMETRY_FILE)


# ============================================================
# Extract baseline values
# ============================================================

baseline_queue = baseline["normal_traffic"]["maximum_queue"]

baseline_wait = baseline["normal_traffic"]["maximum_average_wait"]


# Detection thresholds
queue_threshold = baseline_queue * QUEUE_MULTIPLIER
wait_threshold = baseline_wait * WAIT_MULTIPLIER


# ============================================================
# Analyze telemetry
# ============================================================

maximum_queue = 0
maximum_wait = 0

abnormal_signal = False
queue_anomaly = False
waiting_anomaly = False


# Track consecutive time spent in the same phase
current_phase = None
phase_start_time = None
longest_phase_duration = 0


for record in telemetry:

    time = record["time"]
    phase = record["phase"]

    waiting_vehicles = record["waiting_vehicles"]
    average_wait = record["average_wait"]


    # --------------------------------------------------------
    # Track maximum queue
    # --------------------------------------------------------

    if waiting_vehicles > maximum_queue:
        maximum_queue = waiting_vehicles


    # --------------------------------------------------------
    # Track maximum average waiting time
    # --------------------------------------------------------

    if average_wait > maximum_wait:
        maximum_wait = average_wait


    # --------------------------------------------------------
    # Signal phase anomaly
    # --------------------------------------------------------

    if phase != current_phase:

        # Calculate duration of previous phase
        if current_phase is not None:

            duration = time - phase_start_time

            if duration > longest_phase_duration:
                longest_phase_duration = duration

            if duration >= SIGNAL_PHASE_THRESHOLD:
                abnormal_signal = True

        current_phase = phase
        phase_start_time = time


# ------------------------------------------------------------
# Check final phase duration
# ------------------------------------------------------------

if current_phase is not None:

    final_time = telemetry[-1]["time"]

    duration = final_time - phase_start_time + 1

    if duration > longest_phase_duration:
        longest_phase_duration = duration

    if duration >= SIGNAL_PHASE_THRESHOLD:
        abnormal_signal = True


# ============================================================
# Queue anomaly
# ============================================================

if maximum_queue > queue_threshold:
    queue_anomaly = True


# ============================================================
# Waiting-time anomaly
# ============================================================

if maximum_wait > wait_threshold:
    waiting_anomaly = True


# ============================================================
# Calculate detection score
# ============================================================

indicators = [
    abnormal_signal,
    queue_anomaly,
    waiting_anomaly
]

detection_score = sum(indicators)


# ============================================================
# Determine threat classification
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
# Detection Report
# ============================================================

print()
print("=" * 60)
print("SMARTCITY-X")
print("TRAFFIC ATTACK DETECTION ENGINE")
print("=" * 60)

print()

print("[TARGET]")
print(f"Traffic controller: {TARGET}")

print()

print("[BASELINE]")
print(f"Maximum normal queue:      {baseline_queue}")
print(f"Maximum normal avg wait:   {baseline_wait:.2f}s")

print()

print("[DETECTION THRESHOLDS]")
print(f"Queue threshold:            {queue_threshold:.2f}")
print(f"Waiting-time threshold:     {wait_threshold:.2f}s")
print(f"Signal phase threshold:     {SIGNAL_PHASE_THRESHOLD}s")

print()

print("[OBSERVED TELEMETRY]")
print(f"Maximum observed queue:     {maximum_queue}")
print(f"Maximum observed avg wait:  {maximum_wait:.2f}s")
print(f"Longest signal phase:       {longest_phase_duration}s")

print()

print("=" * 60)
print("ANOMALY INDICATORS")
print("=" * 60)

if abnormal_signal:
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

print("=" * 60)
print("DETECTION RESULT")
print("=" * 60)

if threat_detected:

    print("[ALERT] Traffic anomaly detected")

    print()
    print("Threat: TRAFFIC SIGNAL MANIPULATION")
    print(f"Severity: {severity}")
    print(f"Detection indicators: {detection_score}/3")

else:

    print("[OK] No significant traffic anomaly detected")


print()
print("=" * 60)