import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
PORTS_FILE = PROJECT_ROOT / "config" / "ports.json"


def load_ports() -> dict[str, int]:
    with PORTS_FILE.open(encoding="utf-8") as ports_file:
        ports = json.load(ports_file)
    return {name: int(port) for name, port in ports.items()}
