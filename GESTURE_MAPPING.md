# Gesture Set and Mapping Table

## Overview
This document defines the complete gesture set used in the touchless HCI media control system and their corresponding media control actions.

---

## Gesture Definitions

### 1. OPEN_PALM
**Description:** All five fingers extended (open hand)  
**Detection:** Thumb, index, middle, ring, and pinky fingers all in extended position  
**Media Action:** Play/Pause  
**Keyboard Shortcut:** `Space`  
**Use Case:** Toggle between playing and pausing media

---

### 2. FIST
**Description:** All fingers closed (closed hand)  
**Detection:** Thumb, index, middle, ring, and pinky fingers all in folded position  
**Media Action:** Stop  
**Keyboard Shortcut:** `S`  
**Use Case:** Stop media playback completely

---

### 3. THUMB_UP
**Description:** Thumb extended upward, other fingers closed  
**Detection:** 
- Thumb extended
- Index, middle, ring, pinky closed
- Thumb tip Y-coordinate significantly above wrist Y-coordinate (threshold: -0.05)  
**Media Action:** Volume Up  
**Keyboard Shortcut:** `Ctrl+Up`  
**Use Case:** Increase media volume

---

### 4. THUMB_DOWN
**Description:** Thumb extended downward, other fingers closed  
**Detection:** 
- Thumb extended
- Index, middle, ring, pinky closed
- Thumb tip Y-coordinate significantly below wrist Y-coordinate (threshold: +0.05)  
**Media Action:** Volume Down  
**Keyboard Shortcut:** `Ctrl+Down`  
**Use Case:** Decrease media volume

---

### 5. POINT_RIGHT
**Description:** Index finger pointing and moving to the right  
**Detection:** 
- Index finger extended
- Middle, ring, pinky closed
- Horizontal movement to the right detected (threshold: +0.08 in normalized coordinates)  
**Media Action:** Next Track  
**Keyboard Shortcut:** `N`  
**Use Case:** Skip to next media file in playlist

---

### 6. POINT_LEFT
**Description:** Index finger pointing and moving to the left  
**Detection:** 
- Index finger extended
- Middle, ring, pinky closed
- Horizontal movement to the left detected (threshold: -0.08 in normalized coordinates)  
**Media Action:** Previous Track  
**Keyboard Shortcut:** `P`  
**Use Case:** Go back to previous media file in playlist

---

## Gesture Recognition Parameters

### Hand Landmarks
- **Total landmarks:** 21 points per hand
- **Key landmarks used:**
  - Wrist (0)
  - Thumb: Tip (4), IP joint (3)
  - Index: Tip (8), PIP joint (6)
  - Middle: Tip (12), PIP joint (10)
  - Ring: Tip (16), PIP joint (14)
  - Pinky: Tip (20), PIP joint (18)

### Detection Thresholds
- **Finger extension:** Tip Y-coordinate < PIP Y-coordinate (for index, middle, ring, pinky)
- **Thumb extension:** X-coordinate comparison (direction depends on left/right hand)
- **Thumb up/down:** ±0.05 normalized Y-coordinate difference from wrist
- **Pointing motion:** ±0.08 normalized X-coordinate change between frames
- **Cooldown period:** 0.8 seconds between gesture triggers

### MediaPipe Configuration
- **Model complexity:** 0 (fastest, optimized for edge devices)
- **Max hands:** 1
- **Min detection confidence:** 0.5
- **Min tracking confidence:** 0.5

---

## Performance Targets

| Metric | Target | Notes |
|--------|--------|-------|
| Gesture Recognition Accuracy | >90% | In controlled lighting conditions |
| End-to-End Latency | <200ms | From gesture to action execution |
| Frame Rate | ≥15 FPS | Stable performance on Jetson Nano |
| Resolution | 640×480 | Balanced for performance and accuracy |

---

## VLC Media Player Keyboard Shortcuts

The system sends standard VLC keyboard shortcuts:

| Shortcut | VLC Action |
|----------|------------|
| Space | Play/Pause |
| S | Stop |
| Ctrl+Up | Volume Up |
| Ctrl+Down | Volume Down |
| N | Next |
| P | Previous |

**Note:** VLC window must have keyboard focus for shortcuts to work.

---

## Usage Recommendations

### Optimal Conditions
- **Lighting:** Moderate, even lighting; avoid backlighting
- **Distance:** 0.5-1.5 meters from camera
- **Background:** Plain, contrasting background preferred
- **Hand position:** Keep hand within camera frame, palm facing camera

### Gesture Tips
- Hold gestures steady for 0.5-1 second for reliable detection
- Make deliberate movements for pointing gestures
- Avoid rapid hand movements between gestures
- Ensure fingers are clearly separated for open palm gesture

### Troubleshooting
- If gestures not detected: Check lighting and hand visibility
- If wrong gestures detected: Adjust thresholds in `gesture_media_control.py`
- If actions not working: Ensure VLC window has keyboard focus
- If low FPS: Reduce camera resolution or close other applications
