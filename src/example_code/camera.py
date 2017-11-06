from time import sleep
from picamera import PiCamera
from datetime import datetime


camera = PiCamera()
camera.resolution = (1024, 768)
# Camera warm-up time
sleep(2)
#get the time - use it for the naming the image
date_now = datetime.now() # dates in the format: 2017-10-20 13:16:03.46748345
date = '-'.join(str(date_now).split(' ')[0].split('-'))
time = ''.join(str(date_now).split(' ')[1].split(':')).split('.')[0]

photo_name = str('_'.join([date,time]))+'.jpg'
camera.capture(photo_name)
