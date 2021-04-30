#!/usr/bin/env python
# -*- coding:utf-8 -*-

import rospy
import smach
import smach_ros


# define state 1: navegate to the room where guests are.
class navigate2guests(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['outcome1'])

    def execute(self, userdata):
        rospy.loginfo('Executing state navigate2guests...')
        return 'outcome1'


# define state 2: face to a guest and take a photo of the guest
class face2aguest(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['outcome2'])

    def execute(self, userdata):
        rospy.loginfo('Executing state face2aguest...')
        return 'outcome2'


# define state 3: ask the guest and listen to him
class ask_guest(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['outcome3', 'outcome4'])

    def execute(self, userdata):
        rospy.loginfo('Executing state ask_guest...')
        isUnderstand = True  # 是否听懂
        if isUnderstand:
            isUnderstand = False
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
        smach.State.__init__(self,
                             outcomes=['outcome6', 'outcome6_1'],
                             input_keys=['sii_counter_in'],
                             output_keys=['sii_counter_out'])

    def execute(self, userdata):
        rospy.loginfo('Executing state save_img_info...')
        if userdata.sii_counter_in < 3:
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
        smach.State.__init__(self, outcomes=['outcome7'])

    def execute(self, userdata):
        rospy.loginfo('Executing state introduce_guest...')
        return 'outcome7'


# define state 8: guide the oldest to the sofa
class guide2sofa(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['outcome8'])

    def execute(self, userdata):
        rospy.loginfo('Executing state guide2sofa...')
        return 'outcome8'


def main():

    rospy.init_node('smach_state_machine')

    # Create the sub SMACH state machine
    sm_top = smach.StateMachine(outcomes=['outcomeZ'])

    # Open the container
    with sm_top:
        smach.StateMachine.add('NAVIGATE2GUESTS',
                               navigate2guests(),
                               transitions={'outcome1': 'RECOGNIZE_PEOPLE'})

        # Create the recognizePeople SMACH state machine
        sm_recognizePeople = smach.StateMachine(outcomes=['outcomeX'])
        sm_recognizePeople.userdata.counter_in = 1
        # Open the container
        with sm_recognizePeople:
            # Add states to the container
            smach.StateMachine.add('FACE_TO_A_GUEST',
                                   face2aguest(),
                                   transitions={'outcome2': 'ASK_THE_GUEST'})

            smach.StateMachine.add('ASK_THE_GUEST',
                                   ask_guest(),
                                   transitions={
                                       'outcome3': 'REPEAT_THE_ANSWER',
                                       'outcome4': 'ASK_AGAIN'
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
                                       'sii_counter_in': 'counter_in',
                                       'sii_counter_out': 'counter_in'
                                   })

        smach.StateMachine.add('RECOGNIZE_PEOPLE',
                               sm_recognizePeople,
                               transitions={'outcomeX': 'INTRODUCE_GUEST'})

        smach.StateMachine.add('INTRODUCE_GUEST',
                               introduce_guest(),
                               transitions={'outcome7': 'GUIDE_TO_SOFA'})

        smach.StateMachine.add('GUIDE_TO_SOFA',
                               guide2sofa(),
                               transitions={'outcome8': 'outcomeZ'})
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
