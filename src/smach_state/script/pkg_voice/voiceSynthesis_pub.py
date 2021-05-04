#!/usr/bin/env python
# -*- coding:utf-8 -*-

import rospy
from std_msgs.msg import String


# can change the sleep time in src/xfei_asr/src/tts_subscribe_speak.cpp to make it say two sentences in a row.
# If the sleep time is too short, the pronunciation of the two sentences will overlap.
def voiceSynthesis_pub(words):
    pub = rospy.Publisher("xfwords", String, queue_size=1)
    rospy.sleep(1)
    pub.publish(words)


if __name__ == '__main__':
    rospy.init_node("voiceSynthesis_pub", anonymous=False)
    try:
        voiceSynthesis_pub()
    except rospy.ROSInternalException:
        pass