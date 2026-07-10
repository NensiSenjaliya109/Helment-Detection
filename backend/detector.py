from ultralytics import YOLO

class HelmetDetector:
    def __init__(self, model_path="yolov8n.pt"):
        """
        Initializes the detector by loading the YOLO model.
        We use 'yolov8n.pt' (YOLOv8 Nano) as a default because it is fast and lightweight.
        If you have a custom trained model for helmets, you would pass its path here (e.g., 'best.pt').
        """
        print(f"Loading model from {model_path}...")
        self.model = YOLO(model_path)
        
        # Let the model use its own class names directly!
        print(f"Model internal classes: {self.model.names}")
        
        print("Model loaded successfully!")

    def detect(self, frame):
        """
        Takes an image (frame), passes it to the AI model, and returns the results.
        """
        # The model looks at the frame and returns a list of results
        # We use stream=True for better performance with continuous video frames
        # conf=0.55 — We raised this threshold to 55% to prevent the AI from "hallucinating" 
        # and falsely detecting dark hair as a dark helmet.
        results = self.model(frame, stream=True, conf=0.55)

        # stream=True is a small optimization that tells YOLO to expect a 
        # continuous stream of images rather than just one random picture,
        #  making it run faster.
        return results
