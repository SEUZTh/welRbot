#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import rospy
from face.srv import compare


def face_compare_client(srcPath, dstPath):
    rospy.wait_for_service('/face_compare')  # 阻塞等待
    try:
        face_compare = rospy.ServiceProxy('/face_compare', compare)
        resp = face_compare(srcPath, dstPath)
        return resp.confidence
    except rospy.ServiceException as e:
        print("Comparing face service call failed: %s" % e)


if __name__ == '__main__':
    if len(sys.argv) == 3:
        srcPath = str(sys.argv[1])
        dstPath = str(sys.argv[2])
    else:
        sys.exit(1)

    print("confidence = %s" % face_compare_client(srcPath, dstPath))
