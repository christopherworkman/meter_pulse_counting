from picamera2 import Picamera2
import cv2
import time

# Initialize the camera
picam2 = Picamera2()
picam2.preview_configuration.main.size = (640, 480)
picam2.preview_configuration.main.format = "RGB888"
picam2.configure("preview")

# Start the camera
picam2.start()
time.sleep(1)  # Give time for the camera to warm up

# Capture a frame
frame = picam2.capture_array()

# Show the frame using OpenCV
cv2.imshow("Captured Frame", frame)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Stop the camera
picam2.stop()

