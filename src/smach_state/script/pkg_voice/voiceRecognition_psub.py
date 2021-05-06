#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
import rospy
from std_msgs.msg import String


class voiceRecognition():
    def __init__(self):
        self.pub = rospy.Publisher('voiceWakeup', String, queue_size=1)
        self.rate = rospy.Rate(10)  # 1 Hz
        self.name = ''
        self.favoriteDrink = ''
        self.isUnderstand = False
        self.voice_msg = None

    def voice_recognition_pub(self):
        rospy.sleep(
            1
        )  # There must be a sleep between rospy.Publisher() and pub.publish().
        self.pub.publish('wake up')  # wake up the voice recognition system
        self.rate.sleep()
        print 'Listening...'

    def voice_recognition_sub(self):
        while self.voice_msg is None:
            try:
                self.voice_msg = rospy.wait_for_message('voiceWords',
                                                        String,
                                                        timeout=20)
                print("%s" % self.voice_msg.data)
            except:
                print 'Get voice_msg timeout!'
                self.pub.publish('wake up')
                pass

        if self.voice_msg.data.find('name') > -1:
            self.isUnderstand = True
            words = str(self.voice_msg.data)
            temp = words.split('is ', 2)[1]
            self.name = temp.split('.', 2)[0]
            print self.name
        elif self.voice_msg.data.find('drink') > -1:
            self.isUnderstand = True
            words = str(self.voice_msg.data)
            temp = words.split('is ', 2)[1]
            self.favoriteDrink = temp.split('.', 2)[0]
            print self.favoriteDrink
        else:
            self.isUnderstand = False
        # self.sub1 = rospy.Subscriber('voiceWords', String,
        #                              self.judgeCallback)  #监听识别结果的消息传入回调函数
        # rospy.spin() # keep listening
        # rospy.sleep(11)  # only listen for 11 s, because speak time is 10 s
        print "Recognition end..."

    # def voice_recognition_cancel_sub(self):
    #     self.sub.unregister()

    # def judgeCallback(self, msg):
    #     print msg.data
    #     if msg.data.find('name') > -1:
    #         self.isUnderstand = True
    #         words = str(msg.data)
    #         self.name = words.split('is ', 2)[1]
    #     elif msg.data.find('drink') > -1:
    #         self.isUnderstand = True
    #         words = str(msg.data)
    #         self.favoriteDrink = words.split('is ', 2)[1]
    #     else:
    #         self.isUnderstand = False


if __name__ == '__main__':
    rospy.init_node('voiceRecognitionpsub', anonymous=False)
    vrp = voiceRecognition()
    vrp.voice_recognition_pub()
    vrp.voice_recognition_sub()
    print vrp.isUnderstand
    # vrp.voice_recognition_cancel_sub()
