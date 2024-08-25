import logging

import whisper

from tools.audio.audio_extractor.extractor import AudioExtractor

logger = logging.getLogger(__name__)


class WhisperAudioExtractor(AudioExtractor):
    def __init__(self, model_size="base") -> None:
        logger.info(f"Initializing Whisper model with size: {model_size}")
        self.model = whisper.load_model(model_size, device="cuda")
        logger.info("Whisper model initialized successfully")

    def extract_text(self, audio_file) -> str:
        logger.info(f"Starting transcription for audio file: {audio_file}")
        # Transcribe the audio
        result = self.model.transcribe(audio_file)
        logger.info(f"Transcription completed for audio file: {audio_file}")
        logger.debug(f"Transcription result: {result['text']}")

        # Return the recognized text
        return result["text"]


# sample usage
if __name__ == "__main__":
    whisper_audio_extractor = WhisperAudioExtractor()
    text = whisper_audio_extractor.extract_text(
        "downloads/202408251318.webm",
    )
    print(text)
