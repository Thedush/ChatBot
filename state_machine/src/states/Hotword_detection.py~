import rospy
import smach
import os, sys

#Hotword detection
import snowboydecoder

import time

#Timer variable
t=0

#Global variable for hotword detection output
detected = False

class Hotword_detection(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['Detected','Not_Detected']) # Outcome
	
    def detected_callback(self):
	global detected
	rospy.loginfo('Detected')

	#Assign the detected variable true.
	#The reason for using global variable is that we cannot return the outcome of the state over here. So, this will interrupt the callback once the hotword is detected and then in the main function by checking this variable , the outcome of the state will be set. 
	detected = True

    def interrupt_callback(self):
	global t

	start_time = time.time()
	
	t=(time.time() - start_time)+t
	
        #Timeout for the detection(10secs) and check the detection status
	if t<.0001 and not detected:
		interrupted=False
		return interrupted
	else:
		interrupted=True
		return interrupted

    def execute(self, userdata):
	rospy.loginfo('Executing Hotword Detection')

	print("Tell the keyword to start conversation")
	
	detector = snowboydecoder.HotwordDetector("/home/asimov16/IRA_V2_ws/src/saya_states/src/states/resources/saya.pmdl", sensitivity=0.4, audio_gain=1)
	
	l=detector.start(detected_callback=self.detected_callback,
               interrupt_check=self.interrupt_callback,
               sleep_time=0.03)
	if detected:
		global detected
		detected =False
		return 'Detected'
	else:
		return 'Not_Detected'


