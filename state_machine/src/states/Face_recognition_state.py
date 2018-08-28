#!/usr/bin/env python
import rospy
import smach
import smach_ros

from smach import State
from face_rec.srv import *
from std_msgs.msg import String

class Face_recognition(smach.State):
	def __init__(self):
		#Initializing the state with outcomes and output data to be sent to the next state 
		smach.State.__init__(self, outcomes=['Detected', 'Not_Detected'],output_keys=['Face_recognition_out'])

	def execute(self, userdata):
		rospy.loginfo('Executing state FACE RECOGNITION')
		rospy.wait_for_service('face_server')
		try:
			#Creating an instance to connect with client
			face_recognition_client = rospy.ServiceProxy('face_server', service)

			#Calling the client
			person = face_recognition_client("name")
			
			#Checking the data from the face recognition server 
			if person.prediction == 'None':
				return 'Not_Detected'
			else:
				userdata.Face_recognition_out = person.prediction
				return 'Detected'
    		
		except rospy.ServiceException, e:
			print "Service call failed: %s"%e
	
	
	

		
				





