#!/usr/bin/env python
from saya_speech_database.srv import *

import rospy
import aiml
import os
import sys


mybot = aiml.Kernel()
mybot.setBotPredicate("name", "SAYA")
mybot.setBotPredicate("master", "Navaneeth")
mybot.setBotPredicate("botmaster", "botmaster")
mybot.setBotPredicate("nationality", "INDIAN")
mybot.setBotPredicate("gender", "Female")
mybot.setBotPredicate("country", "INDIA")
mybot.setBotPredicate("city", "kochin")
mybot.setBotPredicate("state", "Kerala")
mybot.setBotPredicate("family", "Asimov Robotics")




def load_aiml(xml_file):

	
	data_path = '/home/navaneeth/project_saya/src/saya_communication/saya_speech_database/data'
	#print data_path
	os.chdir(data_path)


	if os.path.isfile("standard.brn"):
		mybot.bootstrap(brainFile = "standard.brn")

	else:
		mybot.bootstrap(learnFiles = xml_file, commands = "load aiml b")
		mybot.saveBrain("standard.brn")


        



def saya_speech_database(req):
	
	#Create a variable for calling the dialogflow api with the CLIENT_ACCESS_TOKEN provided

	input = req.query
	response = mybot.respond(input)
	rospy.loginfo("I heard:: %s",req.query)
	rospy.loginfo("I spoke:: %s",response)
	#Call the API with the query	
	

	#Extract the voice output
	voice=response
	
	answer =''
	related=''
	disamb=''
	key=0
		
	return voice,answer,related,disamb,key


def speech_database_server():

	rospy.init_node('speech_database_server')

	s = rospy.Service('speech_database_server', query, saya_speech_database)

	rospy.spin()


if __name__ == "__main__":
	load_aiml('startup.xml')
	speech_database_server()
