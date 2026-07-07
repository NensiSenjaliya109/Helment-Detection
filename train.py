from ultralytics import YOLO

def main():
    print("--- Starting Local YOLO Training ---")
    print("Make sure you have downloaded a dataset and unzipped it into this folder!")
    
    # 1. Load the base model
    model = YOLO("yolov8n.pt")
    
    # 2. Start training
    # IMPORTANT: You must change 'data.yaml' to the actual path of your dataset!
    # For example, if you downloaded a dataset folder named 'helmet_dataset', 
    # this should be 'helmet_dataset/data.yaml'
    print("Beginning training process...")
    
    try:
        results = model.train(
            data="data.yaml",  # <-- CHANGE THIS TO YOUR DATASET YAML FILE
            epochs=10,         # 10 is a good number for a laptop CPU test
            imgsz=640
        )
        print("--- Training Complete ---")
        print("Your new brain file is saved in: runs/detect/train/weights/best.pt")
    except Exception as e:
        print(f"\n[ERROR] Training failed. Did you forget to update the data.yaml path?\nError details: {e}")

if __name__ == "__main__":
    main()
