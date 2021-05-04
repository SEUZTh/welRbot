#!/usr/bin/env python
# -*- coding:utf-8 -*-

import rospy
import smach
import smach_ros

from pkg_faceRecognition.face_detect_client1 import detectClient
from pkg_faceRecognition.face_compare_client import face_compare_client
from pkg_move.rotate import rotate
from pkg_navigation.navigation_client import navigate2destination
from pkg_voice.voiceRecognition_psub import voiceRecognition
from pkg_voice.voiceSynthesis_pub import voiceSynthesis_pub
from pkg_camera.take_a_photo import takePhoto
from pkg_save_info.save_info import save_info
from pkg_introduce.introA2B import introA2B
from pkg_introduce.findOldest import findOldest


# define state 1: navegate to the room where guests are.
class navigate2guests(smach.State):
    def __init__(self):
        smach.State.__init__(self,
                             outcomes=['outcome1'],
                             input_keys=['guestPos_in'])

    def execute(self, userdata):
        rospy.loginfo('Executing state navigate2guests...')
        # rotate to gather particles
        rospy.loginfo('Rotate 2 circles...')
        rotate(6)  # 4 * pi

        # To find guests and be faced to them
        rospy.loginfo('To find guests...')
        # n2g = navigate2destination()
        # n2g.navigation_client(userdata.guestPos_in)

        # Take a photo of them
        rospy.loginfo('Take a photo of them...')
        # tp = takePhoto('AllofThem')
        # tp.take_a_photo()

        # Request face detection service
        rospy.loginfo('Request face detection service...')
        # imgPath = '/home/zth/welRobot_ws/src/smach_state/script/pkg_camera/guest_photo/AllofThem.jpg'
        # dc = detectClient()
        # dc.face_detect_client(imgPath)
        # print("faceNum = %s,\nface1 = %s,\nface2 = %s,\nface3 = %s\n" %
        #       (dc.faceNum, dc.face1, dc.face2, dc.face3))

        return 'outcome1'


# define state 2: face to a guest
class face2aguest(smach.State):
    def __init__(self):
        smach.State.__init__(
            self,
            outcomes=['outcome2'],
            input_keys=['eachGuestPos_in', 'guest_counter_in'])

    def execute(self, userdata):
        rospy.loginfo('Executing state face2aguest...')

        # be faced to one of them
        print("be faced to %s" % userdata.guest_counter_in)
        # n2g = navigate2destination()
        # n2g.navigation_client(
        #     userdata.eachGuestPos_in[userdata.guest_counter_in])

        return 'outcome2'


# define state 3: ask the guest and listen to him
class ask_guest(smach.State):
    def __init__(self):
        smach.State.__init__(self,
                             outcomes=['outcome3', 'outcome4'],
                             input_keys=['ask_counter_in', 'guest_info_in'],
                             output_keys=['guest_info_out'])

    def execute(self, userdata):
        rospy.loginfo('Executing state ask_guest...')
        # ask name
        # words_1 = "Hi, what's your name please?"
        # voiceSynthesis_pub(words_1)
        # listen to a guest
        # rospy.loginfo('Listening to name...')
        # vrp = voiceRecognition()
        # vrp.voice_recognition_pub()
        # vrp.voice_recognition_sub()
        name = 'ZTh'
        # ask favorite drink
        words_2 = "What's your favorite drink?"
        # voiceSynthesis_pub(words_2)
        # listen to a guest
        rospy.loginfo('Listening to favorite drink...')
        # vrp = voiceRecognition()
        # vrp.voice_recognition_pub()
        # vrp.voice_recognition_sub()
        favoriteDrink = 'cola'
        if True:
            temp = userdata.guest_info_in
            userdata.guest_info_out = userdata.guest_info_in
            if userdata.ask_counter_in == 0:
                temp['name0'] = 'A'
                temp['drink0'] = 'A1'
            elif userdata.ask_counter_in == 1:
                temp['name1'] = 'B'
                temp['drink1'] = 'B1'
            elif userdata.ask_counter_in == 2:
                temp['name2'] = 'C'
                temp['drink2'] = 'C1'
            else:
                print "Error in asking!"
            print temp
            userdata.guest_info_out = temp
            return 'outcome3'
        else:
            return 'outcome4'


# define state 4: repeat the answer
class repeat_answer(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['outcome5'])

    def execute(self, userdata):
        rospy.loginfo('Executing state repeat_answer...')
        return 'outcome5'


# define state 5: save the image and information of the guest
class save_img_info(smach.State):
    def __init__(self):
        smach.State.__init__(
            self,
            outcomes=['outcome6', 'outcome6_1'],
            input_keys=['sii_counter_in', 'sii_guest_info_in'],
            output_keys=['sii_counter_out', 'sii_guest_info_out'])

    def execute(self, userdata):
        rospy.loginfo('Executing state save_img_info...')
        temp = userdata.sii_guest_info_in

        if userdata.sii_counter_in == 0:
            # take photo
            tp = takePhoto(userdata.sii_guest_info_in['name0'])
            tp.take_a_photo()
            # detect age
            dc = detectClient()
            dc.face_detect_client(
                '/home/zth/welRobot_ws/src/face/face_data/face1.jpg')

            temp['age0'] = str(dc.face1).split(', ')[4].split(')')[0]
            userdata.sii_guest_info_out = temp
            # save info
            save_info(temp['name0'], temp['age0'], temp['drink0'],
                      temp['pos0'])
        elif userdata.sii_counter_in == 1:
            # take photo
            tp = takePhoto(userdata.sii_guest_info_in['name1'])
            tp.take_a_photo()
            # detect age
            dc = detectClient()
            dc.face_detect_client(
                '/home/zth/welRobot_ws/src/face/face_data/face1.jpg')
            temp['age1'] = str(dc.face1).split(', ')[4].split(')')[0]
            userdata.sii_guest_info_out = temp
            # save info
            save_info(userdata.sii_guest_info_in['name1'],
                      userdata.sii_guest_info_in['age1'],
                      userdata.sii_guest_info_in['drink1'],
                      userdata.sii_guest_info_in['pos1'])
        elif userdata.sii_counter_in == 2:
            # take photo
            tp = takePhoto(userdata.sii_guest_info_in['name2'])
            tp.take_a_photo()
            # detect age
            dc = detectClient()
            dc.face_detect_client(
                '/home/zth/welRobot_ws/src/face/face_data/face1.jpg')
            temp['age2'] = str(dc.face1).split(', ')[4].split(')')[0]
            userdata.sii_guest_info_out = temp
            # save info
            save_info(userdata.sii_guest_info_in['name2'],
                      userdata.sii_guest_info_in['age2'],
                      userdata.sii_guest_info_in['drink2'],
                      userdata.sii_guest_info_in['pos2'])
        else:
            print 'Error in saving image and info.'

        if userdata.sii_counter_in < 2:  # 3 times
            userdata.sii_counter_out = userdata.sii_counter_in + 1
            return 'outcome6_1'
        else:
            return 'outcome6'


# define state 6: re-ask
class reask(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['outcome4'])

    def execute(self, userdata):
        rospy.loginfo('Executing state reask...')
        return 'outcome4'


# define state 7: introduce guests to each other
class introduce_guest(smach.State):
    def __init__(self):
        smach.State.__init__(self,
                             outcomes=['outcome7'],
                             input_keys=['introInfo_in', 'introPos_in'])

    def execute(self, userdata):
        rospy.loginfo('Executing state introduce_guest...')
        temp = userdata.introInfo_in
        name = [temp['name0'], temp['name1'], temp['name2']]
        age = [temp['age0'], temp['age0'], temp['age0']]
        drink = [temp['drink0'], temp['drink1'], temp['drink2']]
        pos = userdata.introPos_in
        # find the oldest one
        oldest = findOldest('10', '20', '30')
        print("The oldest one is %s" % name[oldest])
        # introduce each other
        for i in range(3):
            if i != oldest:
                n2g = navigate2destination()
                n2g.navigation_client(pos[i])
                intro = introA2B(name[i])
                for j in range(3):
                    if j != i:
                        intro.intro_A2B(name[j], drink[j])

        n2g = navigate2destination()
        n2g.navigation_client(pos[oldest])
        intro = introA2B(name[i])
        for i in range(3):
            if i != oldest:
                intro.intro_A2B(name[i], drink[i])

        return 'outcome7'


# define state 8: guide the oldest to the sofa
class guide2sofa(smach.State):
    def __init__(self):
        smach.State.__init__(self,
                             outcomes=['outcome8'],
                             input_keys=['sofaPos_in'])

    def execute(self, userdata):
        rospy.loginfo('Executing state guide2sofa...')
        # To find guests
        n2g = navigate2destination()
        n2g.navigation_client(userdata.sofaPos_in)

        return 'outcome8'


def main():
    # Params init
    # The position pf guests and faced to them.
    guestsPosition = [(1.077, -3.008, 0.0), (0.0, 0.0, -0.124, 0.992)]
    # The position pf each guest and faced to one of them.
    eachGuestPosition = [[(1.077, -2.569, 0.0), (0.0, 0.0, 0.201, 0.979)],
                         [(1.323, -2.942, 0.0), (0.0, 0.0, -0.100, 0.994)],
                         [(1.191, -3.665, 0.0), (0.0, 0.0, -0.077, 0.996)]]
    # The position of sofa
    sofaPosition = [(4.020, -4.656, 0.0), (0.0, 0.0, 0.908, 0.418)]
    # Guests' information
    guestInformation = {
        'name0': '',
        'name1': '',
        'name2': '',
        'age0': -1,
        'age1': -1,
        'age2': -1,
        'drink0': '',
        'drink1': '',
        'drink2': '',
        'pos0': [(1.077, -2.569, 0.0), (0.0, 0.0, 0.201, 0.979)],
        'pos1': [(1.323, -2.942, 0.0), (0.0, 0.0, -0.100, 0.994)],
        'pos2': [(1.191, -3.665, 0.0), (0.0, 0.0, -0.077, 0.996)]
    }

    rospy.init_node('smach_state_machine')

    # Create the sub SMACH state machine
    sm_top = smach.StateMachine(outcomes=['outcomeZ'])
    sm_top.userdata.guestPos = guestsPosition
    sm_top.userdata.each_guestPos2 = eachGuestPosition
    sm_top.userdata.each_guestInfo = guestInformation
    sm_top.userdata.sofaPos = sofaPosition
    # Open the container
    with sm_top:
        smach.StateMachine.add('NAVIGATE2GUESTS',
                               navigate2guests(),
                               transitions={'outcome1': 'RECOGNIZE_PEOPLE'},
                               remapping={'guestPos_in': 'guestPos'})

        # Create the recognizePeople SMACH state machine
        sm_recognizePeople = smach.StateMachine(outcomes=['outcomeX'])
        sm_recognizePeople.userdata.counter_in = 0
        sm_recognizePeople.userdata.each_guestPos = eachGuestPosition
        sm_recognizePeople.userdata.guestInfo = guestInformation

        # Open the container
        with sm_recognizePeople:
            # Add states to the container
            smach.StateMachine.add('FACE_TO_A_GUEST',
                                   face2aguest(),
                                   transitions={'outcome2': 'ASK_THE_GUEST'},
                                   remapping={
                                       'eachGuestPos_in': 'each_guestPos',
                                       'guest_counter_in': 'counter_in'
                                   })

            smach.StateMachine.add('ASK_THE_GUEST',
                                   ask_guest(),
                                   transitions={
                                       'outcome3': 'REPEAT_THE_ANSWER',
                                       'outcome4': 'ASK_AGAIN'
                                   },
                                   remapping={
                                       'ask_counter_in': 'counter_in',
                                       'guest_info_in': 'guestInfo',
                                       'guest_info_out': 'guestInfo'
                                   })

            smach.StateMachine.add('ASK_AGAIN',
                                   reask(),
                                   transitions={'outcome4': 'ASK_THE_GUEST'})

            smach.StateMachine.add('REPEAT_THE_ANSWER',
                                   repeat_answer(),
                                   transitions={'outcome5': 'SAVE_IMG_INFO'})
            smach.StateMachine.add('SAVE_IMG_INFO',
                                   save_img_info(),
                                   transitions={
                                       'outcome6': 'outcomeX',
                                       'outcome6_1': 'FACE_TO_A_GUEST'
                                   },
                                   remapping={
                                       'sii_guest_info_in': 'guestInfo',
                                       'sii_counter_in': 'counter_in',
                                       'sii_counter_out': 'counter_in'
                                   })

        smach.StateMachine.add('RECOGNIZE_PEOPLE',
                               sm_recognizePeople,
                               transitions={'outcomeX': 'INTRODUCE_GUEST'})

        smach.StateMachine.add('INTRODUCE_GUEST',
                               introduce_guest(),
                               transitions={'outcome7': 'GUIDE_TO_SOFA'},
                               remapping={
                                   'introInfo_in': 'each_guestInfo',
                                   'introPos_in': 'each_guestPos2'
                               })

        smach.StateMachine.add('GUIDE_TO_SOFA',
                               guide2sofa(),
                               transitions={'outcome8': 'outcomeZ'},
                               remapping={'sofaPos_in': 'sofaPos'})
    # Create and start the introspection server
    sis = smach_ros.IntrospectionServer('smach_state_machine', sm_top,
                                        '/SM_ROOT')
    sis.start()

    # Execute SMACH plan
    outcome = sm_top.execute()

    # Wait for ctrl-c to stop the application
    rospy.spin()
    sis.stop()


if __name__ == '__main__':
    main()
