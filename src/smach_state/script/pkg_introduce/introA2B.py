#!/usr/bin/env python
# -*- coding:utf-8 -*-

import rospy
from std_msgs.msg import String


class introA2B:
    def __init__(self, B_name):
        self.B_name = B_name

    def intro_A2B(self, name, drink):
        words = "Hello, %s. %s likes %s best" % (self.B_name, name, drink)
        print words
        pub = rospy.Publisher("xfwords", String, queue_size=1)
        rospy.sleep(1)
        pub.publish(words)
        rospy.sleep(8)


if __name__ == '__main__':
    rospy.init_node("voiceSynthesis_pub", anonymous=False)
    intro = introA2B('B')
    intro.intro_A2B('A', 'cola')
