def check_violation(detections, signal="RED"):
    violations = []

    person_count = detections.count(0)
    vehicle_detected = (2 in detections or 3 in detections)

    # -------- HELMET LOGIC (IMPROVED SIMULATION) --------
    # Assume violation only if person + bike together
    if person_count > 0 and 3 in detections:
        violations.append("Possible No Helmet")

    # -------- SIGNAL LOGIC --------
    if vehicle_detected and signal == "RED":
        violations.append("Signal Jump")

    if not violations:
        return ["No Violation ✅"]

    return violations