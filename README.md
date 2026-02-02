# 🎬 PirateTube - YouTube Downloader

A Docker-based YouTube video downloader with an interactive terminal interface.

## ✨ Features

- 🎥 Download YouTube videos in multiple qualities
- 🎵 AAC audio encoding for universal compatibility
- 📊 Interactive quality selection
- 🚀 Progress bar with download speed and ETA
- 🐳 Runs in Docker - no Python setup required!

## 🚀 Quick Start (Docker)

### Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running

### Run with ONE Command

**Windows (PowerShell):**
```powershell
docker run -it --rm -v C:\Users\$env:USERNAME\Downloads:/downloads yourusername/piratetube
```

**Mac/Linux:**
```bash
docker run -it --rm -v ~/Downloads:/downloads yourusername/piratetube
```

That's it! Videos will be saved to your Downloads folder.

## 📖 Usage

1. Run the command above
2. Paste a YouTube URL when prompted
3. Choose video quality (or press Enter for best quality)
4. Wait for download to complete
5. Find your video in Downloads folder
6. Type `q` to quit

## 🛠️ Build From Source

If you want to build the Docker image yourself:

```bash
# Clone the repository
git clone https://github.com/yourusername/piratetube.git
cd piratetube

# Build the Docker image
docker build -t piratetube .

# Run it
docker run -it --rm -v ~/Downloads:/downloads piratetube
```

## 📋 What's Included

- **Piratetube-Docker.py** - Main Python script
- **Dockerfile** - Docker configuration
- **requirements.txt** - Python dependencies

## 🔧 Manual Installation (Without Docker)

If you prefer to run without Docker:

1. Install Python 3.12+
2. Install FFmpeg
3. Install dependencies:
   ```bash
   pip install yt-dlp
   ```
4. Run the script:
   ```bash
   python Piratetube-Docker.py
   ```

## 🐛 Troubleshooting

**Problem: "docker: command not found"**
- Install Docker Desktop from https://www.docker.com/products/docker-desktop/

**Problem: "Cannot connect to Docker daemon"**
- Make sure Docker Desktop is running

**Problem: Videos not in Downloads folder**
- Make sure you used the `-v` flag in the command

**Problem: Want to rebuild after code changes**
```bash
docker pull yourusername/piratetube:latest
```

## 📝 License

MIT License - feel free to use and modify!

## ⚠️ Disclaimer

This tool is for personal use only. Please respect YouTube's Terms of Service and copyright laws.

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first.

## 📞 Support

If you encounter any issues, please open an issue on GitHub.

---

Made with ❤️ for easy video downloads
