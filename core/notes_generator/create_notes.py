# a class that will be given a youtube link and slides as folder path

# based on this, the flow shall be as follows:
# 1. download the audio, title from youtube
# 2. extract the text from the audio
# 3. clean the text
# 4. extract the text from the images
# 5. clean the text
# 6. prepare the notes
import logging
import os
from datetime import datetime, timezone

from core.post_processing.fill_slides import SlideReplacer
from tools.audio.audio_extractor.whisper_extractor import WhisperAudioExtractor
from tools.text.generator.notes_generator import NotesGenerator
from tools.text.slide_processor.extractors.img_handler import ImageHandler
from tools.text.text_formatter.computer_science_text_formatter import (
    ComputerScienceTextFormatter,
)
from tools.video.downloader import YouTubeAudioExtractor

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class NotesCreator:
    def __init__(self, youtube_url, slides_folder_path, tesseract_cmd=None) -> None:
        logger.info(
            f"Initializing NotesCreator with YouTube URL: {youtube_url} and slides folder path: {slides_folder_path}",
        )
        self.youtube_url = youtube_url
        self.slides_folder_path = slides_folder_path
        self.tesseract_cmd = tesseract_cmd
        self.audio_extractor = YouTubeAudioExtractor(youtube_url)
        self.whisper_audio_extractor = WhisperAudioExtractor()
        self.image_handler = ImageHandler(slides_folder_path, tesseract_cmd)
        self.text_formatter = ComputerScienceTextFormatter()
        logger.info("NotesCreator initialized successfully")

    def generate_notes(self) -> str:
        logger.info("Starting note generation process")

        # Extract audio from YouTube
        logger.info("Extracting audio from YouTube")
        audio_path, video_title = self.audio_extractor.extract_audio()
        if not audio_path:
            logger.error("Error extracting audio from YouTube")
            return "Error extracting audio from YouTube"
        logger.info(f"Audio extracted successfully: {audio_path}")
        print(f"\nAudio Path: {audio_path}\nVideo Title: {video_title}\n")

        # Extract text from audio
        logger.info("Extracting text from audio")
        audio_text = self.whisper_audio_extractor.extract_text(audio_path)
        cleaned_audio_text = self.text_formatter.format_text(
            audio_text,
            domain=video_title,
        )
        logger.info("Text extracted and formatted from audio")
        print(f"\nAudio Text: {audio_text}\nCleaned Audio Text: {cleaned_audio_text}\n")

        # Extract text from images
        logger.info("Extracting text from images")
        image_texts = self.image_handler.process_images()
        cleaned_image_texts = {
            slide: self.text_formatter.format_text(text, domain=video_title)
            for slide, text in image_texts.items()
        }
        logger.info("Text extracted and formatted from images")
        print(
            f"\nImage Texts: {image_texts}\nCleaned Image Texts: {cleaned_image_texts}\n",
        )

        # Generate notes
        logger.info("Generating notes")
        title = video_title
        transcript = cleaned_audio_text
        slides = cleaned_image_texts
        notes_generator = NotesGenerator(title, transcript, slides)
        notes_content = notes_generator.generate_notes()
        logger.info("Notes generated successfully")
        print(f"\nNotes Content: {notes_content}\n")

        # Save notes to a markdown file
        return NotesCreator.save_notes_to_file(notes_content, self.slides_folder_path)

    @staticmethod
    def save_notes_to_file(notes_content, slides_folder_path) -> str:
        logger.info("Saving notes to a markdown file")

        # Determine the parent directory of the slides folder
        parent_dir = os.path.dirname(slides_folder_path)
        folder_path = os.path.join(parent_dir, "ai_generated_notes")

        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M")
        filename = f"note_{timestamp}.md"
        os.makedirs(folder_path, exist_ok=True)
        file_path = os.path.join(folder_path, filename)
        replaced_markdown = SlideReplacer.replace_slides(
            notes_content,
            slides_folder_path,
        )
        print(replaced_markdown)

        try:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(replaced_markdown)
            logger.info(f"Notes saved to {file_path}")
            print(f"\nNotes saved to: {file_path}\n")
            return f"{file_path}"
        except Exception as e:
            logger.error(f"Failed to save notes: {e}")
            return f"Failed to save notes: {e}"


# Usage
if __name__ == "__main__":
    youtube_url = "https://www.youtube.com/watch?v=y872bCqQ_P0"
    slides_folder_path = "test/agile/slides"
    notes_creator = NotesCreator(youtube_url, slides_folder_path)
    notes_creator.generate_notes()
