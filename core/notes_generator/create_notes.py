# a class that will be given a youtube link and slides as folder path

# based on this, the flow shall be as follows:
# 1. download the audio, title from youtube
# 2. extract the text from the audio
# 3. clean the text
# 4. extract the text from the images
# 5. clean the text
# 6. prepare the notes
import os
from datetime import datetime

from tools.audio.audio_extractor.whisper_extractor import WhisperAudioExtractor
from tools.text.generator.notes_generator import NotesGenerator
from tools.text.slide_processor.extractors.img_handler import ImageHandler
from tools.text.text_formatter.computer_science_text_formatter import (
    ComputerScienceTextFormatter,
)
from tools.video.downloader import YouTubeAudioExtractor


class NotesCreator:
    def __init__(self, youtube_url, slides_folder_path, tesseract_cmd=None) -> None:
        self.youtube_url = youtube_url
        self.slides_folder_path = slides_folder_path
        self.tesseract_cmd = tesseract_cmd
        self.audio_extractor = YouTubeAudioExtractor(youtube_url)
        self.whisper_audio_extractor = WhisperAudioExtractor()
        self.image_handler = ImageHandler(slides_folder_path, tesseract_cmd)
        self.text_formatter = ComputerScienceTextFormatter()

    def generate_notes(self) -> str:
        # Extract audio from YouTube
        audio_path, video_title = self.audio_extractor.extract_audio()
        if not audio_path:
            return "Error extracting audio from YouTube"

        # Extract text from audio
        audio_text = self.whisper_audio_extractor.extract_text(audio_path)
        cleaned_audio_text = self.text_formatter.format_text(audio_text)

        # Extract text from images
        image_texts = self.image_handler.process_images()
        # image text will be a dictionary with slide_number as key and text as value
        cleaned_image_texts = {
            slide: self.text_formatter.format_text(text)
            for slide, text in image_texts.items()
        }

        title = video_title
        transcript = cleaned_audio_text
        slides = cleaned_image_texts
        notes_generator = NotesGenerator(title, transcript, slides)
        notes_content = notes_generator.generate_notes()

        # Save notes to a markdown file
        timestamp = datetime.now().strftime("%Y%m%d%H%M")
        filename = f"{title}_{timestamp}.md"
        folder_path = "ai_generated_notes"
        os.makedirs(folder_path, exist_ok=True)
        file_path = os.path.join(folder_path, filename)

        with open(file_path, "w", encoding="utf-8") as file:
            file.write(notes_content)

        return f"Notes saved to {file_path}"


# Usage
if __name__ == "__main__":
    youtube_url = "https://www.youtube.com/watch?v=video_id"
    slides_folder_path = "path/to/slides/folder"

    notes_creator = NotesCreator(youtube_url, slides_folder_path)
    notes = notes_creator.generate_notes()
    print(notes)
