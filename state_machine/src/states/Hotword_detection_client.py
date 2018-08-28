#!/usr/bin/env python
import rospy
import smach
import smach_ros
import os


from smach import State
from saya_hotword_detector.srv import *
from std_msgs.msg import String



class Hotword_detection(smach.State):
	def __init__(self):
        	smach.State.__init__(self, outcomes=['Detected','Not_Detected']) # Outcome

	def execute(self, userdata):
		rospy.loginfo('Executing state Hotword detection')
		rospy.wait_for_service('hotword_detector')
		try:
			#Creating an instance to connect with client
			hotword_detector_client = rospy.ServiceProxy('hotword_detector', hotword)

			#Calling the client
			response = hotword_detector_client(0)
			
			#Checking the data from the face recognition server 
			if response.detected == True:
				#play the audio file in mpg321 player
				os.system('mpg321 /home/asimov/IRA_V2_ws/src/saya_text_speech/sound_clips/hotword_detected.mp3 &')
				return 'Detected'
			else:
				return 'Not_Detected'
    		
		except rospy.ServiceException, e:
			print "Service call failed: %s"%e
