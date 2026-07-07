import cv2
import time
import threading
import tkinter as tk

class VideoProcessor:
    def __init__(self, video_source=0):
        """
        Initializes the video processor. 
        video_source=0 means use the default webcam.
        You could also pass a string like "my_video.mp4" to read a file.
        """
        self.video_source = video_source
        self.cap = cv2.VideoCapture(self.video_source)
        
        # Cooldown timer: only show a popup every 3 seconds
        self.last_notification_time = 0
        self.notification_cooldown = 3  # seconds

    def _show_popup(self, title, message, bg_color):
        """
        Creates a custom popup window at the TOP CENTER of the screen.
        Runs in its own thread so it never freezes the video.
        """
        popup = tk.Tk()
        popup.overrideredirect(True)   # No title bar or borders
        popup.attributes("-topmost", True)  # Always on top of everything
        popup.configure(bg=bg_color)

        # Calculate position: center at the top of screen
        screen_width = popup.winfo_screenwidth()
        popup_width = 450
        popup_height = 90
        x = (screen_width // 2) - (popup_width // 2)
        y = 20  # 20 pixels from the top
        popup.geometry(f"{popup_width}x{popup_height}+{x}+{y}")

        # Title text (bold)
        tk.Label(popup, text=title, font=("Arial", 13, "bold"),
                 bg=bg_color, fg="white").pack(pady=(10, 2))
        # Message text
        tk.Label(popup, text=message, font=("Arial", 10),
                 bg=bg_color, fg="white").pack()

        # Auto-close after 3 seconds
        popup.after(3000, popup.destroy)
        popup.mainloop()

    def _send_notification(self, title, message, is_danger=True):
        """
        Sends the top-center popup in a background thread.
        Only fires if the cooldown (3 seconds) has passed.
        """
        current_time = time.time()
        if current_time - self.last_notification_time > self.notification_cooldown:
            bg_color = "#CC0000" if is_danger else "#007700"  # Red or Green
            t = threading.Thread(target=self._show_popup, args=(title, message, bg_color), daemon=True)
            t.start()
            self.last_notification_time = current_time

    def process_and_display(self, detector):
        """
        Loops through the video frames, uses the detector to find objects,
        draws the results, and displays the video on the screen.
        """
        if not self.cap.isOpened():
            print("Error: Could not open video source.")
            return

        print("Starting video stream... Press 'q' to quit.")

        while True:
            success, frame = self.cap.read()
            
            if not success:
                print("End of video stream.")
                break

            # --- STEP 1: Ask the Brain ---
            results = detector.detect(frame)

            # Track what was found in this frame for notifications
            found_no_helmet = False
            found_helmet = False

            # --- STEP 2: Draw the Boxes MANUALLY ---
            for r in results:
                annotated_frame = frame.copy()
                for box in r.boxes:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    class_id = int(box.cls[0])
                    confidence = float(box.conf[0])

                    label_map = {0: "No Helmet", 1: "Helmet"}
                    label = label_map.get(class_id, f"Class {class_id}")

                    # GREEN for Helmet, RED for No Helmet
                    color = (0, 255, 0) if class_id == 1 else (0, 0, 255)

                    cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), color, 2)
                    display_text = f"{label} {confidence:.2f}"
                    cv2.putText(annotated_frame, display_text, (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

                    # Track what was detected
                    if class_id == 0:
                        found_no_helmet = True
                    elif class_id == 1:
                        found_helmet = True

            # --- STEP 3: Send Popup Notification ---
            if found_no_helmet:
                self._send_notification(
                    title="🚨 DANGER - No Helmet!",
                    message="Person without helmet detected! Wear safety gear!",
                    is_danger=True
                )
            elif found_helmet:
                self._send_notification(
                    title="✅ Safe - Helmet Detected",
                    message="All persons are wearing helmets. Stay safe!",
                    is_danger=False
                )

            # --- STEP 4: Show the Picture ---
            cv2.imshow("Helmet Detection", annotated_frame)

            # --- STEP 5: Check for Exit ---
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        self.cap.release()
        cv2.destroyAllWindows()
