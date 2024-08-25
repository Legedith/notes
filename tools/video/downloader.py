import datetime
import os

from yt_dlp import YoutubeDL


class YouTubeAudioExtractor:
    def __init__(self, url) -> None:
        self.url = url
        self.audio_file = None
        self.download_folder = "downloads"

        # Ensure the download folder exists
        if not os.path.exists(self.download_folder):
            os.makedirs(self.download_folder)

    def get_timestamp(self) -> str:
        """Return the current timestamp in yyyymmddhhmm format."""
        now = datetime.datetime.now(datetime.timezone.utc)
        return now.strftime("%Y%m%d%H%M")

    def download_audio(self) -> str:
        """Download audio using yt-dlp and return the file path."""
        try:
            # Define the download options
            ydl_opts = {
                "format": "bestaudio/best",  # Get the best audio quality
                "outtmpl": os.path.join(
                    self.download_folder,
                    "%(title)s.%(ext)s",
                ),  # Save file in the specified folder
                "noplaylist": True,  # Download only the single video
            }
            # Use yt-dlp to download audio
            with YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(self.url, download=True)
                original_file = ydl.prepare_filename(info_dict)

                # Generate the new filename with timestamp
                timestamp = self.get_timestamp()
                file_extension = os.path.splitext(original_file)[1]
                new_filename = os.path.join(
                    self.download_folder,
                    f"{timestamp}{file_extension}",
                )

                # Rename the downloaded file
                os.rename(original_file, new_filename)

                self.audio_file = new_filename
                print(f"Downloaded audio file: {self.audio_file}")
                return self.audio_file
        except Exception as e:
            print(f"Error downloading audio: {e}")
            return None

    def extract_audio(self) -> str:
        """Return the file path."""
        return self.download_audio()


if __name__ == "__main__":
    import sys

    ARGS = 2
    if len(sys.argv) != ARGS:
        print("Usage: python youtube_audio_extractor.py <YouTube URL>")
        sys.exit(1)

    url = sys.argv[1]
    extractor = YouTubeAudioExtractor(url)
    audio_path = extractor.extract_audio()
    if audio_path:
        print(f"Audio file saved at: {audio_path}")
