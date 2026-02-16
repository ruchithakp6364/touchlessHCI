"""
Quick setup verification script for gesture media control system.
Tests camera, MediaPipe, and keyboard control functionality.
"""

import sys

def test_imports():
    """Test if all required packages are installed."""
    print("Testing imports...")
    try:
        import cv2
        print("✓ OpenCV installed")
    except ImportError:
        print("✗ OpenCV not found. Run: pip install opencv-python")
        return False
    
    try:
        import mediapipe as mp
        print("✓ MediaPipe installed")
    except ImportError:
        print("✗ MediaPipe not found. Run: pip install mediapipe")
        return False
    
    try:
        import numpy as np
        print("✓ NumPy installed")
    except ImportError:
        print("✗ NumPy not found. Run: pip install numpy")
        return False
    
    try:
        from pynput.keyboard import Controller, Key
        print("✓ pynput installed")
    except ImportError:
        print("✗ pynput not found. Run: pip install pynput")
        return False
    
    return True

def test_camera():
    """Test if camera is accessible."""
    print("\nTesting camera...")
    try:
        import cv2
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("✗ Cannot open camera. Check if camera is connected.")
            return False
        
        ret, frame = cap.read()
        if not ret:
            print("✗ Cannot read from camera.")
            cap.release()
            return False
        
        print(f"✓ Camera working. Resolution: {frame.shape[1]}x{frame.shape[0]}")
        cap.release()
        return True
    except Exception as e:
        print(f"✗ Camera test failed: {e}")
        return False

def test_mediapipe():
    """Test MediaPipe Hands initialization."""
    print("\nTesting MediaPipe Hands...")
    try:
        import mediapipe as mp
        mp_hands = mp.solutions.hands
        hands = mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            model_complexity=0,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
        )
        hands.close()
        print("✓ MediaPipe Hands initialized successfully")
        return True
    except Exception as e:
        print(f"✗ MediaPipe test failed: {e}")
        return False

def test_keyboard():
    """Test keyboard control."""
    print("\nTesting keyboard control...")
    try:
        from pynput.keyboard import Controller
        keyboard = Controller()
        print("✓ Keyboard controller initialized")
        print("  (Note: Actual key presses not tested to avoid interference)")
        return True
    except Exception as e:
        print(f"✗ Keyboard test failed: {e}")
        return False

def main():
    print("=" * 60)
    print("Gesture Media Control - Setup Verification")
    print("=" * 60)
    
    results = []
    results.append(("Imports", test_imports()))
    results.append(("Camera", test_camera()))
    results.append(("MediaPipe", test_mediapipe()))
    results.append(("Keyboard", test_keyboard()))
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    all_passed = True
    for name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{name:20s} {status}")
        if not passed:
            all_passed = False
    
    print("=" * 60)
    
    if all_passed:
        print("\n✓ All tests passed! You're ready to run the gesture control.")
        print("\nNext steps:")
        print("1. Open VLC Media Player and load a media file")
        print("2. Run: python src/gesture_media_control.py")
        print("3. Make sure VLC window has focus")
        print("4. Use gestures in front of the camera")
        return 0
    else:
        print("\n✗ Some tests failed. Please fix the issues above.")
        print("\nTo install all dependencies, run:")
        print("  pip install -r requirements.txt")
        return 1

if __name__ == "__main__":
    sys.exit(main())
