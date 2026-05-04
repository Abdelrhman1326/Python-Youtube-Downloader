import subprocess
import yt_dlp
import sys
import os

RESOLUTIONS = {
    "360p": "bestvideo[height<=360]+bestaudio/best[height<=360]",
    "480p": "bestvideo[height<=480]+bestaudio/best[height<=480]",
    "720p": "bestvideo[height<=720]+bestaudio/best[height<=720]",
    "1080p": "bestvideo[height<=1080]+bestaudio/best[height<=1080]",
    "best": "bestvideo+bestaudio/best"
}

def convert_to_h264(input_file, output_directory=None):
    """
    Converts an existing video file to H.264 (AVC) codec using FFmpeg.
    """
    if not os.path.exists(input_file):
        return None

    file_name = os.path.basename(input_file)
    name_no_ext = os.path.splitext(file_name)[0]

    if output_directory is None:
        output_directory = os.path.dirname(input_file)

    output_file = os.path.join(output_directory, f"{name_no_ext}_h264.mp4")

    # FFmpeg command for maximum compatibility
    command = [
        'ffmpeg',
        '-i', input_file,
        '-c:v', 'libx264',
        '-crf', '23',
        '-preset', 'medium',
        '-c:a', 'aac',
        '-b:a', '192k',
        '-pix_fmt', 'yuv420p',
        '-y',
        output_file
    ]

    try:
        print(f"\n--- Starting H.264 Conversion: {file_name} ---")
        subprocess.run(command, check=True)
        print(f"Conversion Successful: {output_file}")
        return output_file
    except subprocess.CalledProcessError as e:
        print(f"Error during conversion: {e}")
        return None
    except FileNotFoundError:
        print("Error: FFmpeg not found. Ensure it's installed and in your PATH.")
        return None


def format_size(bytes_val):
    if bytes_val is None or bytes_val == 0: return "Unknown size"
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_val < 1024:
            return f"{bytes_val:.2f} {unit}"
        bytes_val /= 1024
    return f"{bytes_val:.2f} TB"


def update_ytdlp():
    print("Checking for yt-dlp updates...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "yt-dlp"])
    except Exception as e:
        print(f"Update skipped: {e}")


def get_base_opts():
    return {
        "socket_timeout": 20,
        "retries": 10,
        "nocheckcertificate": True,
        "ignoreerrors": True,
        "log_tostderr": False,
        "quiet": True,
        "no_warnings": True,
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    }


def get_info_and_confirm(url, opts, is_playlist=False):
    extract_opts = opts.copy()
    extract_opts['extract_flat'] = True
    with yt_dlp.YoutubeDL(extract_opts) as ydl:
        try:
            print("Fetching metadata...")
            info = ydl.extract_info(url, download=False)
            if is_playlist and 'entries' in info:
                print(f"\nPlaylist: {info.get('title')}")
                print(f"Total Videos: {len(list(info['entries']))}")
            else:
                print(f"\nTitle: {info.get('title')}")
                size = info.get('filesize') or info.get('filesize_approx') or 0
                print(f"Estimated Size: {format_size(size)}")
            return input("\nProceed? (y/n): ").strip().lower() == 'y'
        except Exception as e:
            print(f"Error: {e}")
            return False


def download_video(url, save_path, res_choice="best"):
    ydl_opts = get_base_opts()
    ydl_opts.update({
        "format": RESOLUTIONS.get(res_choice, "bestvideo+bestaudio/best"),
        "outtmpl": os.path.join(save_path, "%(title)s.%(ext)s"),
        "merge_output_format": "mp4",
        "noplaylist": True,
    })

    if get_info_and_confirm(url, ydl_opts):
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            original_file = ydl.prepare_filename(info)

            # Ensure we have the correct path if merged to mp4
            if not os.path.exists(original_file):
                original_file = os.path.splitext(original_file)[0] + ".mp4"

            h264:str = input("Do you want to convert the downloaded video codec to h264 (better for compatability) ? ").strip().lower()
            if h264 == 'y':
                # Double-check existence because yt-dlp file extensions can be unpredictable
                if not os.path.exists(original_file):
                    # Fallback: check if an .mp4 version exists if the predicted one doesn't
                    base_path = os.path.splitext(original_file)[0]
                    if os.path.exists(f"{base_path}.mp4"):
                        original_file = f"{base_path}.mp4"

                if os.path.exists(original_file):
                    converted = convert_to_h264(original_file)

                    # Only delete original if the conversion actually created a new file
                    if converted and os.path.exists(converted):
                        try:
                            print(f"Cleaning up original file...")
                            os.remove(original_file)
                        except OSError as e:
                            print(f"Cleanup failed: {e}")
                else:
                    print(f"Error: Could not find downloaded file at {original_file}")


def download_audio(url, save_path):
    ydl_opts = get_base_opts()
    ydl_opts.update({
        "format": "bestaudio/best",
        "outtmpl": os.path.join(save_path, "%(title)s.%(ext)s"),
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
        "noplaylist": True,
    })
    if get_info_and_confirm(url, ydl_opts):
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])


def download_playlist_video_files(url, save_path, res_choice="best"):
    ydl_opts = get_base_opts()
    ydl_opts.update({
        "format": RESOLUTIONS.get(res_choice, "bestvideo+bestaudio/best"),
        "outtmpl": os.path.join(save_path, "%(playlist_title)s/%(playlist_index)s - %(title)s.%(ext)s"),
        "merge_output_format": "mp4",
    })
    if get_info_and_confirm(url, ydl_opts, is_playlist=True):
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            if 'entries' in info:
                for entry in info['entries']:
                    if entry is None: continue
                    file_path = ydl.prepare_filename(entry)
                    if not os.path.exists(file_path):
                        file_path = os.path.splitext(file_path)[0] + ".mp4"

                    converted = convert_to_h264(file_path)
                    if converted:
                        os.remove(file_path)


def download_playlist_audio_files(url, save_path):
    ydl_opts = get_base_opts()
    ydl_opts.update({
        "format": "bestaudio/best",
        "outtmpl": os.path.join(save_path, "%(playlist_title)s/%(playlist_index)s - %(title)s.%(ext)s"),
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192"
        }],
    })
    if get_info_and_confirm(url, ydl_opts, is_playlist=True):
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])


def download_playlist(url, save_path, res_choice="best"):
    print("\n(1) Video Playlist\n(2) Audio Playlist")
    c = input("Choice: ").strip()
    if c == "1":
        download_playlist_video_files(url, save_path, res_choice)
    elif c == "2":
        download_playlist_audio_files(url, save_path)


def main():
    print("\n--- YouTube Downloader & H.264 Converter ---")

    choice = input("Download (1) Video, (2) Playlist, or (3) Audio? ").strip()
    link = input("Enter link: ").strip()

    if not link:
        print("URL is required.")
        return

    save_dir = input("Enter save directory (blank for current folder): ").strip()
    if not save_dir:
        save_dir = os.getcwd()

    if not os.path.exists(save_dir):
        os.makedirs(save_dir, exist_ok=True)

    if choice == "1":
        print("Qualities: 360p, 480p, 720p, 1080p, best")
        res = input("Choice: ").strip().lower()
        download_video(link, save_dir, res)
    elif choice == "2":
        download_playlist(link, save_dir, "best")
    elif choice == "3":
        download_audio(link, save_dir)
    else:
        print("Invalid option.")


if __name__ == "__main__":
    try:
        update_ytdlp()

        terminate:bool = False
        while(not terminate):
            main()
            exit = input("Do you want to terminate? (Y/N) ").strip().lower()
            if exit == "y":
                terminate = True

    except KeyboardInterrupt:
        print("\n\nExiting...")
        sys.exit(0)
