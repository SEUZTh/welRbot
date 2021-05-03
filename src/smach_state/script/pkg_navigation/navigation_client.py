#!/usr/bin/env python

import sys
import rospy
import actionlib

from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal

waypoints = [[(1.522, 0.444, 0.0), (0.0, 0.0, -0.519, 0.85)],
             [(-2.0432, -0.439, 0.0), (0.0, 0.0, -0.559, 0.82902)]]


class navigate2destination():
    def __init__(self):

        self.goal_pose = MoveBaseGoal()
        self.goal_pose.target_pose.header.frame_id = 'map'
        self.navigationClient = actionlib.SimpleActionClient(
            'move_base', MoveBaseAction)

    def navigation_client(self, pose):
        self.goal_pose.target_pose.pose.position.x = pose[0][0]
        self.goal_pose.target_pose.pose.position.y = pose[0][1]
        self.goal_pose.target_pose.pose.position.z = pose[0][2]
        self.goal_pose.target_pose.pose.orientation.x = pose[1][0]
        self.goal_pose.target_pose.pose.orientation.y = pose[1][1]
        self.goal_pose.target_pose.pose.orientation.z = pose[1][2]
        self.goal_pose.target_pose.pose.orientation.w = pose[1][3]

        try:
            self.navigationClient.wait_for_server()
            self.navigationClient.send_goal(self.goal_pose)
            self.navigationClient.wait_for_result()
        except rospy.ServiceException as e:
            print("Navigation service call failed: %s" % e)


if __name__ == '__main__':

    destination = [(1.522, 0.444, 0.0), (0.0, 0.0, -0.519, 0.85)]

    # rospy.init_node('navigation')

    n2d = navigate2destination()
    n2d.navigation_client(destination)
