from ultralytics import YOLO
import cv2

model = YOLO("yolov8n.pt")

def detect_objects_with_boxes(image):
    results = model(image)

    detections = []
    annotated_frame = image.copy()

    for r in results:
        for box in r.boxes:
            cls = int(box.cls[0])
            conf = float(box.conf[0])

            x1, y1, x2, y2 = map(int, box.xyxy[0])

            label = f"ID:{cls} {conf:.2f}"

            cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), (0,255,0), 2)
            cv2.putText(annotated_frame, label, (x1, y1-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)

            detections.append(cls)

    return detections, annotated_frame