#!/usr/bin/env python
import rospy
import smach
import smach_ros

from smach import State
from saya_speech_recognition.srv import *
from std_msgs.msg import String

class Speech_recognition(smach.State):
	def __init__(self):
        	smach.State.__init__(self, outcomes=['Completed','Not_Completed'],output_keys=['speech_recognition_out']) # Outcome

	def execute(self, userdata):
		rospy.loginfo('Executing state speech recognition')
		rospy.wait_for_service('speech_recognizer')
		try:
			#Creating an instance to connect with client
			speech_recognizer_client = rospy.ServiceProxy('speech_recognizer', speech)

			#Calling the client
			response = speech_recognizer_client(1)
			
			#Sending the detected text to the next state 'Text to speech'
			userdata.speech_recognition_out = response.text

			return 'Completed'
    		
		except rospy.ServiceException, e:
			print "Service call failed: %s"%e
			return 'Not_Completed'
