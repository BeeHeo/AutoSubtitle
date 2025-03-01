import os
import subprocess
import glob
import logging
import shutil
from pathlib import Path
from typing import Optional
import signal
import sys
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('subtitle_processor.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class SubtitleProcessor:
    def __init__(self, whisper_model: str = 'small', language: str = 'English'):
        self.whisper_model = whisper_model
        self.language = language
        self.output_format = 'srt'

    def _check_dependencies(self) -> bool:
        """Check if required tools (whisper and ffmpeg) are installed."""
        for cmd in ['whisper', 'ffmpeg']:
            if not shutil.which(cmd):
                logger.error(f"Required tool not found: {cmd}")
                return False
        return True

    def _generate_unique_filename(self, video_path: str, suffix: str = "_subtitled.mp4") -> str:
        """Generate a unique filename to avoid overwriting existing files."""
        base_path = os.path.splitext(video_path)[0]
        unique_suffix = f"{suffix}"
        counter = 1

        while True:
            new_filename = f"{base_path}{unique_suffix}"
            if not os.path.exists(new_filename):
                return new_filename
            unique_suffix = f"_subtitled_{counter}.mp4"
            counter += 1

    def generate_subtitles(self, video_path: str, output_folder: str) -> Optional[str]:
        """Generate subtitles using Whisper if they don't exist."""
        try:
            video_name = os.path.basename(video_path)
            subtitle_path = os.path.join(output_folder, video_name.replace(".mp4", ".srt"))

            if os.path.exists(subtitle_path) and os.path.getsize(subtitle_path) > 0:
                logger.info(f"Subtitles already exist for: {video_name}")
                return subtitle_path

            logger.info(f"Generating subtitles for: {video_name}")
            whisper_cmd = [
                'whisper', video_path,
                '--model', self.whisper_model,
                '--language', self.language,
                '--output_format', self.output_format,
                '--output_dir', output_folder
            ]

            result = subprocess.run(
                whisper_cmd,
                capture_output=True,
                text=True,
                timeout=600,  # 10-minute timeout
                check=True
            )
            logger.info(f"Successfully generated subtitles for: {video_name}")
            return subtitle_path

        except subprocess.CalledProcessError as e:
            logger.error(f"Error generating subtitles for {video_name}: {e.stderr}")
            return None
        except subprocess.TimeoutExpired as e:
            logger.error(f"Timeout generating subtitles for {video_name}: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error generating subtitles for {video_name}: {str(e)}")
            return None

    def embed_subtitles(self, video_path: str, subtitle_path: str) -> bool:
        """Embed subtitles into video using FFmpeg with unique output filenames."""
        try:
            video_name = os.path.basename(video_path)
            # Use a unique filename to avoid overwriting
            temp_output = self._generate_unique_filename(video_path, "_subtitled.mp4")
            subtitle_path_ffmpeg = subtitle_path.replace('\\', '\\\\').replace(':', '\\:')

            logger.info(f"Embedding subtitles into: {video_name}")
            ffmpeg_cmd = [
                'ffmpeg', '-i', video_path,
                '-vf', f"subtitles='{subtitle_path_ffmpeg}'",
                '-c:v', 'libx264',
                '-preset', 'ultrafast',
                '-crf', '23',
                '-c:a', 'copy',
                '-y',
                temp_output
            ]

            result = subprocess.run(
                ffmpeg_cmd,
                capture_output=True,
                text=True,
                timeout=300,  # 5-minute timeout
                check=True
            )

            # Replace original file only if it doesn't already exist as subtitled
            if os.path.exists(temp_output):
                original_base = os.path.splitext(video_path)[0]
                if not os.path.exists(f"{original_base}_subtitled.mp4") and not os.path.exists(
                        f"{original_base}_subtitled_1.mp4"):
                    os.remove(video_path)
                    os.rename(temp_output, video_path)
                    logger.info(f"Successfully embedded subtitles into: {video_name}")
                else:
                    logger.info(f"Keeping original and subtitled versions separate: {video_name}")
                return True
            else:
                logger.error(f"Temporary output file not created for: {video_name}")
                return False

        except subprocess.CalledProcessError as e:
            logger.error(f"FFmpeg error for {video_name}: {e.stderr}")
            return False
        except subprocess.TimeoutExpired as e:
            logger.error(f"Timeout embedding subtitles for {video_name}: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"Error embedding subtitles for {video_name}: {str(e)}")
            return False

    def process_videos(self, input_folder: str) -> dict:
        """Process all videos in the input folder."""
        if not self._check_dependencies():
            return {"success": 0, "failed": 0, "skipped": 0}

        subtitle_folder = os.path.join(input_folder, "subtitles")
        Path(subtitle_folder).mkdir(exist_ok=True)

        video_files = glob.glob(os.path.join(input_folder, "**", "*.mp4"), recursive=True)
        if not video_files:
            logger.warning("No MP4 files found in the specified directory!")
            return {"success": 0, "failed": 0, "skipped": 0}

        stats = {"success": 0, "failed": 0, "skipped": 0}
        total = len(video_files)

        def signal_handler(sig, frame):
            logger.warning("Process interrupted by user")
            sys.exit(0)

        signal.signal(signal.SIGINT, signal_handler)

        for i, video_path in enumerate(video_files, 1):
            logger.info(f"Processing video {i}/{total}: {os.path.basename(video_path)}")

            subtitle_path = self.generate_subtitles(video_path, subtitle_folder)
            if not subtitle_path:
                stats["failed"] += 1
                continue

            if os.path.exists(subtitle_path) and os.path.getsize(subtitle_path) > 0:
                if self.embed_subtitles(video_path, subtitle_path):
                    stats["success"] += 1
                else:
                    stats["failed"] += 1
            else:
                stats["skipped"] += 1
                logger.warning(f"No valid subtitles found for: {os.path.basename(video_path)}")

        logger.info(
            f"Processing complete - Success: {stats['success']}, Failed: {stats['failed']}, Skipped: {stats['skipped']}")
        return stats


def main():
    processor = SubtitleProcessor()
    folder_path = input("Enter the video folder path: ")

    if not os.path.exists(folder_path):
        logger.error("Invalid path provided!")
        return

    stats = processor.process_videos(folder_path)
    print(f"\nProcessing Summary:")
    print(f"Successfully processed: {stats['success']}")
    print(f"Failed: {stats['failed']}")
    print(f"Skipped: {stats['skipped']}")


if __name__ == "__main__":
    main()