"""
OLED Display Module for Jetson Nano 2GB
Hardware: SSD1306 128x64 OLED Display via I2C
I2C Address: 0x3C (default)
Pins: SDA (Pin 3), SCL (Pin 5)
"""

try:
    import board
    import busio
    import adafruit_ssd1306
    from PIL import Image, ImageDraw, ImageFont
    
    # Initialize I2C
    i2c = busio.I2C(board.SCL, board.SDA)
    
    WIDTH = 128
    HEIGHT = 64
    
    # Initialize OLED display (I2C address 0x3C)
    oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3C)
    
    # Clear display
    oled.fill(0)
    oled.show()
    
    # Create image buffer
    image = Image.new("1", (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(image)
    
    # Load default font
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 10)
    except:
        font = ImageFont.load_default()
    
    print("[OLED] Display initialized successfully")
    
except Exception as e:
    print(f"[OLED] Failed to initialize: {e}")
    print("[OLED] Make sure I2C is enabled and OLED is connected")
    raise


def update_oled(gesture="None", fps=0, latency=0):
    """
    Update OLED display with current gesture recognition metrics.
    
    Args:
        gesture: Current detected gesture name
        fps: Current frames per second
        latency: Current latency in milliseconds
    """
    try:
        # Clear the image buffer
        draw.rectangle((0, 0, WIDTH, HEIGHT), outline=0, fill=0)
        
        # Draw text with better formatting
        draw.text((0, 0), f"Gesture:", font=font, fill=255)
        draw.text((0, 12), f"{gesture}", font=font, fill=255)
        draw.text((0, 30), f"FPS: {fps:.1f}", font=font, fill=255)
        draw.text((0, 45), f"Latency: {latency:.1f}ms", font=font, fill=255)
        
        # Update OLED display
        oled.image(image)
        oled.show()
        
    except Exception as e:
        print(f"[OLED] Update failed: {e}")


def clear_oled():
    """Clear the OLED display."""
    try:
        oled.fill(0)
        oled.show()
    except Exception as e:
        print(f"[OLED] Clear failed: {e}")


def show_startup_message():
    """Display startup message on OLED."""
    try:
        draw.rectangle((0, 0, WIDTH, HEIGHT), outline=0, fill=0)
        draw.text((10, 20), "Gesture Control", font=font, fill=255)
        draw.text((20, 35), "Starting...", font=font, fill=255)
        oled.image(image)
        oled.show()
    except Exception as e:
        print(f"[OLED] Startup message failed: {e}")
