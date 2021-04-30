#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import rospy
from face.srv import detect


class detectResponse:
    def __init__(self, faceNum, face1, face2, face3):
        self.faceNum = faceNum
        self.face1 = face1
        self.face2 = face2
        self.face3 = face3


def face_detect_client(imgPath):
    rospy.wait_for_service('/face_detect')  # 阻塞等待
    try:
        face_detect = rospy.ServiceProxy('/face_detect', detect)
        resp1 = face_detect(imgPath)
        detect_resp = detectResponse(resp1.faceNum, resp1.face1, resp1.face2,
                                     resp1.face3)
        return detect_resp
    except rospy.ServiceException as e:
        print("Detecting face service call failed: %s" % e)


if __name__ == '__main__':
    if len(sys.argv) == 2:
        imgPath = str(sys.argv[1])
        print("%s" % imgPath)
    else:
        sys.exit(1)

    detect_result = face_detect_client(imgPath)

    print("faceNum = %s, face1 = %s, face2 = %s, face3 = %s" %
          (detect_result.faceNum, detect_result.face1, detect_result.face2,
           detect_result.face3))
