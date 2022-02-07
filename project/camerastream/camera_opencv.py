import cv2
import time
import numpy as np
import os

from .base_camera import BaseCamera

#global start_time

class camera(BaseCamera):
    video_source1 = 1 
    video_source2 = 2
    video_source3 = 3
    video_source4 = 4

    @staticmethod
    def set_video_source(sources):
        camera.video_source1 = sources[0]
        camera.video_source2 = sources[1]
        camera.video_source3 = sources[2]
        camera.video_source4 = sources[3]

    @staticmethod
    def frames():
        
        camera1 = cv2.VideoCapture(camera.video_source1)
        camera1.set(3, 1280)
        camera1.set(4, 720)

            
        camera2 = cv2.VideoCapture(camera.video_source2)
        camera2.set(3, 1280)
        camera2.set(4, 720)

            
        camera3 = cv2.VideoCapture(camera.video_source3)
        camera3.set(3, 1280)
        camera3.set(4, 720)

            
        camera4 = cv2.VideoCapture(camera.video_source4)
        camera4.set(3, 1280)
        camera4.set(4, 720)

        #start_time = time.time()
        #print(start_time)
        #print(time.ctime(start_time))

        if not (camera1.isOpened() or camera2.isOpened() or camera3.isOpened() or camera4.isOpened()):
            raise RuntimeError('Could not start camera.')

        while True:

            notdetected = cv2.imread("notdetect.jpg")
            
            ret1, img1 = camera1.read()
            if not camera1.isOpened():
                img1 = notdetected
                
            ret2, img2 = camera2.read()
            if not camera2.isOpened():
                img2 = notdetected
    
            ret3, img3 = camera3.read()
            if not camera3.isOpened():
                img3 = notdetected
                
            ret4, img4 = camera4.read()
            if not camera4.isOpened():
                img4 = notdetected
            
            
            imgh1 = np.hstack((img1, img2))
            imgh2 = np.hstack((img3, img4))
            imgv = np.vstack((imgh1, imgh2))
            

            # encode as a jpeg image and return it
            #yield cv2.imencode('.jpg', imgv)[1].tobytes()
            yield imgv

            '''
            if time.time() - start_time >= 5: #in seconds
                print(time.time() - start_time)
                local_time = time.ctime(start_time)
                img_name = ("/project/camerastream/cam1/cam1 {}.jpg".format(local_time))
                cv2.imwrite(img_name, img1)
                print("{} written!".format(img_name))
                start_time = time.time() #resets timer

            '''
