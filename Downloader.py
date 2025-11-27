import yt_dlp

RESOLUTIONS = {
    "360p": "bestvideo[height<=360]+bestaudio",
    "480p": "bestvideo[height<=480]+bestaudio",
    "720p": "bestvideo[height<=720]+bestaudio",
    "1080p": "bestvideo[height<=1080]+bestaudio",
    "best": "bestvideo+bestaudio"
}

def download_video(url, res_choice="best"):
    ydl_opts = {
        "format": RESOLUTIONS.get(res_choice, "bestvideo+bestaudio"),
        "outtmpl": "%(title)s.%(ext)s",  # Save as video title
        "merge_output_format": "mp4",  # Merge audio+video automatically
        "noplaylist": True
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def download_playlist(url, res_choice="best"):
    ydl_opts = {
        "format": RESOLUTIONS.get(res_choice, "bestvideo+bestaudio"),
        "outtmpl": "%(playlist_index)s - %(title)s.%(ext)s",
        "merge_output_format": "mp4"
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def download_audio(url: str):
    ydl_opts = {
        "format": "bestaudio",
        "outtmpl": "%(title)s.%(ext)s",

        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "0"
            }
        ]
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


def main():
    print("YouTube Downloader (Python + yt-dlp)")
    print("GitHub: https://github.com/yt-dlp/yt-dlp")

    choice = input("Download (1) video, (2) playlist, or (3) Audio? ").strip()
    link = input("Enter the YouTube link: ").strip()

    res_choice:str = ""
    if choice == "1" or choice == "2":
        print("\nAvailable qualities: 360p, 480p, 720p, 1080p, best")
        res_choice = input("Enter the quality you want: ").strip().lower()

    if choice == "1":
        download_video(link, res_choice)
    elif choice == "2":
        download_playlist(link, res_choice)
    elif choice == "3":
        download_audio(link)
    else:
        print("Invalid choice!")

    print("Download complete!")


if __name__ == "__main__":
    main()