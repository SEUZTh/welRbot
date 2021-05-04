#!/usr/bin/env python
# -*- coding:utf-8 -*-

import rospy, cv2, cv_bridge
from sensor_msgs.msg import Image


class takePhoto:
    def __init__(self, guest_name):
        self.name = guest_name
        self.savePath = './welRobot_ws/src/smach_state/script/pkg_camera/guest_photo/' + self.name + '.jpg'
        self.bridge = cv_bridge.CvBridge()
        self.image_sub = rospy.Subscriber('camera/rgb/image_raw', Image,
                                          self.image_callback)
        rospy.sleep(
            0.1)  # two photos will be taken in 0.1 s without rospy.spin().

    def image_callback(self, msg):
        print '************ Take a photo! ************'
        # Bridge and save the photo of the guest
        image = self.bridge.imgmsg_to_cv2(msg)
        # cv2.imshow("img", image)
        cv2.imwrite(self.savePath, image)
        print('%s\'s photo has been saved in %s.' % (self.name, self.savePath))


def main():
    # if len(sys.argv) == 2:
    #     guest_name = str(sys.argv[1])
    # else:
    #     sys.exit(1)

    guest_name = 'Mike'
    print 'yes'
    rospy.init_node('takePhoto')
    take_photo = takePhoto(guest_name)

    # rospy.spin()


if __name__ == '__main__':
    main()
