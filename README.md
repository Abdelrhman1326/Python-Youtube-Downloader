# YouTube Downloader

A powerful and easy-to-use CLI tool to download YouTube videos, playlists, and audio directly to your computer. Built with Python and powered by `yt-dlp` and `FFmpeg`.

## 🚀 Features

- **Video Downloads**: Download single videos in various resolutions (360p, 480p, 720p, 1080p, or Best Available).
- **Playlist Downloads**: Effortlessly download entire playlists as either Video or Audio files.
- **Audio Extraction**: Download high-quality audio directly as MP3 files (192kbps).
- **Format Compatibility**: Automatically merges video and audio into high-quality `.mp4` files.
- **H.264 Conversion**: Includes built-in logic to convert videos to H.264 for maximum compatibility across all devices.
- **Auto-Update**: Automatically checks for and installs `yt-dlp` updates every time you run the app to ensure it stays compatible with YouTube's changes.

## 🛠️ System Requirements

The installation scripts will attempt to automatically install these for you if they are missing:

- **FFmpeg**: Essential for merging high-resolution video and audio.
- **Deno**: Required for environment support.
- **Python 3.8+**: Should be installed on your system before running the setup.

## 📥 Installation

The repository includes setup scripts that handle dependency installation (including FFmpeg and Deno) and environment configuration.

### Windows (PowerShell)
1. Open PowerShell as Administrator (required for `winget` to install FFmpeg/Deno).
2. Run the setup script:
   ```powershell
   ./setup.ps1
   ```

### Linux / macOS (Bash)
1. Open your terminal.
2. Make the script executable and run it:
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

## 🎮 How to Use

Simply run the start script, and the interactive CLI will guide you through the process.

### Running the App
- **Windows**: `./start.ps1`
- **Linux / macOS**: `./start.sh`

### Step-by-Step Guide
1. **Choose Download Type**: Select (1) Video, (2) Playlist, or (3) Audio.
2. **Enter URL**: Paste the YouTube link you want to download.
3. **Save Directory**: Enter a path to save the file (or leave blank to save in the current folder).
4. **Choose Quality**: For videos, select your preferred resolution (e.g., `1080p`).
5. **Confirm**: The app will show you the video title and estimated size. Type `y` to start the download!

## ⚙️ How it Works

- **yt-dlp**: Used for high-speed metadata extraction and downloading.
- **FFmpeg**: Handles the merging of separate video and audio streams into a single MP4 file.
- **Virtual Environment**: The scripts automatically create and manage a `.venv` folder to keep your system Python clean.

## 📄 License

This project is intended for personal use. Please respect the terms of service of the content platforms you use.
