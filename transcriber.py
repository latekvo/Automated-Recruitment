import whisper

transcription_model = whisper.load_model("base.en")

def get_text(filename):
  return transcription_model.transcribe('./static/test.mov')["text"]
