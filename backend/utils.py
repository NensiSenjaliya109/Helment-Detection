import cv2
from backend import database

def draw_boxes(frame, results, log_to_db=False):
    """
    Draws bounding boxes on the given frame based on YOLO results.
    Optionally logs detections to the Supabase database.
    Returns the annotated frame, and stats about what was detected.
    """
    annotated_frame = frame.copy()
    
    found_no_helmet = False
    found_helmet = False
    max_danger_conf = 0.0
    max_safe_conf = 0.0
    
    helmet_count = 0
    no_helmet_count = 0

    for r in results:
        for box in r.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            class_id = int(box.cls[0])
            confidence = float(box.conf[0])

            label_map = {0: "Helmet", 1: "No Helmet"}
            label = label_map.get(class_id, f"Class {class_id}")

            # GREEN for Helmet ✅, RED for No Helmet 🚨
            color = (0, 255, 0) if class_id == 0 else (0, 0, 255)

            cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), color, 2)
            display_text = f"{label} {confidence:.2f}"
            cv2.putText(annotated_frame, display_text, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

            # Track what was detected
            if class_id == 0:
                found_helmet = True
                helmet_count += 1
                max_safe_conf = max(max_safe_conf, confidence)
            elif class_id == 1:
                found_no_helmet = True
                no_helmet_count += 1
                max_danger_conf = max(max_danger_conf, confidence)

    # Database logging if requested (e.g. for images/videos processing directly via Streamlit)
    if log_to_db:
        if found_no_helmet:
            database.log_detection("Danger", max_danger_conf)
        elif found_helmet:
            database.log_detection("Safe", max_safe_conf)

    stats = {
        "helmet_count": helmet_count,
        "no_helmet_count": no_helmet_count,
        "danger": found_no_helmet,
        "max_danger_conf": max_danger_conf,
        "max_safe_conf": max_safe_conf
    }
    
    return annotated_frame, stats
