import json
import os


# ============================================================
# SMARTCITY-X
# Attack #5 Detection: Unauthorized Admin API Access
# ============================================================

TELEMETRY_FILE = "E:\\cybersec\\SmartCity-X\\simulation\\api\\api_telemetry.json"


print("=" * 60)
print("        SMARTCITY-X API THREAT DETECTOR")
print("=" * 60)


# ============================================================
# LOAD TELEMETRY
# ============================================================

if not os.path.exists(TELEMETRY_FILE):

    print()
    print("[ERROR] API telemetry file not found.")
    print(f"[ERROR] Expected: {TELEMETRY_FILE}")
    print()
    print("Run api_attack.py first.")
    exit()


try:

    with open(
        TELEMETRY_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        telemetry = json.load(file)

except Exception as e:

    print()
    print("[ERROR] Could not read API telemetry.")
    print(f"[ERROR] {e}")
    exit()


# ============================================================
# EXTRACT TELEMETRY
# ============================================================

http_status = telemetry.get("http_status")

authorization_header = telemetry.get(
    "authorization_header"
)

unauthorized_access = telemetry.get(
    "unauthorized_access"
)

admin_configuration_exposed = telemetry.get(
    "admin_configuration_exposed"
)

application_name_exposed = telemetry.get(
    "application_name_exposed"
)

application_domain_exposed = telemetry.get(
    "application_domain_exposed"
)

server_port_exposed = telemetry.get(
    "server_port_exposed"
)

base_url_exposed = telemetry.get(
    "base_url_exposed"
)

security_related_data_exposed = telemetry.get(
    "security_related_data_exposed"
)


# ============================================================
# DETECTION INDICATORS
# ============================================================

indicators = []


# ------------------------------------------------------------
# Indicator 1: Unauthorized Access
# ------------------------------------------------------------

if unauthorized_access:

    indicators.append(
        "Unauthorized API access"
    )


# ------------------------------------------------------------
# Indicator 2: Missing Authorization Header
# ------------------------------------------------------------

if authorization_header is False:

    indicators.append(
        "Missing Authorization header"
    )


# ------------------------------------------------------------
# Indicator 3: Successful HTTP Response
# ------------------------------------------------------------

if http_status == 200:

    indicators.append(
        "Unauthorized request returned HTTP 200"
    )


# ------------------------------------------------------------
# Indicator 4: Administrative Configuration Exposed
# ------------------------------------------------------------

if admin_configuration_exposed:

    indicators.append(
        "Administrative configuration exposed"
    )


# ------------------------------------------------------------
# Indicator 5: Security-Related Data Exposed
# ------------------------------------------------------------

if security_related_data_exposed:

    indicators.append(
        "Security-related application data exposed"
    )


# ============================================================
# ADDITIONAL CONFIGURATION INDICATORS
# ============================================================

configuration_fields_exposed = 0

if application_name_exposed:
    configuration_fields_exposed += 1

if application_domain_exposed:
    configuration_fields_exposed += 1

if server_port_exposed:
    configuration_fields_exposed += 1

if base_url_exposed:
    configuration_fields_exposed += 1


if configuration_fields_exposed >= 2:

    indicators.append(
        "Multiple application configuration fields exposed"
    )


# ============================================================
# DETECTION SCORE
# ============================================================

detection_score = len(indicators)

total_indicators = 6


# ============================================================
# SEVERITY
# ============================================================

if detection_score >= 4:

    severity = "HIGH"

elif detection_score >= 2:

    severity = "MEDIUM"

elif detection_score == 1:

    severity = "LOW"

else:

    severity = "NONE"


# ============================================================
# DISPLAY DETECTION RESULTS
# ============================================================

print()
print("-" * 60)
print("                  DETECTION RESULTS")
print("-" * 60)


if detection_score > 0:

    for indicator in indicators:

        print(f"[X] {indicator}")

else:

    print("[+] No suspicious indicators detected")


print()
print(f"Threat: UNAUTHORIZED ADMIN API ACCESS")
print(f"Severity: {severity}")
print(
    f"Detection indicators: "
    f"{detection_score}/{total_indicators}"
)


# ============================================================
# ATTACK DETAILS
# ============================================================

print()
print("-" * 60)
print("                    ATTACK DETAILS")
print("-" * 60)

print(f"Target: {telemetry.get('target')}")
print(f"Endpoint: {telemetry.get('endpoint')}")
print(f"Method: {telemetry.get('method')}")
print(f"HTTP Status: {http_status}")
print(
    f"Authorization Header: "
    f"{'PRESENT' if authorization_header else 'NOT PROVIDED'}"
)

print(
    f"Configuration Fields Exposed: "
    f"{configuration_fields_exposed}"
)

print(
    f"Security Data Exposed: "
    f"{'YES' if security_related_data_exposed else 'NO'}"
)


# ============================================================
# FINAL DETECTION DECISION
# ============================================================

print()
print("-" * 60)
print("                  DETECTION DECISION")
print("-" * 60)


if detection_score >= 4:

    print("[!] THREAT DETECTED")
    print("[!] Unauthorized administrative API access")
    print("[!] Administrative configuration exposure")
    print("[!] SOC response required")

elif detection_score >= 2:

    print("[!] Suspicious API activity detected")

elif detection_score == 1:

    print("[!] Low-confidence API anomaly detected")

else:

    print("[+] API activity appears normal")


print()
print("=" * 60)
print("              API DETECTION COMPLETE")
print("=" * 60)