# Complete Jetson Nano Hardware Setup Guide

## ⚠️ IMPORTANT: Does This Run Offline?

**YES! This code runs 100% OFFLINE once setup is complete.**

- ✅ No internet needed during operation
- ✅ All processing happens locally on Jetson Nano
- ✅ MediaPipe models are stored locally
- ✅ Camera feed is processed in real-time on device
- ⚠️ Internet only needed for initial setup (downloading packages)

After setup, you can disconnect from internet and it will work perfectly!

---

## What You Need (Hardware Checklist)

### Required Items:
- [ ] **NVIDIA Jetson Nano Developer Kit** (4GB model recommended)
- [ ] **MicroSD Card** (minimum 32GB, Class 10 or UHS-1, 64GB+ recommended)
- [ ] **5V 4A Power Supply** with barrel jack (2.1mm x 5.5mm) OR USB-C power
- [ ] **USB Webcam** (any standard USB webcam, 720p or higher recommended)
- [ ] **Monitor** with HDMI or DisplayPort input
- [ ] **HDMI or DisplayPort cable**
- [ ] **USB Keyboard**
- [ ] **USB Mouse**
- [ ] **Ethernet cable** OR **USB WiFi adapter** (for initial setup only)

### Optional but Helpful:
- [ ] **Cooling fan** (5V fan, highly recommended to prevent overheating)
- [ ] **Case** for Jetson Nano
- [ ] **USB hub** if you have multiple USB devices

---

## Part 1: Prepare the SD Card (Do This on Your Computer)

### Step 1.1: Download JetPack Image

1. **On your Windows/Mac/Linux computer**, go to:
   ```
   https://developer.nvidia.com/embedded/jetpack
   ```

2. **Download JetPack SD Card Image** (latest version, usually JetPack 4.6.x)
   - File will be named something like: `jetson-nano-jp461-sd-card-image.zip`
   - Size: ~6-7 GB (will take time to download)

3. **Extract the ZIP file**
   - You'll get a `.img` file (around 14-15 GB)

### Step 1.2: Flash the SD Card

**On Windows:**

1. **Download Balena Etcher:**
   ```
   https://www.balena.io/etcher/
   ```
   Install and open it.

2. **Insert your microSD card** into your computer
   - Use SD card adapter if needed
   - Make sure it's 32GB or larger

3. **Flash the image:**
   - Click **"Flash from file"** → Select the `.img` file you extracted
   - Click **"Select target"** → Choose your SD card (be careful to select the right drive!)
   - Click **"Flash!"**
   - Wait 10-20 minutes for flashing to complete
   - You'll see "Flash Complete!" when done

4. **Safely eject the SD card** from your computer

**On Linux/Mac:**
```bash
# Find your SD card device (e.g., /dev/sdb or /dev/disk2)
lsblk  # Linux
diskutil list  # Mac

# Flash the image (replace /dev/sdX with your SD card)
sudo dd if=jetson-nano-image.img of=/dev/sdX bs=4M status=progress
sync
```

---

## Part 2: Physical Assembly of Jetson Nano

### Step 2.1: Insert the SD Card

1. **Locate the SD card slot:**
   - It's on the **bottom/underside** of the Jetson Nano board
   - Look for a small slot labeled "microSD"

2. **Orient the SD card correctly:**
   - **Metal contacts facing UP** (toward the board)
   - **Label side facing DOWN** (toward the table)

3. **Insert the SD card:**
   - Gently push the card into the slot
   - Push until you hear/feel a small click
   - The card should be flush with the board (not sticking out much)

4. **To remove later:** Push the card in slightly, it will spring out

### Step 2.2: Attach Cooling Fan (Highly Recommended)

1. **Locate the 4-pin fan header:**
   - It's near the edge of the board, labeled "FAN" or "J15"

2. **Connect the fan:**
   - Align the 4-pin connector with the header
   - Push down gently until fully seated
   - Fan should start spinning when powered on

3. **Mount the fan:**
   - Use screws or adhesive to attach fan to heatsink
   - Ensure airflow direction is correct (blowing air onto heatsink)

### Step 2.3: Connect Peripherals

**Follow this order:**

1. **Connect HDMI cable:**
   - Plug HDMI cable into Jetson Nano HDMI port
   - Connect other end to your monitor
   - Turn on monitor

2. **Connect USB Keyboard:**
   - Plug into any USB port (there are 4 USB-A ports)

3. **Connect USB Mouse:**
   - Plug into another USB port

4. **Connect USB Webcam:**
   - Plug into a USB port
   - **Important:** Use a USB 3.0 port (blue inside) for better performance

5. **Connect Ethernet cable:**
   - Plug into the Ethernet port (RJ45)
   - Connect to your router/switch
   - (OR use USB WiFi adapter if you don't have Ethernet)

6. **DO NOT connect power yet!**

### Step 2.4: Set Power Mode (Important!)

**For 5V 4A Barrel Jack Power Supply:**

1. **Locate the jumper (J48):**
   - It's a small 2-pin connector near the barrel jack
   - Usually has a small plastic jumper cap

2. **Install the jumper:**
   - Place the jumper cap across both pins
   - This enables barrel jack power mode

**For USB-C Power (Micro-USB on older models):**
- No jumper needed
- Just use USB-C power (but limited to 2A, less powerful)

### Step 2.5: Connect Power (Final Step)

1. **Double-check all connections:**
   - SD card inserted
   - HDMI connected
   - Keyboard, mouse, webcam connected
   - Network cable connected
   - Jumper installed (if using barrel jack)

2. **Connect power supply:**
   - Plug barrel jack into Jetson Nano
   - Plug power adapter into wall outlet

3. **Jetson Nano will boot automatically:**
   - Green LED should light up
   - Fan should start spinning
   - Monitor should show NVIDIA logo

---

## Part 3: First Boot Setup (On Jetson Nano)

### Step 3.1: Initial Ubuntu Setup

When Jetson Nano boots for the first time, you'll see a setup wizard:

1. **Accept License Agreement:**
   - Read and click "I accept"

2. **Select Language:**
   - Choose your language (English recommended)

3. **Select Keyboard Layout:**
   - Choose your keyboard layout

4. **Select Timezone:**
   - Choose your timezone

5. **Create User Account:**
   - **Username:** Choose a username (e.g., `jetson` or your name)
   - **Password:** Create a strong password
   - **Confirm password**
   - Write these down! You'll need them to log in.

6. **Partition Selection:**
   - Choose "Use entire disk" (default)
   - Click Continue

7. **Network Configuration:**
   - If Ethernet is connected, it should auto-configure
   - If using WiFi, select your network and enter password

8. **Wait for setup to complete:**
   - This takes 5-10 minutes
   - System will reboot automatically

9. **Login:**
   - Enter the username and password you created
   - You'll see the Ubuntu desktop

---

## Part 4: Configure Jetson Nano

### Step 4.1: Open Terminal

- Click on the terminal icon in the top bar
- OR press `Ctrl+Alt+T`

### Step 4.2: Update System (Requires Internet)

```bash
# Update package lists
sudo apt update

# Upgrade installed packages (this takes 10-20 minutes)
sudo apt upgrade -y

# Reboot
sudo reboot
```

Wait for system to reboot and log back in.

### Step 4.3: Set Power Mode to Maximum Performance

```bash
# Check current power mode
sudo nvpmodel -q

# Set to maximum performance (5W or 10W mode)
sudo nvpmodel -m 0

# Enable all CPU cores
sudo jetson_clocks
```

### Step 4.4: Verify Camera is Detected

```bash
# List video devices
ls -l /dev/video*

# You should see /dev/video0 (or video1, video2, etc.)

# Test camera with simple capture
v4l2-ctl --list-devices
```

If you see your webcam listed, it's working!

---

## Part 5: Transfer Your Code to Jetson Nano

### Method 1: Using USB Drive (Offline Method)

**On your Windows computer:**

1. **Copy project folder to USB drive:**
   - Copy the entire `HCI` folder to USB drive
   - Safely eject USB drive

2. **On Jetson Nano:**
   - Insert USB drive
   - It should auto-mount (appear on desktop or in file manager)
   - Open file manager, navigate to USB drive
   - Copy the `HCI` folder to your home directory:
   ```bash
   cp -r /media/jetson/USB_DRIVE_NAME/HCI ~/HCI
   ```

### Method 2: Using Network Transfer (Requires Internet)

**Option A - Using SCP (from Windows):**

1. **Install WinSCP** on Windows:
   ```
   https://winscp.net/
   ```

2. **Connect to Jetson Nano:**
   - Host: Jetson Nano IP address (find with `ifconfig` on Jetson)
   - Username: Your Jetson username
   - Password: Your Jetson password

3. **Drag and drop** the `HCI` folder to Jetson Nano home directory

**Option B - Using Git (if you have GitHub):**

```bash
# On Jetson Nano
cd ~
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git HCI
```

### Method 3: Direct Download (if you uploaded to cloud)

```bash
# Example with Google Drive, Dropbox, etc.
# Upload your project as a ZIP file, get the link, then:
wget YOUR_DOWNLOAD_LINK -O project.zip
unzip project.zip
```

---

## Part 6: Install Dependencies on Jetson Nano

### Step 6.1: Navigate to Project Directory

```bash
cd ~/HCI
ls  # You should see: src/, README.md, requirements.txt, etc.
```

### Step 6.2: Install System Dependencies

```bash
# Install Python and OpenCV
sudo apt update
sudo apt install -y python3-pip python3-opencv

# Install VLC media player
sudo apt install -y vlc

# Install other useful tools
sudo apt install -y nano git
```

### Step 6.3: Install Python Packages

```bash
# Install from requirements.txt
pip3 install -r requirements.txt

# This will install:
# - opencv-python
# - mediapipe==0.10.9
# - numpy
# - pynput

# Wait 5-10 minutes for installation
```

### Step 6.4: Verify Installation

```bash
python3 test_setup.py
```

You should see all tests pass with ✓ marks.

---

## Part 7: Run the Gesture Control (OFFLINE!)

### Step 7.1: Disconnect from Internet (Optional)

```bash
# Disable WiFi
sudo nmcli radio wifi off

# OR unplug Ethernet cable

# The code will still work perfectly!
```

### Step 7.2: Open VLC

```bash
# Open VLC
vlc &

# Load a video file
# Go to Media → Open File
# OR drag and drop a video file into VLC
```

### Step 7.3: Run Gesture Control

```bash
cd ~/HCI/src
python3 gesture_media_control.py
```

You should see:
```
[INFO] Running on Linux
[INFO] Starting gesture media control...
[INFO] Make sure VLC (or media player) window has focus!
[INFO] Press 'q' in the video window to quit.
```

### Step 7.4: Test Gestures

- Position yourself in front of the webcam
- Click on VLC window to give it focus
- Perform gestures:
  - ✋ Open palm → Play/Pause
  - ✊ Fist → Stop
  - 👍 Thumbs up → Volume up
  - 👎 Thumbs down → Volume down
  - 👉 Point right → Next track
  - 👈 Point left → Previous track

### Step 7.5: Stop the Program

- Press `q` in the camera window
- OR press `Ctrl+C` in terminal

---

## Part 8: Performance Optimization

### Check Current Performance

```bash
# Check CPU usage
htop

# Check GPU usage
tegrastats

# Check temperature
cat /sys/devices/virtual/thermal/thermal_zone*/temp
```

### If Performance is Low:

```bash
# Ensure maximum performance mode
sudo nvpmodel -m 0
sudo jetson_clocks

# Close unnecessary applications
# Reduce camera resolution in code (already set to 640x480)

# Check if fan is working
# Temperature should be below 70°C
```

---

## Troubleshooting

### SD Card Not Detected
- Remove and reinsert SD card
- Ensure it's pushed in until it clicks
- Try a different SD card (some cards are incompatible)

### No Display on Monitor
- Check HDMI cable connection
- Try a different HDMI cable
- Ensure monitor is on correct input
- Wait 1-2 minutes for boot

### Jetson Won't Power On
- Check power supply is 5V 4A
- Verify jumper (J48) is installed for barrel jack
- Try different power outlet
- Check green LED - should be lit

### Camera Not Working
- Check `ls -l /dev/video*` - should show video0
- Try different USB port (use USB 3.0 - blue port)
- Test with: `cheese` (webcam app)
- Some cameras need extra drivers

### Overheating
- Ensure fan is connected and spinning
- Check temperature: `cat /sys/devices/virtual/thermal/thermal_zone0/temp`
- Should be below 70000 (70°C)
- Add heatsink if not present
-