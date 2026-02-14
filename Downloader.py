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

def update_ytdlp():
    """Update yt-dlp to the latest version"""
    print("Updating yt-dlp to the latest version...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "yt-dlp"])
        print("yt-dlp updated successfully!\n")
    except Exception as e:
        print(f"Failed to update yt-dlp: {e}\n")

def download_video(url, res_choice="best"):
    ydl_opts = {
        "format": RESOLUTIONS.get(res_choice, "bestvideo+bestaudio/best"),
        "outtmpl": "%(title)s.%(ext)s",
        "merge_output_format": "mp4",
        "noplaylist": True,
        "quiet": False,
        "no_warnings": False,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except yt_dlp.utils.DownloadError as e:
        print(f"\nError downloading video: {e}")
        print("Try updating yt-dlp: pip install --upgrade yt-dlp")
        raise

def download_playlist(url, res_choice="best"):
    ydl_opts = {
        "format": RESOLUTIONS.get(res_choice, "bestvideo+bestaudio/best"),
        "outtmpl": "%(playlist_index)s - %(title)s.%(ext)s",
        "merge_output_format": "mp4",
        "quiet": False,
        "no_warnings": False,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except yt_dlp.utils.DownloadError as e:
        print(f"\nError downloading playlist: {e}")
        print("Try updating yt-dlp: pip install --upgrade yt-dlp")
        raise

def download_audio(url: str):
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": "%(title)s.%(ext)s",
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192"
            }
        ],
        "quiet": False,
        "no_warnings": False,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except yt_dlp.utils.DownloadError as e:
        print(f"\nError downloading audio: {e}")
        print("Try updating yt-dlp: pip install --upgrade yt-dlp")
        raise

def main():
    print("YouTube Downloader (Python + yt-dlp)")
    print("GitHub: https://github.com/yt-dlp/yt-dlp\n")
    
    # Ask if user wants to update yt-dlp first
    update = input("Update yt-dlp to latest version? (y/n): ").strip().lower()
    if update == "y":
        update_ytdlp()
    
    choice = input("Download (1) video, (2) playlist, or (3) Audio? ").strip()
    link = input("Enter the YouTube link: ").strip()
    
    res_choice: str = ""
    if choice == "1" or choice == "2":
        print("\nAvailable qualities: 360p, 480p, 720p, 1080p, best")
        res_choice = input("Enter the quality you want: ").strip().lower()
    
    try:
        if choice == "1":
            download_video(link, res_choice)
        elif choice == "2":
            download_playlist(link, res_choice)
        elif choice == "3":
            download_audio(link)
        else:
            print("Invalid choice!")
            return
        
        print("\nDownload complete!")
    except Exception as e:
        print(f"\nDownload failed: {e}")

if __name__ == "__main__":
    main()