import RPi.GPIO as GPIO
import time
import threading
from datetime import datetime
from picamera2 import Picamera2
import cv2
import os

# === CONFIG ===
PULSE_GPIO_PIN = 17  # change this to your actual GPIO pin number
IMAGE_DIR = "/home/cworkman/gas_meter_images"
LOG_FILE = "/home/cworkman/gas_meter_log.csv"

# === Setup ===
os.makedirs(IMAGE_DIR, exist_ok=True)

picam2 = Picamera2()
picam2.preview_configuration.main.size = (1280, 720)
picam2.preview_configuration.main.format = "RGB888"
picam2.configure("preview")
picam2.start()
time.sleep(2)  # Camera warm-up

pulse_count = 0
last_hourly_capture = 0

# === Functions ===

def take_photo(label):
    global pulse_count
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{IMAGE_DIR}/gas_meter_{label}_{timestamp}.jpg"
    frame = picam2.capture_array()
    cv2.putText(frame, f"{label} {timestamp}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1,
                (255, 255, 255), 2, cv2.LINE_AA)
    cv2.imwrite(filename, frame)
    print(f"[{label}] Photo saved: {filename}")
    log_entry = f"{timestamp},{label},{pulse_count},{filename}\n"
    with open(LOG_FILE, "a") as f:
        f.write(log_entry)

def pulse_callback(channel):
    global pulse_count
    pulse_count += 1
    take_photo("pulse")

def hourly_check():
    global last_hourly_capture
    while True:
        now = time.time()
        if now - last_hourly_capture >= 3600:
            take_photo("hourly")
            last_hourly_capture = now
        time.sleep(10)

# === Setup GPIO ===
GPIO.setmode(GPIO.BCM)
GPIO.setup(PULSE_GPIO_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(PULSE_GPIO_PIN, GPIO.FALLING, callback=pulse_callback, bouncetime=200)

# === Start hourly thread ===
threading.Thread(target=hourly_check, daemon=True).start()

print("Pulse logger running. Press Ctrl+C to exit.")
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Exiting...")
finally:
    GPIO.cleanup()
    picam2.stop()

