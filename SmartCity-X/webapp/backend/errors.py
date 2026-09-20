from flask import jsonify

from .schemas import error_response


class BackendError(Exception):
    def __init__(self, message: str, *, code: str = "backend_error", status_code: int = 400):
        super().__init__(message)
        self.code = code
        self.status_code = status_code


def register_error_handlers(app) -> None:
    @app.errorhandler(BackendError)
    def handle_backend_error(error: BackendError):
        return jsonify(error_response(error.code, str(error))), error.status_code

    @app.errorhandler(404)
    def handle_not_found(_error):
        return jsonify(error_response("not_found", "The requested resource was not found")), 404

    @app.errorhandler(500)
    def handle_internal_error(_error):
        return jsonify(error_response("internal_error", "The backend could not complete the request")), 500
