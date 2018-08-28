
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-t", "--text",help="text for the google_speech",
                    action="store")
args = parser.parse_args()
print ()




from google_speech import Speech

# say "Hello World"
text = args.text
lang = "ta"
speech = Speech(text, lang)
#speech.play()

# you can also apply audio effects (using SoX)
# see http://sox.sourceforge.net/sox.html#EFFECTS for full effect documentation
sox_effects = ("speed", "1")
speech.play(sox_effects)