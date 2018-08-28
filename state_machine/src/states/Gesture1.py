import roslib
import rospy
import smach
import smach_ros
import os, sys
from std_msgs.msg import Bool


class gesture(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['Completed']) # Outcome
	
    def execute(self, userdata):
       	os.system("roslaunch eva_arm_controller Hi.launch") # launches the play back file
	return 'Completed'
	
