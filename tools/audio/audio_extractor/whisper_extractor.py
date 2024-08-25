import whisper

from tools.audio.audio_extractor.extractor import AudioExtractor


class WhisperAudioExtractor(AudioExtractor):
    def __init__(self, model_size="medium"):
        self.model = whisper.load_model(model_size)

    def extract_text(self, audio_file) -> str:
        # Transcribe the audio
        result = self.model.transcribe(audio_file)

        # Return the recognized text
        return result["text"]


# sample usage
if __name__ == "__main__":
    whisper_audio_extractor = WhisperAudioExtractor()
    text = whisper_audio_extractor.extract_text(
        "tools/audio/audio_extractor/samples/audio1.mp3"
    )
    print(text)
