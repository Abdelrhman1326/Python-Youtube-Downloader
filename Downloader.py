import yt_dlp
import subprocess
import sys

RESOLUTIONS = {
    "360p": "bestvideo[height<=360]+bestaudio/best[height<=360]",
    "480p": "bestvideo[height<=480]+bestaudio/best[height<=480]",
    "720p": "bestvideo[height<=720]+bestaudio/best[height<=720]",
    "1080p": "bestvideo[height<=1080]+bestaudio/best[height<=1080]",
    "best": "bestvideo+bestaudio/best"
}


def format_size(bytes):
    """Convert bytes to a human-readable format."""
    if bytes is None: return "Unknown size"
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes < 1024:
            return f"{bytes:.2f} {unit}"
        bytes /= 1024
    return f"{bytes:.2f} TB"


def update_ytdlp():
    print("Updating yt-dlp...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "yt-dlp"])
        print("yt-dlp updated successfully!\n")
    except Exception as e:
        print(f"Failed to update: {e}\n")


def get_info_and_confirm(url, opts, is_playlist=False):
    """Extracts info, calculates size, and asks for user confirmation."""
    with yt_dlp.YoutubeDL(opts) as ydl:
        try:
            # We set download=False to only fetch metadata
            info = ydl.extract_info(url, download=False)

            total_size = 0
            if is_playlist and 'entries' in info:
                print(f"\nPlaylist: {info.get('title')}")
                print(f"Videos: {len(info['entries'])}")
                for entry in info['entries']:
                    if entry:
                        total_size += entry.get('filesize') or entry.get('filesize_approx') or 0
            else:
                print(f"\nTitle: {info.get('title')}")
                total_size = info.get('filesize') or info.get('filesize_approx') or 0

            print(f"Estimated Size: {format_size(total_size)}")
            confirm = input("Proceed with download? (y/n): ").strip().lower()
            return confirm == 'y'
        except Exception as e:
            print(f"Error fetching info: {e}")
            return False


def download_video(url, res_choice="best"):
    ydl_opts = {
        "format": RESOLUTIONS.get(res_choice, "bestvideo+bestaudio/best"),
        "outtmpl": "%(title)s.%(ext)s",
        "merge_output_format": "mp4",
        "noplaylist": True,
    }
    if get_info_and_confirm(url, ydl_opts):
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])


def download_playlist(url, res_choice="best"):
    ydl_opts = {
        "format": RESOLUTIONS.get(res_choice, "bestvideo+bestaudio/best"),
        "outtmpl": "%(playlist_index)s - %(title)s.%(ext)s",
        "merge_output_format": "mp4",
    }
    if get_info_and_confirm(url, ydl_opts, is_playlist=True):
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])


def download_audio(url: str):
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": "%(title)s.%(ext)s",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192"
        }],
    }
    if get_info_and_confirm(url, ydl_opts):
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])


def main():
    print("YouTube Downloader (Python + yt-dlp)\n")

    update = input("Update yt-dlp? (y/n): ").strip().lower()
    if update == "y":
        update_ytdlp()

    choice = input("Download (1) video, (2) playlist, or (3) Audio? ").strip()
    link = input("Enter link: ").strip()

    res_choice = ""
    if choice in ["1", "2"]:
        print("\nQualities: 360p, 480p, 720p, 1080p, best")
        res_choice = input("Choice: ").strip().lower()

    if choice == "1":
        download_video(link, res_choice)
    elif choice == "2":
        download_playlist(link, res_choice)
    elif choice == "3":
        download_audio(link)
    else:
        print("Invalid choice!")


if __name__ == "__main__":
    main()