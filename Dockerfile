FROM python:3.14-rc-slim

# Install FFmpeg
RUN apt-get update && apt-get install -y ffmpeg && apt-get clean

# Install yt-dlp
RUN pip install --no-cache-dir yt-dlp

# Create downloads folder
RUN mkdir /downloads

# Copy the script
COPY Piratetube-Docker.py /app/Piratetube-Docker.py

WORKDIR /app

CMD ["python", "Piratetube-Docker.py"]
