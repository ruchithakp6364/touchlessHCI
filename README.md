## Touchless HCI for Media Control Using Hand Gestures

This project implements a **touchless human–computer interaction (HCI)** system that works on **Windows, Linux, and NVIDIA Jetson Nano**.  
Using **MediaPipe Hands**, a USB camera, and Python, it detects real-time hand gestures and translates them into media control commands for a local media player (e.g., VLC).

**Cross-Platform Support:** Works on Windows, Linux (including Jetson Nano), and macOS using `pynput` for keyboard control.

---

### Project Structure

- **`requirements.txt`** – Python dependencies for the gesture control app.
- **`src/gesture_media_control.py`** – Main script: camera capture, hand tracking, gesture recognition, and VLC control.

---

### Hardware Setup (Jetson Nano)

1. **Prepare Jetson Nano**
   - Flash an SD card with a JetPack image (official NVIDIA image).
   - Insert SD card into Jetson Nano.
   - Connect monitor (HDMI/DisplayPort), keyboard, and mouse.
   - Use a **5V 4A** power supply (barrel jack) or a properly powered USB‑C/USB‑micro input as recommended by NVIDIA.

2. **Connect Camera**
   - Plug a **USB webcam** into one of the Jetson Nano USB ports.
   - Place the camera so that it clearly sees your upper body and hands in front of the monitor.

3. **Network & System**
   - Connect Jetson Nano to the internet (Ethernet or Wi‑Fi).
   - Boot, complete initial Ubuntu setup, and open a terminal.

4. **Install Media Player (VLC)**
   ```bash
   sudo apt update
   sudo apt install -y vlc xdotool
   ```
   - Launch VLC at least once to ensure it runs:
   ```bash
   vlc &
   ```
   - Click on the VLC window so it has keyboard focus (important for hotkeys to work).

---

### Software Setup

#### On Windows:

1. **Install Python dependencies**

   From the project root (where `requirements.txt` is located):

   ```cmd
   pip install -r requirements.txt
   ```

2. **Install VLC Media Player**
   - Download from https://www.videolan.org/vlc/
   - Install and launch VLC

3. **Test camera**
   ```cmd
   python -c "import cv2; cap = cv2.VideoCapture(0); ret, frame = cap.read(); print('Camera OK:', ret); cap.release()"
   ```

#### On Linux/Jetson Nano:

1. **Install Python dependencies**

   From the project root (where `requirements.txt` is located):

   ```bash
   sudo apt update
   sudo apt install -y python3-pip python3-opencv

   pip3 install -r requirements.txt
   ```

2. **Install VLC**
   ```bash
   sudo apt update
   sudo apt install -y vlc
   ```

2. **Confirm camera works**

   ```bash
   python3 - << 'EOF'
   import cv2
   cap = cv2.VideoCapture(0)
   ret, frame = cap.read()
   print("Camera OK:", ret, "Frame shape:" if ret else "", frame.shape if ret else "")
   cap.release()
   EOF
   ```

---

### Running the Gesture Control App

#### On Windows:

1. **Start VLC**
   - Open VLC Media Player
   - Load a media file (video or audio)
   - **Click on the VLC window** to ensure it has keyboard focus

2. **Run the gesture controller**

   From the project root:

   ```cmd
   cd src
   python gesture_media_control.py
   ```

#### On Linux/Jetson Nano:

1. **Start VLC**
   - Open a terminal on Jetson Nano and run:
   ```bash
   vlc &
   ```
   - Load a media file and keep VLC playing/paused; **click once on the VLC window** to ensure it has focus.

2. **Run the gesture controller**

   From the project root:

   ```bash
   cd src
   python3 gesture_media_control.py
   ```

3. **Use the gestures in front of the camera** (same for all platforms)

   - **Open palm (all fingers up)** → Play/Pause (`space`)
   - **Fist (all fingers closed)** → Stop (`s`)
   - **Thumb up** (thumb extended up, other fingers closed) → Volume Up (`Ctrl+Up`)
   - **Thumb down** (thumb extended down, other fingers closed) → Volume Down (`Ctrl+Down`)
   - **Index pointing and moving right** → Next track (`n`)
   - **Index pointing and moving left** → Previous track (`p`)

   The window titled **"Hand Gesture Media Control"** will show:
   - Detected hand landmarks
   - Current recognized gesture
   - Approximate FPS

4. **Quit**

   - Press **`q`** while the OpenCV window is active to exit the program.

---

### Notes for Performance and Accuracy

- Use **moderate, even lighting**; avoid very bright backlights and very dark rooms.
- Keep the hand roughly at the same distance from the camera during use.
- Gesture thresholds (for movement and thumb direction) can be tuned directly in `gesture_media_control.py`.
- For better performance:
  - Resolution is set to **640×480**.
  - MediaPipe Hands is configured with `model_complexity=0` and `max_num_hands=1` to keep latency low on Jetson Nano.

## 🎥 Demo Video

Watch the project demo here:

👉 https://youtu.be/GmmsfG5WTk8?si=KZfpPczzZdsBfcBX

---

## 📄 Documentation

Full project documentation:

👉 [Download Project Report](docs/hci-aisoc.docx)

---

## 🚀 Project Overview

Touchless Human–Computer Interaction system using:

- Jetson Nano 2GB Edge AI deployment
- Real-time hand gesture recognition
- Media player control using gestures
- OLED display integration for feedback
- Optimized for low-resource hardware
