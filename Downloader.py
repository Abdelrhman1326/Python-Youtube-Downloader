import yt_dlp
import subprocess
import sys
import os

RESOLUTIONS = {
    "360p": "bestvideo[height<=360]+bestaudio/best[height<=360]",
    "480p": "bestvideo[height<=480]+bestaudio/best[height<=480]",
    "720p": "bestvideo[height<=720]+bestaudio/best[height<=720]",
    "1080p": "bestvideo[height<=1080]+bestaudio/best[height<=1080]",
    "best": "bestvideo+bestaudio/best"
}

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
    """
    Standardizing options to bypass throttling and handle connection drops.
    """
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
            print("Fetching metadata... (this may take a moment)")
            info = ydl.extract_info(url, download=False)

            if is_playlist and 'entries' in info:
                title = info.get('title', 'Unknown Playlist')
                entries = list(info['entries'])
                print(f"\nPlaylist: {title}")
                print(f"Total Videos: {len(entries)}")
                est_size = len(entries) * 50 * 1024 * 1024
                print(f"Estimated Download Size: ~{format_size(est_size)}")
            else:
                print(f"\nTitle: {info.get('title')}")
                size = info.get('filesize') or info.get('filesize_approx') or 0
                print(f"Estimated Size: {format_size(size)}")

            return input("\nProceed with download? (y/n): ").strip().lower() == 'y'
        except Exception as e:
            print(f"Error gathering info: {e}")
            return False

def download_video(url, save_path, res_choice="best"):
    ydl_opts = get_base_opts()
    ydl_opts.update({
        "format": RESOLUTIONS.get(res_choice, "bestvideo+bestaudio/best"),
        "outtmpl": os.path.join(save_path, "%(title)s.%(ext)s"),
        "merge_output_format": "mp4",
        "noplaylist": True,
        "quiet": False,
    })
    if get_info_and_confirm(url, ydl_opts):
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

def download_audio(url, save_path):
    """
    Downloads a single audio track and converts it to MP3.
    """
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
        "quiet": False,
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
        "quiet": False,
    })
    if get_info_and_confirm(url, ydl_opts, is_playlist=True):
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

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
        "quiet": False,
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
    update_ytdlp()
    print("\n--- YouTube Downloader ---")

    choice = input("Download (1) Video, (2) Playlist, or (3) Audio? ").strip()
    link = input("Enter link: ").strip()

    if not link:
        print("URL is required.")
        return

    save_dir = input("Enter save directory (leave blank for current folder): ").strip()
    if not save_dir:
        save_dir = os.getcwd()

    if not os.path.exists(save_dir):
        try:
            os.makedirs(save_dir)
        except Exception as e:
            print(f"Could not create directory: {e}")
            return

    res_choice = "best"
    if choice == "1":
        print("Qualities: 360p, 480p, 720p, 1080p, best")
        res_choice = input("Choice: ").strip().lower()
        download_video(link, save_dir, res_choice)
    elif choice == "2":
        download_playlist(link, save_dir, res_choice)
    elif choice == "3":
        download_audio(link, save_dir)
    else:
        print("Invalid option.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProcess interrupted by user. Exiting...")
        sys.exit(0)
