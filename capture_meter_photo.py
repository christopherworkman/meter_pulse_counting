import sys
import time
from datetime import datetime
from picamera2 import Picamera2
import cv2

# Check for "show" argument
show_image = "show" in sys.argv

# Initialize camera
picam2 = Picamera2()
picam2.preview_configuration.main.size = (1280, 720)
picam2.preview_configuration.main.format = "RGB888"
picam2.configure("preview")
picam2.start()
time.sleep(2)  # Warm up

# Capture image
frame = picam2.capture_array()

# Add timestamp overlay
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
cv2.putText(frame, timestamp, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
            1, (255, 255, 255), 2, cv2.LINE_AA)

# Optionally show image
if show_image:
    cv2.imshow("Gas Submeter Snapshot", frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Save image with timestamped filename
filename = datetime.now().strftime("gas_meter_%Y%m%d_%H%M%S.jpg")
cv2.imwrite(filename, frame)
print(f"Image saved as: {filename}")

picam2.stop()

