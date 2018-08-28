#!/usr/bin/env python
from saya_speech_database.srv import *
import rospy
import demjson  
import requests


from std_msgs.msg import String

#Dialogflow imports
import json
import os.path
import os
try:
    import apiai
except ImportError:
    sys.path.append(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
    )
    import apiai

#Access token for dialogflow bank_agent
#CLIENT_ACCESS_TOKEN = '14a19d48dff4489385c4d52264f82ef9'

#Access token for dialogflow KSUM_info agent
CLIENT_ACCESS_TOKEN = '5b9bd2b9cc684e38bfe64b45aae2ecaf'


dialogflow = apiai.ApiAI(CLIENT_ACCESS_TOKEN)



def saya_speech_database(req):
	
	#Create a variable for calling the dialogflow api with the CLIENT_ACCESS_TOKEN provided
	request = dialogflow.text_request()
	
	#Call the API with the query	
	request.query = req.query

	#Store the response
	response = request.getresponse()
	
	#Decode the json
        result=json.loads(response.read().decode())

	#Print the output results
	from pprint import pprint
	pprint (result)

	#Extract the voice output
	voice=result['result']['fulfillment']['speech']
	
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
	speech_database_server()
