from flask import Flask, jsonify, send_from_directory
import os
import secrets
from datetime import datetime


# ============================================================
# SMARTCITY-X
# CCTV SIMULATOR
# ============================================================

app = Flask(__name__)


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VIDEO_DIR = os.path.join(BASE_DIR, "videos")


# ============================================================
# CAMERA DATABASE
# ============================================================

CAMERAS = {

    "CAM-01": {
        "id": "CAM-01",
        "location": "Main Street Intersection",
        "video": "CAM-01.mp4",
        "username": "admin",
        "password": "admin",
        "status": "ONLINE",
        "authentication": "AUTHORIZED",
        "session": "LEGITIMATE",
        "stream": "ACTIVE",
        "active_token": None
    },

    "CAM-02": {
        "id": "CAM-02",
        "location": "City Center",
        "video": "CAM-02.mp4",
        "username": "admin",
        "password": "admin",
        "status": "ONLINE",
        "authentication": "AUTHORIZED",
        "session": "LEGITIMATE",
        "stream": "ACTIVE",
        "active_token": None
    },

    "CAM-03": {
        "id": "CAM-03",
        "location": "Public Parking Area",
        "video": "CAM-03.mp4",
        "username": "admin",
        "password": "admin",
        "status": "ONLINE",
        "authentication": "AUTHORIZED",
        "session": "LEGITIMATE",
        "stream": "ACTIVE",
        "active_token": None
    }
}


# ============================================================
# ATTACK STATE
# ============================================================

ATTACK_STATE = {

    "active": False,

    "camera": None,

    "authentication_failures": 0,

    "successful_login": False,

    "unauthorized_session": False,

    "legitimate_session_terminated": False,

    "stream_interrupted": False,

    "attacker_token": None
}


# ============================================================
# STATUS
# ============================================================

@app.route("/api/cctv/status", methods=["GET"])
def cctv_status():

    return jsonify({

        "cameras": CAMERAS,

        "attack": ATTACK_STATE

    })


# ============================================================
# CAMERA STATUS
# ============================================================

@app.route("/api/cctv/<camera_id>", methods=["GET"])
def camera_status(camera_id):

    camera = CAMERAS.get(camera_id)

    if not camera:

        return jsonify({
            "error": "Camera not found"
        }), 404

    return jsonify(camera)


# ============================================================
# VIDEO STREAM
# ============================================================

@app.route("/api/cctv/<camera_id>/video")
def camera_video(camera_id):

    camera = CAMERAS.get(camera_id)

    if not camera:

        return jsonify({
            "error": "Camera not found"
        }), 404

    # Stream is unavailable when compromised
    if camera["stream"] != "ACTIVE":

        return jsonify({
            "error": "CCTV stream interrupted"
        }), 503

    return send_from_directory(
        VIDEO_DIR,
        camera["video"]
    )


# ============================================================
# NORMAL CAMERA LOGIN
# ============================================================

@app.route("/api/cctv/<camera_id>/login", methods=["POST"])
def camera_login(camera_id):

    camera = CAMERAS.get(camera_id)

    if not camera:

        return jsonify({
            "error": "Camera not found"
        }), 404

    token = secrets.token_hex(16)

    camera["active_token"] = token

    camera["authentication"] = "AUTHORIZED"
    camera["session"] = "LEGITIMATE"
    camera["stream"] = "ACTIVE"

    return jsonify({

        "success": True,

        "camera": camera_id,

        "session": "LEGITIMATE",

        "token": token

    })


# ============================================================
# RESET CAMERA
# ============================================================

@app.route("/api/cctv/<camera_id>/reset", methods=["POST"])
def reset_camera(camera_id):

    camera = CAMERAS.get(camera_id)

    if not camera:

        return jsonify({
            "error": "Camera not found"
        }), 404

    camera["status"] = "ONLINE"

    camera["authentication"] = "AUTHORIZED"

    camera["session"] = "LEGITIMATE"

    camera["stream"] = "ACTIVE"

    camera["active_token"] = None

    ATTACK_STATE.update({

        "active": False,

        "camera": None,

        "authentication_failures": 0,

        "successful_login": False,

        "unauthorized_session": False,

        "legitimate_session_terminated": False,

        "stream_interrupted": False,

        "attacker_token": None

    })

    return jsonify({

        "success": True,

        "message": "Camera restored",

        "camera": camera_id

    })


# ============================================================
# HEALTH CHECK
# ============================================================

@app.route("/api/health")
def health():

    return jsonify({

        "system": "SMARTCITY-X CCTV",

        "status": "ONLINE",

        "timestamp": datetime.now().isoformat()

    })


# ============================================================
# START SERVER
# ============================================================

if __name__ == "__main__":

    print("=" * 60)
    print("          SMARTCITY-X CCTV SERVER")
    print("=" * 60)

    print()

    print("Cameras:")

    for camera_id, camera in CAMERAS.items():

        print(
            f"  {camera_id} | "
            f"{camera['location']} | "
            f"{camera['status']}"
        )

    print()

    print("Video directory:")
    print(VIDEO_DIR)

    print()

    print("Server: http://127.0.0.1:5001")

    print()

    app.run(
        host="127.0.0.1",
        port=5001,
        debug=False
    )