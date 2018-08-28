
import rospy
import smach
import smach_ros

from smach import State
from saya_speech_database.srv import *
from std_msgs.msg import String

class Speech_database(smach.State):
	def __init__(self):
        	smach.State.__init__(self, outcomes=['Completed','Not_Completed'],input_keys=['Database_in'],output_keys=['speech_database_out']) # Outcome

	def execute(self, userdata):
		rospy.loginfo('Pinging the speech database server')
		rospy.wait_for_service('speech_database_server')
		try:
			#Creating an instance to connect with client
			speech_database_client = rospy.ServiceProxy('speech_database_server', query)

			#Calling the client
			response = speech_database_client(userdata.Database_in)
			
			#Sending the detected text to the next state 'Text to speech'
			userdata.speech_database_out = response.voice
			print response.voice

			return 'Completed'
    		
		except rospy.ServiceException, e:
			print "Service call failed: %s"%e
			return 'Not_Completed'
