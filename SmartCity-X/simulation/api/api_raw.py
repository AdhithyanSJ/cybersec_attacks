import requests
import json

TARGET = "http://127.0.0.1:3000"
ENDPOINT = "/rest/admin/application-configuration"

URL = TARGET + ENDPOINT
BURP_PROXY = "http://127.0.0.1:8080"

print("=" * 60)
print("        SMARTCITY-X API RESPONSE INSPECTOR")
print("=" * 60)

print(f"Target: {URL}")
print(f"Proxy : {BURP_PROXY}")
print()

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

    print("[ERROR] Request failed")
    print(e)
    exit()


print(f"HTTP Status: {response.status_code}")
print(f"Response Size: {len(response.content)} bytes")
print()

try:

    data = response.json()

except ValueError:

    print("[ERROR] Response is not valid JSON")
    print(response.text[:2000])
    exit()


# ============================================================
# SHOW TOP-LEVEL STRUCTURE
# ============================================================

print("-" * 60)
print("TOP-LEVEL JSON STRUCTURE")
print("-" * 60)

print("Type:", type(data).__name__)

if isinstance(data, dict):

    print("Top-level keys:")

    for key in data.keys():
        print(f"  - {key}")

elif isinstance(data, list):

    print(f"Response contains {len(data)} list elements")


# ============================================================
# INSPECT CONFIG
# ============================================================

print()
print("-" * 60)
print("CONFIG STRUCTURE")
print("-" * 60)

if isinstance(data, dict) and "config" in data:

    config = data["config"]

    print("config type:", type(config).__name__)

    if isinstance(config, dict):

        print("config keys:")

        for key in config.keys():
            print(f"  - {key}")

        print()
        print("First-level config values:")

        for key, value in config.items():

            if isinstance(value, (dict, list)):

                print(
                    f"  {key}: "
                    f"<{type(value).__name__}>"
                )

            else:

                print(f"  {key}: {value}")

    else:

        print("config is not a dictionary")

else:

    print("[!] No top-level 'config' key found")


# ============================================================
# SEARCH FOR IMPORTANT FIELDS RECURSIVELY
# ============================================================

print()
print("-" * 60)
print("SEARCHING ENTIRE RESPONSE")
print("-" * 60)


target_fields = [
    "applicationName",
    "applicationDomain",
    "serverPort",
    "baseUrl",
    "version",
    "localBackupEnabled",
    "geoStalkingMetaSecurityQuestion",
    "geoStalkingMetaSecurityAnswer",
    "geoStalkingVisualSecurityQuestion",
    "geoStalkingVisualSecurityAnswer"
]


def recursive_search(obj, target, path="root"):

    results = []

    if isinstance(obj, dict):

        for key, value in obj.items():

            current_path = f"{path}.{key}"

            if key == target:

                results.append(
                    (current_path, value)
                )

            results.extend(
                recursive_search(
                    value,
                    target,
                    current_path
                )
            )

    elif isinstance(obj, list):

        for index, value in enumerate(obj):

            current_path = f"{path}[{index}]"

            results.extend(
                recursive_search(
                    value,
                    target,
                    current_path
                )
            )

    return results


for field in target_fields:

    matches = recursive_search(data, field)

    if matches:

        print()
        print(f"[FOUND] {field}")

        for path, value in matches[:3]:

            print(f"  Path : {path}")
            print(f"  Value: {value}")

    else:

        print(f"[NOT FOUND] {field}")


# ============================================================
# SAVE COMPLETE RESPONSE FOR INSPECTION
# ============================================================

with open(
    "raw_api_response.json",
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        data,
        file,
        indent=4
    )


print()
print("[+] Full response saved to:")
print("    simulation/api/raw_api_response.json")

print()
print("=" * 60)
print("              INSPECTION COMPLETE")
print("=" * 60)