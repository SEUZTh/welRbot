#!/usr/bin/env python
# -*- coding:utf-8 -*-

import rospy, cv2, cv_bridge, ast
from sensor_msgs.msg import Image
from pkg_faceRecognition.face_detect_client1 import detectClient


class takePhoto:
    def __init__(self, guest_name):
        self.name = guest_name
        self.savePath = '/home/zth/welRobot_ws/src/smach_state/script/pkg_camera/guest_photo/' + self.name + '.jpg'
        self.bridge = cv_bridge.CvBridge()
        self.img = cv2.imread(
            '/home/zth/welRobot_ws/src/smach_state/script/pkg_camera/guest_photo/pyy.png'
        )

    def take_a_photo(self):
        # while self.img is None:
        #     try:
        #         self.img = rospy.wait_for_message('camera/rgb/image_raw',
        #                                           Image,
        #                                           timeout=10)
        #     except:
        #         print 'failed'
        #         pass
        print '************ Take a photo! ************'
        # Bridge and save the photo of the guest
        # self.image = self.bridge.imgmsg_to_cv2(self.img)
        self.image = self.img
        cv2.imshow("img", self.image)
        cv2.imwrite(self.savePath, self.image)
        print('%s\'s photo has been saved in %s.' % (self.name, self.savePath))
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def save_face(self, face_pos):
        x = face_pos[0]
        y = face_pos[0]
        w = face_pos[0]
        h = face_pos[0]
        print face_pos
        # img_draw_rectangle = cv2.rectangle(self.image, (x, y), (x + w, y + h),
        #                                    (0, 255, 0), 20)
        # cv2.imshow("img1", img_draw_rectangle)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        # cv2.imwrite(self.savePath, img_draw_rectangle)
        # print('%s\'s photo has been saved in %s.' % (self.name, self.savePath))

        img_face = self.image[x:x + w, y:y + h]
        cv2.imshow("img2", img_face)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        cv2.imwrite(self.savePath, img_face)
        print('%s\'s face photo has been saved in %s.' %
              (self.name, self.savePath))


def main():
    guest_name = 'xxxx'
    rospy.init_node('takePhoto')
    take_photo = takePhoto(guest_name)
    take_photo.take_a_photo()

    d = detectClient()
    d.face_detect_client(
        '/home/zth/welRobot_ws/src/smach_state/script/pkg_camera/guest_photo/pyy.png'
    )

    # face_pos = ast.literal_eval('[,,,,]')
    face_pos = list(d.face1)
    take_photo.save_face(face_pos)


if __name__ == '__main__':
    main()
