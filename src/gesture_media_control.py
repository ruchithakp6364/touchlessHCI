import cv2
import mediapipe as mp
import time
import platform
import os
from pynput.keyboard import Controller, Key

# Optional OLED display support (Jetson Nano only)
try:
    from oled_display import update_oled
    OLED_AVAILABLE = True
    print("[INFO] OLED display module loaded successfully")
except ImportError as e:
    OLED_AVAILABLE = False
    print(f"[INFO] OLED display not available: {e}")
    print("[INFO] Running without OLED display (normal for Windows/Mac)")
    
    # Dummy function when OLED is not available
    def update_oled(gesture="None", fps=0, latency=0):
        pass


# -------------- Cross-platform Media Control --------------

keyboard = Controller()

def send_volume_command(direction, increment_10_percent=True):
    """
    Send volume commands to VLC with proper OSD display.
    direction: 'up' or 'down'
    increment_10_percent: If True, sends multiple commands for ~10% change
    """
    try:
        if increment_10_percent:
            # Send multiple volume commands for larger increment
            # VLC's Ctrl+Up/Down changes volume by ~5%, so send 2 commands for ~10%
            for _ in range(2):
                if direction == 'up':
                    keyboard.press(Key.ctrl)
                    keyboard.press(Key.up)
                    keyboard.release(Key.up)
                    keyboard.release(Key.ctrl)
                elif direction == 'down':
                    keyboard.press(Key.ctrl)
                    keyboard.press(Key.down)
                    keyboard.release(Key.down)
                    keyboard.release(Key.ctrl)
                time.sleep(0.1)  # Small delay between commands
        else:
            # Single volume command
            if direction == 'up':
                send_key('ctrl+up')
            elif direction == 'down':
                send_key('ctrl+down')
                
    except Exception as exc:
        print(f"[WARN] Failed to send volume command: {exc}")


def send_key(key: str) -> None:
    """
    Send a keypress using pynput (cross-platform).
    Examples:
        'space', 'ctrl+up', 'ctrl+shift+up', 'n', 'p', 's'
    
    Works on Windows, Linux (Jetson Nano), and macOS.
    VLC window should have focus for media control.
    """
    try:
        key_lower = key.lower()
        
        # Handle modifier combinations
        if '+' in key_lower:
            parts = key_lower.split('+')
            
            # Handle Ctrl+Shift combinations (for VLC volume 10% increments)
            if len(parts) == 3 and parts[0] == 'ctrl' and parts[1] == 'shift':
                main_key = parts[2]
                
                # Press Ctrl+Shift
                keyboard.press(Key.ctrl)
                keyboard.press(Key.shift)
                
                # Press main key
                if main_key == 'up':
                    keyboard.press(Key.up)
                    keyboard.release(Key.up)
                elif main_key == 'down':
                    keyboard.press(Key.down)
                    keyboard.release(Key.down)
                else:
                    keyboard.press(main_key)
                    keyboard.release(main_key)
                
                # Release modifiers
                keyboard.release(Key.shift)
                keyboard.release(Key.ctrl)
                
            # Handle single modifier combinations
            elif len(parts) == 2:
                modifier = parts[0]
                main_key = parts[1]
                
                # Press modifier
                if modifier == 'ctrl':
                    keyboard.press(Key.ctrl)
                elif modifier == 'alt':
                    keyboard.press(Key.alt)
                elif modifier == 'shift':
                    keyboard.press(Key.shift)
                
                # Press main key
                if main_key == 'up':
                    keyboard.press(Key.up)
                    keyboard.release(Key.up)
                elif main_key == 'down':
                    keyboard.press(Key.down)
                    keyboard.release(Key.down)
                else:
                    keyboard.press(main_key)
                    keyboard.release(main_key)
                
                # Release modifier
                if modifier == 'ctrl':
                    keyboard.release(Key.ctrl)
                elif modifier == 'alt':
                    keyboard.release(Key.alt)
                elif modifier == 'shift':
                    keyboard.release(Key.shift)
        
        # Handle single keys
        elif key_lower == 'space':
            keyboard.press(Key.space)
            keyboard.release(Key.space)
        else:
            keyboard.press(key_lower)
            keyboard.release(key_lower)
            
    except Exception as exc:
        print(f"[WARN] Failed to send key {key}: {exc}")

def show_vlc_osd_message(message, duration=2000):
    """
    Display a message on VLC's On-Screen Display (OSD).
    Desktop notifications disabled - only console output.
    VLC's native volume OSD still works via keyboard shortcuts.
    """
    # Only log to console, no desktop notifications
    print(f"[VLC OSD] {message}")


def create_vlc_overlay_window(fps, latency_ms, gesture_count, avg_latency, gesture_name="None"):
    """
    VLC overlay window disabled - no-op function.
    Performance metrics still visible in camera window.
    """
    return False


def create_performance_overlay_file(fps, latency_ms, gesture_count, avg_latency):
    """
    Performance subtitle overlay disabled - no-op function.
    No subtitle file will be created.
    """
    return None


GESTURE_TO_KEY = {
    "OPEN_PALM": "space",       # Play/Pause
    "FIST": "s",                # Stop
    "PEACE_SIGN": "ctrl+up",    # Volume up (2 fingers - index + middle)
    "ONE_FINGER": "ctrl+down",  # Volume down (1 finger - index only)
    "POINT_RIGHT": "n",         # Next track
    "POINT_LEFT": "p",          # Previous track
}

TRIGGER_COOLDOWN = 0.8  # seconds between gesture-triggered actions


# -------------- MediaPipe Hands Init --------------

try:
    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils
    
    hands = mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=1,
        model_complexity=0,  # 0 = fastest, good for Jetson Nano
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
    )
except AttributeError:
    print("[ERROR] MediaPipe version incompatible. Please install: pip install mediapipe==0.10.9")
    exit(1)


# -------------- Gesture Classification Utilities --------------

TIP_IDS = [4, 8, 12, 16, 20]   # Thumb, Index, Middle, Ring, Pinky tips
PIP_IDS = [3, 6, 10, 14, 18]   # Thumb IP, others PIP joints


def get_finger_states(landmarks, handedness_label):
    """
    Return a list [thumb, index, middle, ring, pinky] where 1 = extended, 0 = folded.
    landmarks: list of 21 normalized landmarks with .x and .y.
    handedness_label: 'Left' or 'Right' from MediaPipe.
    """
    fingers = []

    # Thumb: check x coordinate depending on hand side
    if handedness_label == "Right":
        thumb_is_open = landmarks[TIP_IDS[0]].x < landmarks[PIP_IDS[0]].x
    else:  # Left hand
        thumb_is_open = landmarks[TIP_IDS[0]].x > landmarks[PIP_IDS[0]].x
    fingers.append(1 if thumb_is_open else 0)

    # Other four fingers: tip.y < pip.y means finger is up (image origin is top-left)
    for tip_id, pip_id in zip(TIP_IDS[1:], PIP_IDS[1:]):
        finger_is_open = landmarks[tip_id].y < landmarks[pip_id].y
        fingers.append(1 if finger_is_open else 0)

    return fingers


def classify_static_gesture(landmarks, handedness_label):
    """
    Classify gesture based on finger states and pointing direction.
    Returns: 'OPEN_PALM', 'FIST', 'PEACE_SIGN', 'ONE_FINGER', 'POINT_RIGHT', 'POINT_LEFT', or None.
    """
    fingers = get_finger_states(landmarks, handedness_label)
    thumb, index, middle, ring, pinky = fingers

    # Open palm: all fingers open
    if fingers == [1, 1, 1, 1, 1]:
        return "OPEN_PALM"

    # Fist: all fingers closed
    if fingers == [0, 0, 0, 0, 0]:
        return "FIST"

    # Peace sign: index and middle fingers up, others down (Volume Up)
    if index == 1 and middle == 1 and thumb == ring == pinky == 0:
        return "PEACE_SIGN"

    # One finger: only index finger up (Volume Down)
    if index == 1 and thumb == middle == ring == pinky == 0:
        # Make sure it's pointing up, not left/right
        index_tip = landmarks[TIP_IDS[1]]
        index_mcp = landmarks[5]
        wrist = landmarks[0]
        
        # Check if pointing more vertically than horizontally
        vertical_distance = abs(index_tip.y - wrist.y)
        horizontal_distance = abs(index_tip.x - index_mcp.x)
        
        if vertical_distance > horizontal_distance:
            return "ONE_FINGER"

    # Pointing with index: index open, others closed (for left/right navigation)
    if index == 1 and middle == ring == pinky == 0:
        # Determine pointing direction based on index finger direction
        index_tip = landmarks[TIP_IDS[1]]  # Index finger tip
        index_mcp = landmarks[5]  # Index finger MCP (base joint)
        wrist = landmarks[0]
        
        # Calculate pointing direction vector
        pointing_vector_x = index_tip.x - index_mcp.x
        
        # Use a threshold to determine clear left/right pointing
        if pointing_vector_x > 0.05:  # Pointing right
            return "POINT_RIGHT"
        elif pointing_vector_x < -0.05:  # Pointing left
            return "POINT_LEFT"

    return None


# -------------- Main Loop --------------

def main():
    print(f"[INFO] Running on {platform.system()}")
    print("[INFO] Starting gesture media control...")
    print("[INFO] Make sure VLC (or media player) window has focus!")
    print("[INFO] Press 'q' in the video window to quit.\n")
    print("[INFO] Gesture Controls:")
    print("  - Open Palm: Play/Pause")
    print("  - Fist: Stop")
    print("  - Peace Sign (2 fingers): Volume Up +10% (with VLC display)")
    print("  - One Finger (pointing up): Volume Down -10% (with VLC display)")
    print("  - Point Right: Next track")
    print("  - Point Left: Previous track\n")
    print("[INFO] Performance metrics shown in camera window.")
    print("  4. Console output with detailed metrics\n")
    
    cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
    cap.set(cv2.CAP_PROP_FPS, 30)

    if not cap.isOpened():
        print("[ERROR] Cannot open camera. Check if camera is connected.")
        return

    prev_time = time.time()
    last_trigger_time = 0.0
    
    # Performance tracking
    gesture_count = 0
    start_time = time.time()
    
    # Latency tracking
    gesture_detection_times = []
    action_execution_times = []
    fps_history = []
    
    # Performance targets
    TARGET_FPS = 15.0
    TARGET_LATENCY_MS = 200.0
    
    # OSD update timing
    last_osd_update = 0.0
    osd_update_interval = 1.0  # Update OSD every 1 second

    while True:
        frame_start_time = time.time()
        
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame from camera.")
            break

        # Mirror the frame for more natural interaction
        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Measure gesture detection time
        detection_start = time.time()
        results = hands.process(rgb)
        detection_time = (time.time() - detection_start) * 1000  # Convert to ms

        gesture_label_to_show = "None"
        latency_ms = 0.0

        if results.multi_hand_landmarks and results.multi_handedness:
            hand_landmarks = results.multi_hand_landmarks[0]
            handedness = results.multi_handedness[0].classification[0].label  # 'Left' or 'Right'

            # Draw landmarks
            mp_drawing.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
            )

            lm = hand_landmarks.landmark
            detected_gesture = classify_static_gesture(lm, handedness)

            now = time.time()
            time_since_last = now - last_trigger_time

            if detected_gesture and time_since_last >= TRIGGER_COOLDOWN:
                key = GESTURE_TO_KEY.get(detected_gesture)
                gesture_label_to_show = detected_gesture
                if key:
                    # Measure action execution time
                    action_start = time.time()
                    
                    # Handle volume gestures specially for 10% increments with VLC OSD
                    if detected_gesture == "PEACE_SIGN":
                        send_volume_command('up', increment_10_percent=True)
                    elif detected_gesture == "ONE_FINGER":
                        send_volume_command('down', increment_10_percent=True)
                    else:
                        send_key(key)
                    
                    action_time = (time.time() - action_start) * 1000  # Convert to ms
                    
                    # Calculate end-to-end latency
                    latency_ms = detection_time + action_time
                    
                    gesture_count += 1
                    print(f"[ACTION] {detected_gesture} -> key: {key} | Latency: {latency_ms:.1f}ms")
                    last_trigger_time = now
                    
                    # Store performance data
                    gesture_detection_times.append(detection_time)
                    action_execution_times.append(action_time)
                    
                    # Show performance info on VLC OSD
                    if gesture_detection_times:
                        avg_total_latency = (sum(gesture_detection_times) + sum(action_execution_times)) / len(gesture_detection_times)
                    else:
                        avg_total_latency = latency_ms
                    
                    # Calculate current average FPS
                    current_avg_fps = sum(fps_history) / len(fps_history) if fps_history else 15.0
                    fps_status = "GOOD" if current_avg_fps >= TARGET_FPS else "LOW"
                    latency_status = "GOOD" if latency_ms <= TARGET_LATENCY_MS else "HIGH"
                    
                    osd_message = f"Gesture: {detected_gesture} | Latency: {latency_ms:.1f}ms ({latency_status}) | FPS: {current_avg_fps:.1f} ({fps_status})"
                    show_vlc_osd_message(osd_message, 2000)
            elif detected_gesture:
                gesture_label_to_show = detected_gesture
                latency_ms = detection_time  # Just detection time when no action

        # FPS calculation
        curr_time = time.time()
        fps = 1.0 / (curr_time - prev_time) if curr_time != prev_time else 0.0
        prev_time = curr_time
        
        # Store FPS history (keep last 30 frames for average)
        fps_history.append(fps)
        if len(fps_history) > 30:
            fps_history.pop(0)
        
        avg_fps = sum(fps_history) / len(fps_history) if fps_history else fps

        # Update VLC OSD periodically with performance metrics
        current_time = time.time()
        if current_time - last_osd_update >= osd_update_interval:
            if gesture_detection_times:
                avg_total_latency = (sum(gesture_detection_times) + sum(action_execution_times)) / len(gesture_detection_times)
            else:
                avg_total_latency = 0
            
            last_osd_update = current_time


        # Display performance metrics
        cv2.putText(frame, f"Gesture: {gesture_label_to_show}", (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        cv2.putText(frame, f"FPS: {avg_fps:.1f}", (10, 60),
            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)

        if latency_ms > 0:
            cv2.putText(frame, f"Latency: {latency_ms:.1f}ms", (10, 90),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)

        update_oled(gesture_label_to_show, avg_fps, latency_ms)
        
        
        # Performance summary
        #cv2.putText(frame, f"Gestures: {gesture_count}", (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        cv2.imshow("Hand Gesture Media Control", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

    # Performance summary
    total_time = time.time() - start_time
    print(f"\n=== PERFORMANCE SUMMARY ===")
    print(f"Session duration: {total_time:.1f}s")
    print(f"Average FPS: {avg_fps:.1f}")
    if gesture_detection_times:
        avg_detection = sum(gesture_detection_times) / len(gesture_detection_times)
        avg_action = sum(action_execution_times) / len(action_execution_times)
        avg_total_latency = avg_detection + avg_action

        print(f"Average Latency: {avg_total_latency:.1f} ms")
    
    if gesture_detection_times:
        avg_detection = sum(gesture_detection_times) / len(gesture_detection_times)
        avg_action = sum(action_execution_times) / len(action_execution_times)
        avg_total_latency = avg_detection + avg_action
        
        print(f"Average detection time: {avg_detection:.1f}ms")
        print(f"Average action time: {avg_action:.1f}ms")
        print(f"Average end-to-end latency: {avg_total_latency:.1f}ms (Target: ≤{TARGET_LATENCY_MS}ms) {'✓' if avg_total_latency <= TARGET_LATENCY_MS else '⚠'}")
    
    cap.release()
    cv2.destroyAllWindows()
    hands.close()


if __name__ == "__main__":
    main()
