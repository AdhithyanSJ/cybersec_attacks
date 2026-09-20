import requests
import json
import os
import time
from datetime import datetime


# ============================================================
# SMARTCITY-X
# CCTV AUTHENTICATION + SESSION COMPROMISE
# ============================================================

SERVER = "http://127.0.0.1:5001"

CAMERA_ID = "CAM-01"

TELEMETRY_FILE = "simulation/cctv/cctv_telemetry.json"


# ============================================================
# CONTROLLED TEST CREDENTIALS
# ============================================================

CREDENTIALS = [

    ("admin", "123456"),

    ("admin", "password"),

    ("admin", "admin")

]


print("=" * 60)
print("        SMARTCITY-X CCTV ATTACK SIMULATION")
print("=" * 60)

print()

print(f"Target Camera : {CAMERA_ID}")

print("Attack        : Authentication + Session Compromise")

print()


# ============================================================
# INITIAL STATUS
# ============================================================

try:

    status = requests.get(
        f"{SERVER}/api/cctv/{CAMERA_ID}",
        timeout=5
    ).json()

except Exception as e:

    print("[ERROR] CCTV server unavailable.")
    print(e)
    exit()


print("-" * 60)
print("                    INITIAL STATE")
print("-" * 60)

print(f"Camera Status : {status['status']}")
print(f"Authentication: {status['authentication']}")
print(f"Session       : {status['session']}")
print(f"Stream        : {status['stream']}")

print()


# ============================================================
# ATTACK
# ============================================================

print("-" * 60)
print("               LAUNCHING ATTACK")
print("-" * 60)

print()

print("[ATTACK] Starting controlled authentication attack...")

authentication_failures = 0

successful_login = False

attacker_token = None


# ============================================================
# BRUTE FORCE
# ============================================================

for username, password in CREDENTIALS:

    print(
        f"[ATTACK] Trying "
        f"{username} / {password} ..."
    )

    time.sleep(0.7)

    # Intentionally controlled local credential test
    if username == "admin" and password == "admin":

        print(
            "[ATTACK] SUCCESS - credentials accepted"
        )

        successful_login = True

        attacker_token = (
            "ATTACKER-" +
            datetime.now().strftime("%H%M%S")
        )

        break

    else:

        authentication_failures += 1

        print("[ATTACK] FAILED")


# ============================================================
# SESSION COMPROMISE
# ============================================================

legitimate_session_terminated = False

stream_interrupted = False

unauthorized_session = False


if successful_login:

    print()

    print(
        "[ATTACK] Unauthorized authentication successful"
    )

    print(
        "[ATTACK] Attacker session established"
    )

    unauthorized_session = True

    print(
        "[ATTACK] Terminating legitimate camera session"
    )

    time.sleep(1)

    legitimate_session_terminated = True

    print(
        "[ATTACK] Legitimate session terminated"
    )

    print(
        "[ATTACK] Interrupting CCTV stream"
    )

    time.sleep(1)

    stream_interrupted = True

    print(
        "[ATTACK] CAM-01 stream interrupted"
    )


# ============================================================
# SAVE TELEMETRY
# ============================================================

telemetry = {

    "timestamp":
        datetime.now().isoformat(),

    "target":
        "CCTV",

    "camera_id":
        CAMERA_ID,

    "camera_location":
        status["location"],

    "authentication_failures":
        authentication_failures,

    "successful_unauthorized_login":
        successful_login,

    "unauthorized_session":
        unauthorized_session,

    "attacker_session":
        attacker_token,

    "legitimate_session_terminated":
        legitimate_session_terminated,

    "stream_interrupted":
        stream_interrupted,

    "attack":
        "CCTV AUTHENTICATION AND SESSION COMPROMISE",

    "impact":
        "UNAUTHORIZED CAMERA ACCESS"

}


os.makedirs(
    "simulation/cctv",
    exist_ok=True
)


with open(
    TELEMETRY_FILE,
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        telemetry,
        file,
        indent=4
    )


# ============================================================
# FINAL RESULT
# ============================================================

print()

print("-" * 60)
print("                    ATTACK RESULT")
print("-" * 60)

if successful_login:

    print(
        "[!] CCTV authentication compromised"
    )

    print(
        "[!] Unauthorized session established"
    )

    print(
        "[!] Legitimate session terminated"
    )

    print(
        "[!] CCTV stream interrupted"
    )

else:

    print(
        "[+] Authentication attack unsuccessful"
    )


print()

print("[+] CCTV telemetry saved")

print(
    f"[+] Telemetry: {TELEMETRY_FILE}"
)

print()

print("=" * 60)
print("          CCTV ATTACK SIMULATION COMPLETE")
print("=" * 60)