from detector import HelmetDetector
from video_processor import VideoProcessor

def main():
    print("--- Starting Helmet Detection Project ---")
    
    # 1. Initialize the AI Brain
    # Note: The standard 'yolov8n.pt' file will automatically download 
    # from the internet the very first time you run this code.
    print("Step 1: Waking up the AI with our custom brain...")
    # my_detector = HelmetDetector(model_path="yolov8n.pt")  # (The old default brain)
    my_detector = HelmetDetector(model_path="best.pt")  # (Your new custom brain!)
    
    # 2. Initialize the Eyes (Webcam)
    # 0 is usually the built-in laptop webcam. 
    # You can change 0 to "my_video.mp4" if you have a video file to test.
    print("Step 2: Opening the camera...")
    my_processor = VideoProcessor(video_source=0)
    
    # 3. Connect the Brain and the Eyes and start processing!
    print("Step 3: Running detection. (Press 'q' in the video window to stop)")
    my_processor.process_and_display(my_detector)
    
    print("--- Program successfully closed ---")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[INFO] Program was cleanly stopped from the terminal. Goodbye!")
