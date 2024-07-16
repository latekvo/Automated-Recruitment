import whisper

transcription_model = whisper.load_model("small.en")


def get_text(filename: str):
    return transcription_model.transcribe(filename)["text"]
