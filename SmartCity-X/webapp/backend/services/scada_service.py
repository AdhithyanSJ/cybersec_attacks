from typing import Any

from pymodbus.client import ModbusTcpClient

from ..errors import BackendError


PLC_IP = "127.0.0.1"
PLC_PORT = 502
BREAKER_REGISTER = 1024
AUTHORIZED_STATE = 0
MANIPULATED_STATE = 1


def reset_breaker_state() -> dict[str, Any]:
    client = ModbusTcpClient(PLC_IP, port=PLC_PORT)
    try:
        if not client.connect():
            raise BackendError(
                "Could not connect to OpenPLC",
                code="scada_connection_error",
                status_code=502,
            )

        current = client.read_holding_registers(
            address=BREAKER_REGISTER,
            count=1,
        )
        if current.isError():
            raise BackendError(
                "Could not read the OpenPLC breaker register",
                code="scada_read_error",
                status_code=502,
            )

        previous_value = current.registers[0]
        if previous_value == AUTHORIZED_STATE:
            return {
                "status": "NO_RESET_NEEDED",
                "previous_value": previous_value,
                "reset_value": AUTHORIZED_STATE,
                "verified_value": previous_value,
                "response": "MANUAL_RECOVERY",
                "message": "Breaker Command is already 0; no reset was necessary.",
            }

        if previous_value != MANIPULATED_STATE:
            raise BackendError(
                f"Unexpected breaker register value: {previous_value}",
                code="scada_state_error",
                status_code=409,
            )

        write_result = client.write_register(
            address=BREAKER_REGISTER,
            value=AUTHORIZED_STATE,
        )
        if write_result.isError():
            raise BackendError(
                "Could not write the authorized breaker state to OpenPLC",
                code="scada_write_error",
                status_code=502,
            )

        verified = client.read_holding_registers(
            address=BREAKER_REGISTER,
            count=1,
        )
        if verified.isError():
            raise BackendError(
                "Could not verify the recovered OpenPLC breaker register",
                code="scada_verify_error",
                status_code=502,
            )

        verified_value = verified.registers[0]
        if verified_value != AUTHORIZED_STATE:
            raise BackendError(
                f"OpenPLC breaker register verification returned {verified_value}",
                code="scada_verify_error",
                status_code=502,
            )

        return {
            "status": "RECOVERED",
            "previous_value": previous_value,
            "reset_value": AUTHORIZED_STATE,
            "verified_value": verified_value,
            "response": "MANUAL_RECOVERY",
            "message": "Manual recovery completed; Breaker Command is 0.",
        }
    finally:
        client.close()
