
from nodeTranscriptionClientWebSocketBridge import NodeTranscriptionSocket
from whisper_live.client import TranscriptionClient


# Define a callback function to handle the transcription result
def on_electron_message(message):
  print("Received message from Electron:", message)

# Create a new server socket listening on port 9080
server = NodeTranscriptionSocket(port=9080, message_callback=on_electron_message)
server.start()

def on_transcription_result(result):
  print("Received transcription result:", result)
  # Send the result to all connected clients
  server.send_json(result)

client = TranscriptionClient(
  "gpu.centralus.cloudapp.azure.com",
  9090,
  lang="it",
  translate=False,
  model="small",                                      # also support hf_model => `Systran/faster-whisper-small`
  use_vad=True,
  save_output_recording=False,                        # Only used for microphone input, False by Default
  output_recording_filename="./output_recording.wav", # Only used for microphone input
  callback=on_transcription_result                    # Add the callback function here
)

client()