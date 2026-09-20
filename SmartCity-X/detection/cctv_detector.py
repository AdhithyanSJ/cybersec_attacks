import json
import os


# ============================================================
# SMARTCITY-X
# CCTV THREAT DETECTOR
# ============================================================

TELEMETRY_FILE = "simulation/cctv/cctv_telemetry.json"


print("=" * 60)
print("        SMARTCITY-X CCTV THREAT DETECTOR")
print("=" * 60)


# ============================================================
# LOAD TELEMETRY
# ============================================================

if not os.path.exists(TELEMETRY_FILE):

    print("[ERROR] CCTV telemetry not found.")

    exit()


with open(
    TELEMETRY_FILE,
    "r",
    encoding="utf-8"
) as file:

    telemetry = json.load(file)


# ============================================================
# INDICATORS
# ============================================================

indicators = []


# Authentication failures
if telemetry.get("authentication_failures", 0) > 0:

    indicators.append(
        "Multiple failed authentication attempts"
    )


# Unauthorized login
if telemetry.get(
    "successful_unauthorized_login"
):

    indicators.append(
        "Unauthorized camera authentication"
    )


# Unauthorized session
if telemetry.get(
    "unauthorized_session"
):

    indicators.append(
        "Unauthorized camera session"
    )


# Legitimate session terminated
if telemetry.get(
    "legitimate_session_terminated"
):

    indicators.append(
        "Legitimate camera session terminated"
    )


# Stream interruption
if telemetry.get(
    "stream_interrupted"
):

    indicators.append(
        "CCTV stream interruption"
    )


# ============================================================
# SCORE
# ============================================================

score = len(indicators)

total = 5


if score >= 4:

    severity = "HIGH"

elif score >= 2:

    severity = "MEDIUM"

elif score == 1:

    severity = "LOW"

else:

    severity = "NONE"


# ============================================================
# OUTPUT
# ============================================================

print()

print("-" * 60)
print("                  DETECTION RESULTS")
print("-" * 60)


for indicator in indicators:

    print(f"[X] {indicator}")


print()

print(
    "Threat: CCTV AUTHENTICATION AND SESSION COMPROMISE"
)

print(
    f"Severity: {severity}"
)

print(
    f"Detection indicators: {score}/{total}"
)


# ============================================================
# CAMERA DETAILS
# ============================================================

print()

print("-" * 60)
print("                    CAMERA DETAILS")
print("-" * 60)

print(
    f"Camera: "
    f"{telemetry.get('camera_id')}"
)

print(
    f"Location: "
    f"{telemetry.get('camera_location')}"
)

print(
    f"Authentication Failures: "
    f"{telemetry.get('authentication_failures')}"
)

print(
    f"Unauthorized Session: "
    f"{'YES' if telemetry.get('unauthorized_session') else 'NO'}"
)

print(
    f"Stream Interrupted: "
    f"{'YES' if telemetry.get('stream_interrupted') else 'NO'}"
)


# ============================================================
# DECISION
# ============================================================

print()

print("-" * 60)
print("                  DETECTION DECISION")
print("-" * 60)


if score >= 4:

    print("[!] THREAT DETECTED")

    print(
        "[!] CCTV authentication compromise"
    )

    print(
        "[!] Unauthorized camera session"
    )

    print(
        "[!] SOC response required"
    )

elif score >= 2:

    print(
        "[!] Suspicious CCTV activity detected"
    )

else:

    print(
        "[+] No significant CCTV anomaly detected"
    )


print()

print("=" * 60)
print("             CCTV DETECTION COMPLETE")
print("=" * 60)