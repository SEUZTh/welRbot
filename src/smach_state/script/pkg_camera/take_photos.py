#!/usr/bin/env python
# -*- coding:utf-8 -*-

import rospy, cv2, cv_bridge
from sensor_msgs.msg import Image


class takePhoto:
    def __init__(self, guest_name):
        self.name = guest_name
        self.bridge = cv_bridge.CvBridge()
        self.image_sub = rospy.Subscriber('camera/rgb/image_raw', Image,
                                          self.image_callback)

    def image_callback(self, msg):
        print 'Yes'
        # Bridge and save the photo of the guest
        image = self.bridge.imgmsg_to_cv2(msg)
        cv2.imshow("img", image)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        cv2.imwrite(
            '/home/zth/welRobot_ws/src/smach_state/script/pkg_camera/guest_photo/'
            + self.name + '.jpg', image)
        print('%s\'s photo has been saved.' % self.name)


if __name__ == '__main__':
    # if len(sys.argv) == 2:
    #     guest_name = str(sys.argv[1])
    # else:
    #     sys.exit(1)

    guest_name = 'Mike'
    rospy.init_node('takePhoto')
    take_photo = takePhoto(guest_name)

    rospy.spin()
