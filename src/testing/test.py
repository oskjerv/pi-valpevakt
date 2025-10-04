#from picamera2 import Picamera2, Preview
#import time
#picam2 = Picamera2()
#camera_config = picam2.create_preview_configuration()
#picam2.configure(camera_config)
#picam2.start_preview(Preview.QTGL)
#picam2.start()
#time.sleep(2)
#picam2.capture_file("test.jpg")

from picamera2 import Picamera2
import time

picam2 = Picamera2()

# Use a still or video configuration — preview not needed
camera_config = picam2.create_still_configuration()
picam2.configure(camera_config)

picam2.start()
time.sleep(2)  # Let camera warm up
picam2.capture_file("test.jpg")

picam2.stop()
