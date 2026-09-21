from datetime import datetime, timezone

from flask import Flask, jsonify

from .config import load_ports
from .errors import register_error_handlers
from .routes.cctv import cctv_bp
from .routes.attacks import attacks_bp
from .schemas import success_response
from .services.cctv_service import CCTVService
from .routes.scada import scada_bp

from flask_cors import CORS


def create_app() -> Flask:
    app = Flask(__name__)
    CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:5173"]
    }
})
    app.config["PORTS"] = load_ports()
    app.extensions["cctv_service"] = CCTVService()
    app.register_blueprint(cctv_bp)
    app.register_blueprint(attacks_bp)
    app.register_blueprint(scada_bp)
    register_error_handlers(app)

    @app.get("/api/health")
    def health():
        return jsonify(
            success_response(
                {
                    "service": "SmartCity-X orchestration backend",
                    "status": "ONLINE",
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "port": app.config["PORTS"]["backend"],
                }
            )
        )

    @app.get("/api/status")
    def status():
        return jsonify(
            success_response(
                {
                    "service": "SmartCity-X orchestration backend",
                    "status": "ONLINE",
                    "dependencies": {
                        "cctv": {"status": "ONLINE", "checked": True, "mode": "in_process"},
                        "traffic": {"status": "NOT_CONFIGURED", "checked": False},
                        "scada": {"status": "NOT_CONFIGURED", "checked": False},
                        "network": {"status": "NOT_CONFIGURED", "checked": False},
                        "api": {"status": "NOT_CONFIGURED", "checked": False},
                    },
                }
            )
        )

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=app.config["PORTS"]["backend"], debug=False)
