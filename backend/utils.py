import cv2
from backend import database

def draw_boxes(frame, results, log_to_db=False):
    """
    Draws bounding boxes on the given frame based on YOLO results.
    Optionally logs detections to the Supabase database.
    Returns the annotated frame, and stats about what was detected.
    
    Uses the model's ACTUAL class names to determine Safe vs Danger.
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

            # Get the REAL class name from the model
            label = r.names.get(class_id, f"Class {class_id}").lower()

            # --- CLASSIFICATION LOGIC ---
            # Model Classes: {0: 'full', 1: 'half', 2: 'invalid', 3: 'no-helmet'}
            # HELMET (Safe):      full, half
            # NO HELMET (Danger): invalid, no-helmet
            
            # If it's a full or half helmet, it's safe. Otherwise, it's danger!
            is_helmet = label in ["full", "half"]

            if is_helmet:
                color = (0, 255, 0)  # GREEN for Helmet ✅
                display_label = "Helmet"
                found_helmet = True
                helmet_count += 1
                max_safe_conf = max(max_safe_conf, confidence)
            else:
                color = (0, 0, 255)  # RED for No Helmet 🚨
                display_label = "No Helmet"
                found_no_helmet = True
                no_helmet_count += 1
                max_danger_conf = max(max_danger_conf, confidence)

            cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), color, 2)
            display_text = f"{display_label} {confidence:.2f}"
            cv2.putText(annotated_frame, display_text, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

    # Database logging
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

