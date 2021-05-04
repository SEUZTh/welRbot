#!/usr/bin/env python
# -*- coding:utf-8 -*-

import rospy, cv2, cv_bridge
from sensor_msgs.msg import Image


class takePhoto:
    def __init__(self, guest_name):
        self.name = guest_name
        self.savePath = '/home/zth/welRobot_ws/src/smach_state/script/pkg_camera/guest_photo/' + self.name + '.jpg'
        self.bridge = cv_bridge.CvBridge()
        self.img = None

    def take_a_photo(self):
        while self.img is None:
            try:
                self.img = rospy.wait_for_message('camera/rgb/image_raw',
                                                  Image,
                                                  timeout=10)
            except:
                print 'failed'
                pass
        print '************ Take a photo! ************'
        # Bridge and save the photo of the guest
        self.image = self.bridge.imgmsg_to_cv2(self.img)
        # cv2.imshow("img", image)
        cv2.imwrite(self.savePath, self.image)
        print('%s\'s photo has been saved in %s.' % (self.name, self.savePath))


def main():
    guest_name = 'Mike'
    rospy.init_node('takePhoto')
    take_photo = takePhoto(guest_name)
    take_photo.take_a_photo()


if __name__ == '__main__':
    main()
