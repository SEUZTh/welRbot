#!/usr/bin/env python
# -*- coding:utf-8 -*-

import rospy
#导入最主要的Python for ROS库
from geometry_msgs.msg import Twist
from math import pi


class rotate():
    def __init__(self, goal_angle):
        # publish the message in the topic of '/cmd_vel' which control the speed of the robot
        self.cmd_vel = rospy.Publisher('/cmd_vel', Twist, queue_size=1)

        # set the update frequency to 50HZ
        rate = 50
        r = rospy.Rate(rate)
        # set parameters
        # angular speed: 1.0rad/s
        angular_speed = 1.0
        # Initialize the movement command
        move_cmd = Twist()
        move_cmd.linear.x = 0.0
        move_cmd.linear.y = 0.0
        move_cmd.linear.z = 0.0
        move_cmd.angular.x = 0.0
        move_cmd.angular.y = 0.0
        move_cmd.angular.z = angular_speed
        ticks = int(goal_angle * pi * rate)
        for i in range(ticks):
            self.cmd_vel.publish(move_cmd)
            r.sleep()
        # stop
        self.cmd_vel.publish(Twist())
        rospy.sleep(1)


if __name__ == '__main__':
    try:
        # the name of the node
        rospy.init_node('rotate', anonymous=False)
        rotate()
    except:
        rospy.loginfo("Rotate node terminated.")
