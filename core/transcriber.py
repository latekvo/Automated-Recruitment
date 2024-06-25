import whisper

transcription_model = whisper.load_model("base.en")


def get_text(filename: str = "./static/test.mov"):
    return transcription_model.transcribe(filename)["text"]