# a class that will be given a youtube lin and slides as folder path

# based on this, the flow shall be as follows:
# 1. download the audio, title from youtube
# 2. extract the text from the audio
# 3. clean the text
# 4. extract the text from the images
# 5. clean the text
# 6. prepare the notes

from tools.audio.audio_extractor.whisper_extractor import WhisperAudioExtractor
from tools.text.slide_processor.extractors.img_handler import ImageHandler
from tools.video.downloader import YouTubeAudioExtractor