from picamera import PiCamera
from time import sleep

camera = PiCamera()
camera.rotation = 180
camera.start_preview()
# sleep(10)
for i in range(5):
    sleep(2)
    camera.capture('/home/pi/Documents/pi_camera_test/image' + str(int(i)) + '.png')
    # Single image save
    # camera.capture('/home/pi/Documents/pi_camera_test/testPi_image.png')
camera.stop_preview()