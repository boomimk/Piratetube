<p align="center">
  <h1 align="center">🎬 PirateTube</h1>
  <p align="center">A simple, no-nonsense YouTube video downloader for Windows</p>
  <p align="center">
    <img src="https://img.shields.io/badge/platform-Windows-informational?style=for-the-badge" />
    <img src="https://img.shields.io/badge/Maintained%3F-yes-green.svg?style=for-the-badge" />
  </p>
</p>

---

## Info

Only use Piratetube to download videos that you have permission to download.

I am not responsable for how Piratetube is used in any way shape or form.

if you are having truble you can just download the python file and run only that and it will work.

ONLY WORKS ON WINDOWS FOR NOW.

---

## ✨ Features

-  Download videos in any available resolution (4K, 1080p, 720p, and more)
-  Audio automatically encoded to AAC 192kbps for universal compatibility
-  Shows file size estimates before you download
-  Saves directly to your **Downloads** folder

---

## 🐳 Use with Docker

PirateTube can also be run in a Docker container for a consistent environment across systems.

### Quick Start with Docker Compose

```bash
docker-compose up
```

This will:
- Build the Docker image automatically
- Mount your **Downloads** folder to the container
- Run PirateTube in interactive mode

### 🔨 Manual Docker Build

If you prefer to build and run manually:

```bash
docker build -t piratetube .
docker run -it -v ~/Downloads:/downloads piratetube
```

**Note**: On Windows, replace `~/Downloads` with your actual Downloads folder path, e.g., `C:\Users\YourUsername\Downloads:/downloads`