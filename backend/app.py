from flask import Flask, request, jsonify
import cv2
import numpy as np
import os
from datetime import datetime

from detection import detect_objects_with_boxes
from violation import check_violation
from database import save_log
from number_plate import generate_number_plate

app = Flask(__name__)

# ---------------- CONFIG ----------------
EVIDENCE_FOLDER = "../data/evidence"
os.makedirs(EVIDENCE_FOLDER, exist_ok=True)


# ---------------- HOME ROUTE ----------------
@app.route("/")
def home():
    return "🚓 Smart Traffic AI Backend is Running Successfully!"


# ---------------- DETECTION ROUTE ----------------
@app.route("/detect", methods=["POST"])
def detect():
    try:
        # Validate input
        if "image" not in request.files:
            return jsonify({"status": "error", "message": "No image provided"}), 400

        file = request.files["image"]
        signal = request.form.get("signal", "RED")

        # Convert image
        img = cv2.imdecode(
            np.frombuffer(file.read(), np.uint8),
            cv2.IMREAD_COLOR
        )

        if img is None:
            return jsonify({"status": "error", "message": "Invalid image"}), 400

        # ---------------- AI DETECTION ----------------
        detections, output_img = detect_objects_with_boxes(img)

        # ---------------- VIOLATION CHECK ----------------
        violations = check_violation(detections, signal)

        # ---------------- NUMBER PLATE ----------------
        plate = generate_number_plate()

        # ---------------- SAVE EVIDENCE ----------------
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        image_filename = f"{plate}_{timestamp}.jpg"
        image_path = os.path.join(EVIDENCE_FOLDER, image_filename)

        cv2.imwrite(image_path, output_img)

        # ---------------- SAVE LOG ----------------
        log_data = {
            "plate": plate,
            "violations": violations,
            "signal": signal,
            "evidence_image": image_filename,
            "timestamp": timestamp
        }

        save_log(log_data)

        # ---------------- ENCODE IMAGE ----------------
        _, buffer = cv2.imencode(".jpg", output_img)

        # ---------------- RESPONSE ----------------
        return jsonify({
            "status": "success",
            "plate": plate,
            "violations": violations,
            "signal": signal,
            "timestamp": timestamp,
            "evidence_image": image_filename,
            "image": buffer.tobytes().hex()
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# ---------------- HEALTH CHECK ----------------
@app.route("/health")
def health():
    return jsonify({
        "status": "running",
        "service": "Smart Traffic AI Backend"
    })


# ---------------- RUN SERVER ----------------
if __name__ == "__main__":
    app.run(debug=True)