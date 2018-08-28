#!/usr/bin/env python
from saya_speech_database.srv import *
import rospy
import demjson  
import requests
import os

from std_msgs.msg import String

def saya_speech_database(req):
	
	#Lists to store the related and disambiguous questions from the API response
	related=[]
	disamb=[]
	key =0
	
	#Format for calling the API:Api address + query
	text = 'http://159.203.108.219:8080/SenseforthChatEngine/chat?source=alexa&apiuser=test&client=HDFCFAQDB&q='+req.query

	#Call the API using request library
	r=requests.post(text)
	
	#Convert the json reply from APi into python dictionary	
	response=r.json()
	
	#Decoding the values from the dictionary
	#Extracting the text from the dictonary to speak
	if ('voice' in response):
		voice=response['voice']
	else:
		voice=''

	#Check whether the answer key is in the dictionary
	if ('answer' in response):
		answer = response['answer']

	#Check whether the disamb key is in the dictionary and extract the questions(starts from 1) from it and append it to the list 'disamb'
	if ('disamb' in response):
		for i in range(len(response['disamb'])):
			l =str(i+1)
			question = "question " + l
			disamb.append(response['disamb'][i][question])

	#Check whether the related key is in the dictionary and extract the questions(starts from 1) from it and append it to the list 'related'
	if ('related' in response):
		for i in range(len(response['related'])):
			l =str(i+1)
			question = "question " + l
			related.append(response['related'][i][question])

	#Check whether the key is in the dictionary
	if ('key' in response):
		key = response['key']

		
	return voice,answer,related,disamb,key


def speech_database_server():

	rospy.init_node('speech_database_server')

	s = rospy.Service('speech_database_server', query, saya_speech_database)

	rospy.spin()


if __name__ == "__main__":
	speech_database_server()
