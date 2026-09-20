from typing import Any


def success_response(data: Any, *, status: str = "ok") -> dict[str, Any]:
    return {"status": status, "data": data}


def error_response(code: str, message: str) -> dict[str, Any]:
    return {"status": "error", "error": {"code": code, "message": message}}
