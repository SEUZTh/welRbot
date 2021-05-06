#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys, rospy, tf, actionlib
from geometry_msgs.msg import *
from tf.transformations import quaternion_from_euler


def init_location(x, y):
    pub = rospy.Publisher('initialpose',
                          PoseWithCovarianceStamped,
                          queue_size=1)
    p = PoseWithCovarianceStamped()
    p.header.frame_id = "map"
    p.pose.pose.position.x = x
    p.pose.pose.position.y = y
    p.pose.pose.position.z = 0
    p.pose.pose.orientation = Quaternion(*quaternion_from_euler(0, 0, 0))
    p.pose.covariance = \
    [ 0.1 , 0,    0, 0, 0, 0,
        0   , 0.1 , 0, 0, 0, 0,
        0   , 0   , 0, 0, 0, 0,
        0   , 0   , 0, 0, 0, 0,
        0   , 0   , 0, 0, 0, 0,
        0   , 0   , 0, 0, 0, 0.1 ]
    for t in range(0, 5):
        rospy.sleep(1)
        pub.publish(p)

    rospy.loginfo("Init location is ( %d, %d )" %
                  (p.pose.pose.position.x, p.pose.pose.position.y))


if __name__ == '__main__':
    try:
        # the name of the node
        rospy.init_node('/init_location', anonymous=False)
        init_location(-2, -2)
    except:
        rospy.loginfo("Init_location node terminated.")