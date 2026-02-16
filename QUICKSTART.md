# Quick Start Guide

## Windows Setup (5 minutes)

### 1. Install Dependencies
```cmd
pip install -r requirements.txt
```

### 2. Verify Setup
```cmd
python test_setup.py
```

### 3. Install VLC
Download and install from: https://www.videolan.org/vlc/

### 4. Run the Application
```cmd
cd src
python gesture_media_control.py
```

### 5. Use Gestures
- Open VLC and play a video
- Click on VLC window (must have focus)
- Perform gestures in front of camera:
  - **Open palm** → Play/Pause
  - **Fist** → Stop
  - **Thumbs up** → Volume up
  - **Thumbs down** → Volume down
  - **Point right** (with motion) → Next track
  - **Point left** (with motion) → Previous track

---

## Linux/Jetson Nano Setup

### 1. Install System Dependencies
```bash
sudo apt update
sudo apt install -y python3-pip python3-opencv vlc
```

### 2. Install Python Dependencies
```bash
pip3 install -r requirements.txt
```

### 3. Verify Setup
```bash
python3 test_setup.py
```

### 4. Run the Application
```bash
cd src
python3 gesture_media_control.py
```

---

## Troubleshooting

### Camera not detected
- Check if camera is connected
- Try different USB port
- On Linux: Check permissions with `ls -l /dev/video0`

### Gestures not working
- Ensure good lighting
- Keep hand 0.5-1.5m from camera
- Make deliberate, clear gestures
- Check that VLC window has keyboard focus

### Low FPS
- Close other applications
- Reduce camera resolution in code
- On Jetson: Ensure power mode is MAXN

### Keys not working in VLC
- Click on VLC window to give it focus
- Check VLC keyboard shortcuts in Preferences
- On Windows: Run as administrator if needed

---

## Performance Tips

- Use moderate, even lighting
- Plain background works best
- Keep hand movements deliberate
- Wait for cooldown between gestures (0.8s)
- Ensure camera is stable (not moving)

---

## Next Steps

- Read `GESTURE_MAPPING.md` for detailed gesture definitions
- Adjust thresholds in `gesture_media_control.py` if needed
- Record demo video for project deliverable
- Test in different lighting conditions
- Measure and document performance metrics
