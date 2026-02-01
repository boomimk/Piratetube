import yt_dlp
from pathlib import Path

# Create PYT folder on Desktop
DESKTOP_PATH = Path.home() / "Desktop"
PYT_FOLDER = DESKTOP_PATH / "PYT"
PYT_FOLDER.mkdir(exist_ok=True)


class MyLogger:
    def debug(self, msg): pass

    def warning(self, msg):
        if "No supported JavaScript runtime" not in msg:
            print(f"⚠️  {msg}")

    def error(self, msg):
        print(f"❌ {msg}")


def get_simple_formats(url):
    """Fetches only formats that have both Video + Audio (No FFmpeg needed)"""
    # 'b' stands for best single file (progressive)
    ydl_opts = {'logger': MyLogger(), 'noplaylist': True}

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        formats = info.get('formats', [])

        options = []
        print(f"\n📹 Title: {info.get('title')}")
        print(f"{'#':<3} | {'Resolution':<10} | {'Type'}")
        print("-" * 30)

        count = 1
        for f in formats:
            # acodec != none AND vcodec != none means it's a complete file
            if f.get('acodec') != 'none' and f.get('vcodec') != 'none':
                res = f.get('height')
                ext = f.get('ext')
                options.append({'id': f.get('format_id'), 'res': res})
                print(f"{count:<3} | {res:>4}p         | {ext}")
                count += 1

        return options


def download_video(url, format_id):
    ydl_opts = {
        'format': format_id,  # Just download the exact ID, no merging (+)
        'outtmpl': f'{PYT_FOLDER}/%(title)s.%(ext)s',
        'logger': MyLogger(),
        'progress_hooks': [progress_hook],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


def progress_hook(d):
    if d['status'] == 'downloading':
        print(f"\r⏬ Downloading: {d.get('_percent_str', '0%')}", end='')
    elif d['status'] == 'finished':
        print("\n✅ Saved!")


def main():
    print("--- SIMPLE DOWNLOADER (No FFmpeg Required) ---")
    while True:
        url = input("\nURL (or 'q'): ").strip()
        if url.lower() == 'q': break

        try:
            options = get_simple_formats(url)
            if not options:
                print("No simple formats found. YouTube might be blocking this video.")
                continue

            choice = input("\nPick # (usually the bottom one is best): ")
            if choice.isdigit() and 0 < int(choice) <= len(options):
                selected = options[int(choice) - 1]
                download_video(url, selected['id'])
            else:
                print("Invalid choice.")
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()