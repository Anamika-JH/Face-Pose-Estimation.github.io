# 📌 Face Pose Estimation

This project demonstrates a real-time **Face Pose Estimation** system that integrates computer vision techniques with Unity for dynamic head tracking and visualization.

---

## 🚀 Methodology

The system consists of two key components:

1. **Real-Time Face Pose Estimation (Python)**  
2. **Head Movement Synchronization in Unity (C#)**

### 🧠 1️⃣ Real-Time Face Pose Estimation

- The Python script `Face PoseV2.py` utilizes **OpenCV** and **Dlib** to detect 68 facial landmarks from a live webcam feed.
- Using the **Perspective-n-Point (PnP)** algorithm along with camera calibration parameters, it estimates the **rotation and translation vectors** that describe the head’s position and orientation in 3D space.
- The translation vectors are transmitted via **UDP (User Datagram Protocol)** to Unity for real-time synchronization.

### 🎮 2️⃣ Head Movement Synchronization in Unity

- The C# script `CameraMovement.cs` receives the pose data over UDP in Unity.
- This script processes the incoming translation vectors and applies them to the **Main Camera** in Unity, enabling real-time camera adjustments that correspond to the user’s head movements.
- ⚠️ **Note:** Attach `CameraMovement.cs` to the **Main Camera** in Unity to enable head tracking functionality.

---

## 📂 Files Included

- `Face PoseV2.py` – Python script for real-time face pose estimation and UDP data transmission.
- `CameraMovement.cs` – Unity C# script to control the Main Camera based on received pose data.
- `shape_predictor_68_face_landmarks.dat` - can be accessed [here](https://drive.google.com/file/d/1jKrKU81QQF_IGWWxc230nFELWEaVGira/view?usp=drive_link)
---

## ⚙️ Setup Instructions

### 💻 For Python:
1. **Install the required libraries:**
   ```bash
   pip install opencv-python dlib numpy
2. **Move shape_predictor_68_face_landmarks.dat to Codes folder**

### 🎯 For Unity:
1. **Create a new Unity project.**
2. **Attach CameraMovement.cs to the Main Camera in your Unity scene.**

## 🎥 Video Demonstration

For a video demonstration of the project, [visit the webpage here](https://anamika-jh.github.io/Face-Pose-Estimation.github.io/).


## Acknowledgments
Parts of this project page were adopted from the [Nerfies](https://nerfies.github.io/) page.

## Website License
<a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/">Creative Commons Attribution-ShareAlike 4.0 International License</a>.
