#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import rospy
from face.srv import detect


class detectClient():
    def __init__(self):
        self.faceNum = 0
        self.face1 = 0
        self.face2 = 0
        self.face3 = 0

    def face_detect_client(self, imgPath):
        rospy.wait_for_service('/face_detect')  # 阻塞等待
        try:
            face_detect = rospy.ServiceProxy('/face_detect', detect)
            resp1 = face_detect(imgPath)

            self.faceNum = resp1.faceNum
            self.face1 = resp1.face1
            self.face2 = resp1.face2
            self.face3 = resp1.face3

        except rospy.ServiceException as e:
            print("Detecting face service call failed: %s" % e)


if __name__ == '__main__':
    if len(sys.argv) == 2:
        imgPath = str(sys.argv[1])
        print("%s" % imgPath)
    else:
        sys.exit(1)
    rospy.init_node('faceDetectClient', anonymous=False)
    dc = detectClient()
    dc.face_detect_client(imgPath)
    print("faceNum = %s,\nface1 = %s,\nface2 = %s,\nface3 = %s\n" %
          (dc.faceNum, dc.face1, dc.face2, dc.face3))
    # print("%d" % int(str(dc.face1).split(', ')[4].split(')')[0])) # print age
