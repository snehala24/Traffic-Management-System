import streamlit as st
import requests
import numpy as np
import cv2
import json
import pandas as pd
import os

# ---------------- CSS ----------------
def load_css():
    st.markdown("""
    <style>
    body { background-color: #0e1117; color: #ffffff; }
    .stApp { background-color: #0e1117; }
    h1, h2, h3 { color: #00ffcc; }

    .stButton>button {
        background-color: #ff4b4b;
        color: white;
        border-radius: 10px;
        height: 3em;
        width: 100%;
        font-size: 16px;
    }

    .stButton>button:hover { background-color: #ff1c1c; }

    .stTextInput>div>div>input,
    .stSelectbox>div>div {
        background-color: #1f2937;
        color: white;
    }

    </style>
    """, unsafe_allow_html=True)

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Smart Traffic AI", layout="wide")
load_css()

st.markdown("<h1 style='text-align: center;'>🚓 SMART TRAFFIC AI SYSTEM</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center;'>Police Monitoring & Violation Detection Dashboard</h4>", unsafe_allow_html=True)
st.markdown("---")

menu = st.sidebar.selectbox(
    "Menu", ["Dashboard", "Detection", "Live Camera", "Logs", "E-Challan"]
)

# ---------------- DASHBOARD ----------------
if menu == "Dashboard":
    st.subheader("📊 System Overview")

    col1, col2, col3 = st.columns(3)
    col1.metric("🚨 Total Violations", "LIVE")
    col2.metric("📷 Active Cameras", "3")
    col3.metric("🟢 System Status", "ONLINE")

    st.markdown("### 📈 Violation Analytics")

    try:
        with open("../data/logs.json") as f:
            logs = json.load(f)

        if logs:
            counts = {}

            for log in logs:
                data = log.get("data", {})
                for v in data.get("violations", []):
                    counts[v] = counts.get(v, 0) + 1

            st.bar_chart(counts)
        else:
            st.info("No data yet")

    except:
        st.warning("No analytics available")

# ---------------- DETECTION ----------------
elif menu == "Detection":
    st.subheader("📸 Upload Traffic Image")

    signal = st.selectbox("Traffic Signal", ["RED", "GREEN"])
    file = st.file_uploader("Upload Image")

    if file:
        st.image(file, use_column_width=True)

        if st.button("🚨 Detect Violation"):
            response = requests.post(
                "http://127.0.0.1:5000/detect",
                files={"image": file},
                data={"signal": signal}
            )

            result = response.json()

            st.subheader("🚨 Violations Detected")
            for v in result["violations"]:
                if "No Violation" in v:
                    st.success(v)
                else:
                    st.error(v)

            # Vehicle details
            st.subheader("🚗 Vehicle Details")
            st.success(f"Number Plate: {result['plate']}")

            # Auto challan
            st.subheader("🧾 Auto E-Challan")
            for v in result["violations"]:
                if "No Violation" not in v:
                    fine = "₹500" if "Helmet" in v else "₹1000"
                    st.error(f"""
                    🚓 Traffic Police  
                    Vehicle: {result['plate']}  
                    Violation: {v}  
                    Fine: {fine}
                    """)

            # Show processed image
            img_bytes = bytes.fromhex(result["image"])
            nparr = np.frombuffer(img_bytes, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            st.image(img, channels="BGR", use_column_width=True)

# ---------------- LIVE CAMERA ----------------
elif menu == "Live Camera":
    st.subheader("🎥 Live Traffic Monitoring")

    run = st.checkbox("Start Camera")

    if run:
        cap = cv2.VideoCapture(0)
        frame_window = st.image([])

        while run:
            ret, frame = cap.read()
            if not ret:
                st.error("Camera not working")
                break

            _, img_encoded = cv2.imencode('.jpg', frame)

            try:
                response = requests.post(
                    "http://127.0.0.1:5000/detect",
                    files={"image": img_encoded.tobytes()}
                )

                result = response.json()

                img_bytes = bytes.fromhex(result["image"])
                nparr = np.frombuffer(img_bytes, np.uint8)
                img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

                frame_window.image(img, channels="BGR")

            except:
                st.error("Backend not responding")

        cap.release()

# ---------------- LOGS ----------------
elif menu == "Logs":
    st.subheader("📋 Violation Logs + Evidence")

    try:
        with open("../data/logs.json") as f:
            logs = json.load(f)

        for log in logs[::-1]:
            data = log.get("data", {})

            st.write("⏰ Time:", log.get("time"))
            st.write("🚗 Plate:", data.get("plate"))
            st.write("⚠️ Violations:", data.get("violations"))

            img_file = data.get("evidence_image")
            if img_file:
                path = f"../data/evidence/{img_file}"
                if os.path.exists(path):
                    st.image(path)

            st.markdown("---")

    except:
        st.error("Logs not found")

# ---------------- E-CHALLAN ----------------
elif menu == "E-Challan":
    st.subheader("🧾 Manual E-Challan System")

    name = st.text_input("Owner Name")
    vehicle = st.text_input("Vehicle Number")
    violation = st.selectbox("Violation Type", ["No Helmet", "Signal Jump"])
    fine = st.selectbox("Fine Amount", ["₹500", "₹1000", "₹2000"])

    if st.button("Generate Challan"):
        st.success("✅ Challan Generated Successfully!")

        st.markdown("### 🚓 Traffic Police Department")
        st.write(f"👤 Owner: {name}")
        st.write(f"🚗 Vehicle: {vehicle}")
        st.write(f"⚠️ Violation: {violation}")
        st.write(f"💰 Fine: {fine}")

        st.info("Future Scope: Payment Gateway Integration")