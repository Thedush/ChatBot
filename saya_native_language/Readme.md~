Steps:

1. Launch rosmaster in the NUC.

2. Connect the ethernet cable from NUC to PC.
Configure the ip address incase if its's not connecting.
Login in to raspberry pi.
sudo ssh pi@raspberrypi
Passwrd:raspberry

Launch the next 2 command in the raspberrypi through ssh:
---------------------------------------------------------
3.  rosrun saya_speech_recognition speech_server.py 
This launches the google speech API and then takes the input through MIC array.
Note:
The mic array should be selected as the primary input in the raspberry pi sound settings.

5.  rosrun saya_hotword_detector hotword_server.py 
This launches the hotword detection module.

Note:
These two codes are available in the catkin_ws in the raspberry pi
------------------------------------------------------------------------------------
6. rosrun saya_speech_database saya_dialogflow_database_server.py 
This launches the dialogflow api database.

7. rosrun saya_text_speech saya_text_speech_server.py 
This launches th google TTS server

8. rosrun saya_states ira_speech_service_architecture.py
This is a state machine package which has an example flow 
speech_recognition --> DialogFlow APi   --> Text to speech.


