#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import rospy
from face.srv import search


def face_search_client():
    rospy.wait_for_service('/face_search')  # 阻塞等待
    try:
        face_search = rospy.ServiceProxy('/face_search', search)
        resp = face_search()
        return resp.out
    except rospy.ServiceException as e:
        print("Searching for face service call failed: %s" % e)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print ''
    else:
        sys.exit(1)

    print("out = %s" % face_search_client())
