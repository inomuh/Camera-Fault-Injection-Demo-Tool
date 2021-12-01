#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Real-time Fault Injector For Camera FI Demo Tool #

import os
from os import listdir
from os.path import isfile, join
from class_fi_realtime_ui import RealtimeImageFault as fireal
import rospy
from sensor_msgs.msg import Image
import cv2
import numpy as np
from cv_bridge import CvBridge



class RealtimeFaultInjector(object):
    """
    TOF/RGB Camera Image (Realtime) Fault Library For Camera FI Demo Tool
    ----------------------------------------------------------------
    ### Variables:
        - robot_camera = Robot Camera info
        - publish_camera = Faulty Camera screen (optional)
        - camera_type = Camera Type info
        - fault_type: Choosing fault type
        - fault_rate: Fault rate (%)
        - fi_pub_rate: ROS Publisher rate (Hz) 
        - cv2_screen: CV2 screen check (True/False)

    ### TOF Image Faults (Under-development):
        - Salt&Pepper -> salt_pepper()
        - Gaussian -> gaussian()
        - Poisson -> poisson()

    ### RGB Image Faults:
        - Open -> open_fault()
        - Close -> close_fault()
        - Erosion -> erosion()
        - Dilation -> dilation()
        - Gradient -> gradient()
        - Motion-blur -> motion_blur()
        - Partialloss -> partialloss()

    ###### Created by AKE - 04.11.21
    """
 
    def __init__(self,robot_camera, publish_camera, camera_type, fault_type, fault_rate, fi_pub_rate, cv2_screen=False):
        
        
        self.bridge = CvBridge()
        self.kernel = self.fault_rate_calc(fault_rate)
        self.camera_type = camera_type
        self.robot_camera = robot_camera
        self.publish_camera = publish_camera
        self.fault_type = fault_type
        self.fault_rate = fault_rate
        self.cv2_screen = cv2_screen
        self.fi_pub_rate = fi_pub_rate
        
        
        rospy.init_node("camera_fault_injection_demo_tool_node",anonymous=True)
        # Robot kamera bilgisi arayüzden gelecek.
        rospy.Subscriber(robot_camera, Image, self.camera_callback)
        #rospy.Subscriber("right_rokos/color_camera/image_raw", Image, self.camera_callback)
        rospy.spin()
        
    def camera_callback(self, msg):

        if self.camera_type == "TOF":
            img = self.bridge.imgmsg_to_cv2(msg, '32FC1') #For color cam, use "bgr8"
            im_arr = np.asarray(img)
            
        elif self.camera_type == "RGB":
            img = self.bridge.imgmsg_to_cv2(msg, 'bgr8')

        fir = fireal(img, self.kernel, self.fault_type, self.fault_rate)
        
        if self.fault_type == "Gaussian":
            #img = fir.gaussian()
            print("This fault type will be added.")
        elif self.fault_type == "Poisson":
            #img = fir.poisson()
            print("This fault type will be added.")
        elif self.fault_type == "Salt&Pepper":
            #img = fir.saltpepper()
            print("This fault type will be added.")
        elif self.fault_type == "Open":
            img = fir.open_fault()
        elif self.fault_type == "Close":
            img = fir.close_fault()
        elif self.fault_type == "Dilation":
            img = fir.dilation()
        elif self.fault_type == "Erosion":
            img = fir.erosion()
        elif self.fault_type == "Gradient":
            img = fir.gradient()
        elif self.fault_type == "Moiton-blur":
            img = fir.motion_blur()
        elif self.fault_type == "Partialloss":
            img = fir.partialloss()
        else:
            pass    
        
        if self.cv2_screen == True:
            cv2.imshow("CV2 Screen",img)
            cv2.waitKey(1)
            print("test")
            ### cv2_screen değişkeni işaretliyse basılan hatayı cv2 ekranında gösterir.
            #os.system("gnome-terminal -x python cv2_show.py") 
            
        else:
            self.camera_fault_publisher(img, self.robot_camera, self.camera_type, self.fi_pub_rate)
        

    def camera_fault_publisher(self, msg, robot_camera, camera_type, rate):

        pub_camera = rospy.Publisher(robot_camera, Image, queue_size=10)
        #pub_camera = rospy.Publisher("right_rokos/color_camera/image_raw", Image, queue_size=10)
        if camera_type == "TOF":
            img = self.bridge.cv2_to_imgmsg(msg, '32FC1')
        elif camera_type == "RGB":
            img = self.bridge.cv2_to_imgmsg(msg, 'bgr8')

        pub_camera.publish(img)
        r = rospy.Rate(rate)
        r.sleep()

    def read_image_list(self, file_path):
        """
        Resim klasöründeki resimlerin isimlerini bir listeye kaydeder.
        """
        onlyfiles = [f for f in listdir(file_path) if isfile(join(file_path, f))]
        image_list = [i.split(".",1)[0] for i in onlyfiles]
        return image_list
    
    def fault_rate_calc(self, fr):

        fr = int(fr)
        kernel = np.ones((fr,fr),np.uint8)

        return kernel

#if __name__ == "__main__":
#    
#    cv2_screen = False
#    camera_type = "RGB"
#    robot_camera = "right_rokos/color_camera/image_raw"
#    publish_camera = "right_rokos/color_camera/image_raw_faulty"
#    fault_type = "Erosion"
#    fault_rate = 5
#    RealtimeFaultInjector(robot_camera, publish_camera, camera_type, fault_type, fault_rate, cv2_screen)