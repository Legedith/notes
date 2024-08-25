import os
import datetime
from yt_dlp import YoutubeDL

class YouTubeAudioExtractor:
    def __init__(self, url):
        self.url = url
        self.audio_file = None

    def get_timestamp(self):
        """Return the current timestamp in yyyymmddhhmm format."""
        now = datetime.datetime.now()
        return now.strftime("%Y%m%d%H%M")

    def download_audio(self):
        """Download audio using yt-dlp and return the file path."""
        try:
            # Define the download options
            ydl_opts = {
                'format': 'bestaudio/best',  # Get the best audio quality
                'outtmpl': '%(title)s.%(ext)s',  # Save file with the video title as name
                'noplaylist': True,  # Download only the single video
            }
            # Use yt-dlp to download audio
            with YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(self.url, download=True)
                original_file = ydl.prepare_filename(info_dict)
                
                # Generate the new filename with timestamp
                timestamp = self.get_timestamp()
                file_extension = os.path.splitext(original_file)[1]
                new_filename = f"{timestamp}{file_extension}"
                
                # Rename the downloaded file
                os.rename(original_file, new_filename)
                
                self.audio_file = new_filename
                print(f"Downloaded audio file: {self.audio_file}")
                return self.audio_file
        except Exception as e:
            print(f"Error downloading audio: {e}")
            return None

    def extract_audio(self):
        """Main method to download the audio and return the file path."""
        return self.download_audio()

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python youtube_audio_extractor.py <YouTube URL>")
        sys.exit(1)
    
    url = sys.argv[1]
    extractor = YouTubeAudioExtractor(url)
    audio_path = extractor.extract_audio()
    if audio_path:
        print(f"Audio file saved at: {audio_path}")
    else:
        print("Failed to download audio.")
