# 🪖 AI-Powered Helmet Detection System

Welcome to the **Helmet Detection System**! This is a complete, production-ready computer vision application built to automatically monitor safety compliance using state-of-the-art AI.

---

# 📌 What is this project?
This project is an automated safety monitoring system. It uses Artificial Intelligence to instantly scan images, recorded videos, or live webcam feeds to determine if individuals are wearing safety helmets. If a violation (no helmet) is detected, it is immediately highlighted and permanently logged to a cloud database for safety auditing.

# ⚙️ How it works
1. **The Brain (AI):** A custom-trained YOLOv8 object detection model (`best.pt`) looks at video frames and mathematically calculates the probability of a "Helmet" or "No Helmet" being present.
2. **The Eyes (OpenCV):** We use OpenCV to process the images, draw bounding boxes (Green for Safe, Red for Danger), and overlay confidence scores.
3. **The Memory (Supabase):** Every time a frame is analyzed, the system securely sends a log to a Supabase PostgreSQL database so managers can view a history of safety violations.
4. **The Face (Streamlit):** Everything is wrapped in a beautiful, dark-mode web dashboard that allows users to interact with the AI without needing to write code.

# 🏗️ Real-World Use Cases
This system is highly valuable in industrial and urban environments where safety is critical:
* **Construction Sites & Manufacturing Plants:** Automatically ensure that all workers entering hazardous zones are wearing hard hats.
* **Smart Traffic Monitoring:** Identify motorcyclists riding without helmets on public roads for automatic ticketing.
* **Mining & Oil Rigs:** Provide 24/7 safety monitoring without requiring human supervisors to stare at camera feeds all day.

---

# 💻 Tech Stack & Why it was chosen
* **Ultralytics YOLOv8:** The industry standard for real-time object detection. Chosen for its incredible speed and accuracy, allowing us to process live webcam video without lag.
* **Streamlit:** A Python web framework. Chosen because it allows us to build a stunning, interactive web dashboard in pure Python without needing to manage complex React/Node.js stacks.
* **OpenCV (`opencv-python`):** The premier computer vision library. Chosen to efficiently handle video stream decoding and frame manipulation (drawing the boxes).
* **Supabase:** An open-source Firebase alternative. Chosen because it provides a seamless, instant cloud PostgreSQL database with a simple Python API for logging our history.

---

# 📂 Project Structure & File Explanation

## 🖥️ `frontend/` (The User Interface)
* `app.py`: The main entry point for the Streamlit dashboard and the "Home" page showing live statistics.
* `pages/1_📷_Image_Detection.py`: UI for uploading static images and running AI inference.
* `pages/2_🎥_Video_Detection.py`: UI for uploading recorded video files and processing them frame-by-frame.
* `pages/3_🔴_Live_Webcam.py`: UI for tapping into your computer's webcam for real-time safety monitoring.
* `pages/4_🗄️_History.py`: Connects to Supabase to display a live feed of all past safety detections.
* `assets/style.css`: Contains custom CSS to make the dashboard look premium with dark mode, shadows, and rounded corners.

## 🧠 `backend/` (The AI Engine & Logic)
* `detector.py`: Contains the `HelmetDetector` class which loads the YOLOv8 model and runs predictions.
* `utils.py`: Reusable helper functions for drawing the red/green bounding boxes on images and triggering database logs.
* `database.py`: Manages the secure connection to the Supabase cloud and handles inserting/fetching history.
* `best.pt`: The custom-trained AI weight file (the "brain" that knows what a helmet looks like).

## 📄 Root Files
* `requirements.txt`: The list of all external Python libraries needed to run the project.
* `.env`: A secret file storing the Supabase URL and API Keys (hidden from GitHub).
* `.gitignore`: A configuration file telling GitHub to ignore large files and secrets (like `.env`).

---

# 🚀 How to Run the Project (For New Users)

If you have just downloaded this project, follow these steps to get it running on your local machine:

**Step 1: Install Dependencies**
Open your terminal and install all the required Python libraries:
```bash
pip install -r requirements.txt
```

**Step 2: Setup Database Secrets**
1. Create a file named `.env` in the root folder of the project.
2. Add your Supabase credentials to the file like this:
```env
SUPABASE_URL=https://your-project-url.supabase.co
SUPABASE_KEY=your-anon-api-key
```

**Step 3: Launch the Dashboard**
Start the web application by running:
```bash
streamlit run frontend/app.py
```
A browser window will automatically open at `http://localhost:8501` showing the dashboard!
