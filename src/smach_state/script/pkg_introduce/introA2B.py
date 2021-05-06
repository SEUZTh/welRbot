#!/usr/bin/env python
# -*- coding:utf-8 -*-

import rospy
from std_msgs.msg import String
from pkg_voice.voiceSynthesis_pub import voiceSynthesis_pub


class introA2B:
    def __init__(self, B_name):
        self.B_name = B_name
        words = "Hello, %s." % self.B_name
        voiceSynthesis_pub(words)

    def intro_A2B(self, name, drink):
        # words = "Hello, %s. %s likes %s best" % (self.B_name, name, drink)
        words = "%s likes %s best" % (name, drink)
        print words
        voiceSynthesis_pub(words)
        rospy.sleep(8)


if __name__ == '__main__':
    rospy.init_node("voiceSynthesis_pub", anonymous=False)
    intro = introA2B('B')
    intro.intro_A2B('A', 'cola')
