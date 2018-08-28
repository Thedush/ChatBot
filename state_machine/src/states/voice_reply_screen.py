import rospy
import smach
import os, sys
import time

import webbrowser
import demjson


class Text_reply(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['completed'],input_keys=['Text_in'],) # Outcome
	
    def execute(self, userdata):
	rospy.loginfo('Executing Text_screen state')
	f = open('/home/asimov16/IRA_V2_ws/src/saya_states/ui_screen/Saya_screen.html','w')

	#print (userdata.Text_in.answer)
	#print (userdata.Text_in.related)
	#print (userdata.Text_in.disamb)
	#print (userdata.Text_in.key)
	#print (userdata.Text_in.voice)
	
	#check whether the answer field is empty
	if userdata.Text_in.answer != "":
		f.write(userdata.Text_in.answer+'<br>')
		
	#check whether the text contains any disambiguous questions
	if len(userdata.Text_in.disamb):
		f.write('Disambiguous Questions:'+'<br>')
		for i in range(len(userdata.Text_in.disamb)):
			f.write(userdata.Text_in.disamb[i]+'<br>')

	#check whether the text contains any related questions
	if len(userdata.Text_in.related):
		f.write('Related Questions:'+'<br>')
		for i in range(len(userdata.Text_in.related)):
			f.write(userdata.Text_in.related[i]+'<br>')
				
	f.close()

	#open the file to show the options
	filename ='file:///home/asimov16/IRA_V2_ws/src/saya_states/ui_screen/Saya_screen.html'
	webbrowser.open_new_tab(filename)
		

	return 'completed'


