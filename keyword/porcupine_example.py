import pvporcupine
import pyaudio
import os
from dotenv import load_dotenv

load_dotenv()
# Define the path to the Porcupine model file for the desired wake word
# porcupine_model_file = pvporcupine.porcupine.Porcupine.DEFAULT_MODEL_PATH

# Define the keyword (wake word) you want to detect
keyword = "porcupine"

# Initialize Porcupine with the desired keyword
porcupine = pvporcupine.create(
    keywords=[keyword],
    access_key=os.getenv("PORCUPINE_ACCESS_KEY"),
)

# Initialize PyAudio
pa = pyaudio.PyAudio()

# Define the audio stream parameters
audio_format = pyaudio.paInt16
channels = 1
rate = porcupine.sample_rate

# Open the audio stream
audio_stream = pa.open(
    rate=rate,
    channels=channels,
    format=audio_format,
    input=True,
    frames_per_buffer=porcupine.frame_length
)

print("Listening for the wake word '{}'...".format(keyword))

try:
    while True:
        # Read a single frame of audio data from the stream
        pcm = audio_stream.read(porcupine.frame_length, exception_on_overflow=False)

        # Pass the audio frame to Porcupine for wake word detection
        result = porcupine.process(pcm)

        # If the wake word is detected, print a message
        if result:
            print("Wake word '{}' detected!".format(keyword))

except KeyboardInterrupt:
    print("Stopping...")
finally:
    # Clean up
    audio_stream.close()
    pa.terminate()
    porcupine.delete()
