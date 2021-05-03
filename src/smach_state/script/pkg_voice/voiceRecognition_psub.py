#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
import rospy
from std_msgs.msg import String


class voiceRecognition():
    def __init__(self):
        rospy.init_node('voiceRecognitionpsub', anonymous=False)
        self.pub = rospy.Publisher('voiceWakeup', String, queue_size=1)
        self.rate = rospy.Rate(10)  # 1 Hz

    def voice_recognition_pub(self):
        rospy.sleep(
            1
        )  # There must be a sleep between rospy.Publisher() and pub.publish().
        self.pub.publish('wake up')  # wake up the voice recognition system
        self.rate.sleep()

    def voice_recognition_sub(self):
        self.sub1 = rospy.Subscriber('voiceWords', String,
                                     self.judgeCallback)  #监听识别结果的消息传入回调函数
        # rospy.spin() # keep listening
        rospy.sleep(11)  # only listen for 11 s, because speak time is 10 s
        print "end"

    def voice_recognition_cancel_sub(self):
        self.sub.unregister()

    def judgeCallback(self, msg):
        print msg.data
        if msg.data.find('name') > -1:
            self.isUnderstand = True
        elif msg.data.find('drink') > -1:
            self.isUnderstand = True
        else:
            self.isUnderstand = False


if __name__ == '__main__':
    vrp = voiceRecognition()
    vrp.voice_recognition_pub()
    vrp.voice_recognition_sub()
    print vrp.isUnderstand
    # vrp.voice_recognition_cancel_sub()
