
import roslib
import rospy
import smach
import smach_ros
import os, sys
from std_msgs.msg import Bool

import time

class speech(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['Completed']) # Outcome
	
    def execute(self, userdata):
	time.sleep(2)
       	os.system("mpg321 /home/asimov/IRA_V2_ws/src/saya_states/sound_snippets/future_event_audio_files/hello.mp3") # launches the play back file
	#time.sleep(3)
	return 'Completed'
