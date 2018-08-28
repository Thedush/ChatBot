#!/usr/bin/env python
from saya_text_speech.srv import *
import rospy
import os, sys
import time

#Google text to speech
from gtts import gTTS

#Extracting audio information
from mutagen.mp3 import MP3
from google.cloud import translate

translate_client = translate.Client()
def saya_text_speech(req):

	#Calling google text to speech
	try:
		#tts=gTTS(text=req.text, lang='en', slow=False)
		#ts.save("/home/navaneeth/project_saya/src/saya_communication/saya_text_speech/sound_clips/reply.mp3")
		req.text=translate_engtotam(req.text)
		import subprocess
		#req.text = u'{}'.format(req.text)
		#print reply
		#req.text=u"'{}'".format(req.text).encode('utf-8')
		python3_command = "/home/navaneeth/project_saya/src/saya_native_language/saya_native_text_speech/scripts/google_speech_python.py"  # launch your python2 script using bash
		py2output = subprocess.check_output(["python3", python3_command, '-t',req.text])
		print py2output
		print "completed"
		return 1
	except:
		print ("Google text to speech error")
		return 0


def translate_engtotam(text):
    global final_text,translate_client
       
    # The target language
    target = 'hi'

    # Translates text into english
    translation = translate_client.translate(
        text,
        target_language=target)

    print(u'Text: {}'.format(text))
    print(u'Translation: {}'.format(translation['translatedText']))
    final_text = u'{}'.format(translation['translatedText'])
    return final_text

def speech_text_speech_server():

	rospy.init_node('saya_native_text_speech_server')

	s = rospy.Service('saya_native_text_speech_server', text, saya_text_speech)

	rospy.spin()

if __name__ == "__main__":
	speech_text_speech_server()
