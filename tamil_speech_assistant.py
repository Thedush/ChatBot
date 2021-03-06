#!/usr/bin/env python

# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Google Cloud Speech API sample application using the streaming API.

NOTE: This module requires the additional dependency `pyaudio`. To install
using pip:

    pip install pyaudio

Example usage:
    python transcribe_streaming_mic.py
"""

# [START import_libraries]
from __future__ import division

import re
import sys
import subprocess

from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
import pyaudio
import wave
from six.moves import queue

from playsound import playsound
from google.cloud import translate
#Hotword detection
#import snowboydecoder

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

#Google text to speech
from gtts import gTTS

# [END import_libraries]

#Access token for dialogflow
CLIENT_ACCESS_TOKEN = '5b9bd2b9cc684e38bfe64b45aae2ecaf'
ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)

# Audio recording parameters
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms
translate_client = translate.Client()

class MicrophoneStream(object):
    """Opens a recording stream as a generator yielding the audio chunks."""
    def __init__(self, rate, chunk):
        self._rate = rate
        self._chunk = chunk

        # Create a thread-safe buffer of audio data
        self._buff = queue.Queue()
        self.closed = True

    def __enter__(self):
        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16,
            # The API currently only supports 1-channel (mono) audio
            # https://goo.gl/z757pE
            channels=1, rate=self._rate,
            input=True, frames_per_buffer=self._chunk,
            # Run the audio stream asynchronously to fill the buffer object.
            # This is necessary so that the input device's buffer doesn't
            # overflow while the calling thread makes network requests, etc.
            stream_callback=self._fill_buffer,
        )

        self.closed = False

        return self

    def __exit__(self, type, value, traceback):
        self._audio_stream.stop_stream()
        self._audio_stream.close()
        self.closed = True
        # Signal the generator to terminate so that the client's
        # streaming_recognize method will not block the process termination.
        self._buff.put(None)
        self._audio_interface.terminate()

    def _fill_buffer(self, in_data, frame_count, time_info, status_flags):
        """Continuously collect data from the audio stream, into the buffer."""
        self._buff.put(in_data)
        return None, pyaudio.paContinue

    def generator(self):
        while not self.closed:
            # Use a blocking get() to ensure there's at least one chunk of
            # data, and stop iteration if the chunk is None, indicating the
            # end of the audio stream.
            chunk = self._buff.get()
            if chunk is None:
                return
            data = [chunk]

            # Now consume whatever other data's still buffered.
            while True:
                try:
                    chunk = self._buff.get(block=False)
                    if chunk is None:
                        return
                    data.append(chunk)
                except queue.Empty:
                    break

            yield b''.join(data)
# [END audio_stream]


def listen_print_loop(responses):
    """Iterates through server responses and prints them.

    The responses passed is a generator that will block until a response
    is provided by the server.

    Each response may contain multiple results, and each result may contain
    multiple alternatives; for details, see https://goo.gl/tjCPAU.  Here we
    print only the transcription for the top alternative of the top result.

    In this case, responses are provided for interim results as well. If the
    response is an interim one, print a line feed at the end of it, to allow
    the next result to overwrite it, until the response is a final one. For the
    final one, print a newline to preserve the finalized transcription.
    """
    num_chars_printed = 0
    for response in responses:
        if not response.results:
            continue

        # The `results` list is consecutive. For streaming, we only care about
        # the first result being considered, since once it's `is_final`, it
        # moves on to considering the next utterance.
        result = response.results[0]
        if not result.alternatives:
            continue

        # Display the transcription of the top alternative.
        transcript = result.alternatives[0].transcript

        # Display interim results, but with a carriage return at the end of the
        # line, so subsequent lines will overwrite them.
        #
        # If the previous result was longer than this one, we need to print
        # some extra spaces to overwrite the previous result
        overwrite_chars = ' ' * (num_chars_printed - len(transcript))

        if not result.is_final:
            sys.stdout.write(transcript + overwrite_chars + '\r')
            sys.stdout.flush()

            num_chars_printed = len(transcript)

        else:
            final = transcript + overwrite_chars
            print final
            final=translate(final)
            dialog(final)

            # Exit recognition if any of the transcribed phrases could be
            # one of our keywords.
            if re.search(r'\b(exit|quit)\b', transcript, re.I):
                print('Exiting..')
                break
	    break

	   

            num_chars_printed = 0


def translate(text):
    global final_text,translate_client
       
    # The target language
    target = 'en'

    # Translates text into english
    translation = translate_client.translate(
        text,
        target_language=target)

    print(u'Text: {}'.format(text))
    print(u'Translation: {}'.format(translation['translatedText']))
    final_text = u'{}'.format(translation['translatedText'])
    return final_text

# def text_speech(reply):

# 	tts=gTTS(text=reply, lang='ta', slow=False)
	
# 	tts.save("reply.mp3")
	
# 	os.system('mpg321 reply.mp3 &')

# 	return



def simple_text_speech(reply):
	reply = u'{}'.format(reply)
	#print reply
	tamil=u"'{}'".format(reply).encode('utf-8')
	#print tamil.encode('ascii', 'ignore')
	import subprocess
	python3_command = "google_speech_python.py"  # launch your python2 script using bash
	py2output = subprocess.check_output(["python3", python3_command, '-t',tamil])
	print py2output
	print "completed"
	#os.system(tamil)
	#os.system("google_speech -l ta '{}'".format(reply))
	return
def translate_engtotam(text):
    global final_text,translate_client
       
    # The target language
    target = 'ta'

    # Translates text into english
    translation = translate_client.translate(
        text,
        target_language=target)

    print(u'Text: {}'.format(text))
    print(u'Translation: {}'.format(translation['translatedText']))
    final_text = u'{}'.format(translation['translatedText'])
    return final_text

def dialog(query):
	
	request = ai.text_request()

	request.query = query

	response = request.getresponse()
	result=json.loads(response.read().decode())
	
	#from pprint import pprint
	
	#pprint (result)

	reply=result['result']['fulfillment']['speech']

	#result1 = result['result']
	reply=translate_engtotam(reply)
	simple_text_speech(reply)

	#context = result1.get('contexts')	
	#print reply
	return (0)
	# value= context[0]
	
	# print value.get('name')
	
	# if context:
	# 	if value.get('name')=="withdrawcash-followup":
	# 		var = raw_input("Please enter the amount ")
	# 		var = int(var)
	# 		print "you entered", var
	# 		dialog(var)
	# 	if value.get('name')=="accountnumber" or value.get('name')=="loans-yes-followup":
	# 		var = raw_input("Please enter the account number ")
	# 		var = int(var)
	# 		print "you entered", var
	# 		dialog(var)
	# 	if value.get('name')=="moneytransfer-followup":
	# 		var = raw_input("Please enter the bank details ")
	# 		print "you entered", var
	# 		dialog(var)
		
			
def detected_callback():
	main()
	#try:
	#	print("keyword_detected")		
	#	main()
	#	
	#except:
	#	print("Exception throwed")
	#	
	#	
	#print("Response completed")
	


def hotword_detector():
	
	print("Tell the keyword to start conversation")
	
	detector = snowboydecoder.HotwordDetector("resources/saya.pmdl", sensitivity=0.4, audio_gain=1)

	detector.start(detected_callback)



def main():
    # See http://g.co/cloud/speech/docs/languages
    # for a list of supported languages.
    language_code = 'ta-IN'  # a BCP-47 language tag

    client = speech.SpeechClient()
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code=language_code,
	speech_contexts=[speech.types.SpeechContext(phrases=['saya'])])
    streaming_config = types.StreamingRecognitionConfig(
        config=config,
        interim_results=True,
	single_utterance=False)

    with MicrophoneStream(RATE, CHUNK) as stream:
        audio_generator = stream.generator()
        requests = (types.StreamingRecognizeRequest(audio_content=content)
                    for content in audio_generator)

        responses = client.streaming_recognize(streaming_config, requests)

        # Now, put the transcription responses to use.
        listen_print_loop(responses)



	



if __name__ == '__main__':
	#hotword_detector()
    main()
	
           		
