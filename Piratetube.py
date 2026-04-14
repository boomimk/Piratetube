import yt_dlp
from pathlib import Path
import os

# Create PYT folder on Desktop
DESKTOP_PATH = Path.home() / "Desktop"
PYT_FOLDER = DESKTOP_PATH / "PYT"
PYT_FOLDER.mkdir(exist_ok=True)


# Color codes for pretty terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


def print_header():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"\n{Colors.CYAN}{'═' * 70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}                    🎬 YOUTUBE DOWNLOADER PRO 🎬{Colors.END}")
    print(f"{Colors.CYAN}{'═' * 70}{Colors.END}\n")


def print_success(msg):
    print(f"{Colors.GREEN}✓ {msg}{Colors.END}")


def print_error(msg):
    print(f"{Colors.RED}✗ {msg}{Colors.END}")


def print_info(msg):
    print(f"{Colors.CYAN}ℹ {msg}{Colors.END}")


def print_warning(msg):
    print(f"{Colors.YELLOW}⚠ {msg}{Colors.END}")


class MyLogger:
    def debug(self, msg): pass

    def warning(self, msg):
        if "JavaScript" not in msg:
            print_warning(msg)

    def error(self, msg):
        print_error(msg)


def get_available_formats(url):
    """Fetches all available video resolutions"""
    ydl_opts = {'logger': MyLogger(), 'noplaylist': True, 'quiet': True}

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        formats = info.get('formats', [])

        # Pretty video info display
        print(f"\n{Colors.BOLD}📹 Title:{Colors.END} {Colors.CYAN}{info.get('title')}{Colors.END}")
        duration = info.get('duration', 0)
        print(f"{Colors.BOLD}⏱️  Duration:{Colors.END} {duration // 60}:{duration % 60:02d}")
        print(f"{Colors.BOLD}👤 Channel:{Colors.END} {info.get('uploader', 'Unknown')}\n")

        print(f"{Colors.CYAN}{'─' * 70}{Colors.END}")
        print(f"{Colors.BOLD}  {'#':<4} │ {'Quality':<15} │ {'FPS':<8} │ {'File Size (est.)'}{Colors.END}")
        print(f"{Colors.CYAN}{'─' * 70}{Colors.END}")

        # Collect unique video resolutions
        seen_heights = set()
        options = []

        for f in formats:
            height = f.get('height')
            vcodec = f.get('vcodec', 'none')
            fps = f.get('fps', 30)
            filesize = f.get('filesize') or f.get('filesize_approx', 0)

            if height and vcodec != 'none' and height not in seen_heights:
                seen_heights.add(height)

                # Estimate file size
                if filesize:
                    size_mb = filesize / (1024 * 1024)
                    size_str = f"{size_mb:.1f} MB"
                else:
                    size_str = "Unknown"

                # Quality label with color
                quality_label = f"{height}p"
                if height >= 1080:
                    quality_color = Colors.GREEN
                    badge = "🔥 HD"
                elif height >= 720:
                    quality_color = Colors.YELLOW
                    badge = "📺 HD"
                else:
                    quality_color = Colors.END
                    badge = "📱 SD"

                options.append({
                    'height': height,
                    'fps': fps,
                    'size': size_str,
                    'label': quality_label,
                    'badge': badge
                })

        # Sort by resolution (highest first)
        options.sort(key=lambda x: x['height'], reverse=True)

        count = 1
        for opt in options:
            if opt['height'] >= 1080:
                color = Colors.GREEN
            elif opt['height'] >= 720:
                color = Colors.YELLOW
            else:
                color = Colors.END

            print(f"  {color}{count:<4} │ {opt['label']:<15} │ {opt['fps']:<8} │ {opt['size']}{Colors.END}")
            count += 1

        print(f"{Colors.CYAN}{'─' * 70}{Colors.END}\n")
        return options


def download_video(url, resolution):
    """Downloads video with proper audio encoding"""
    ydl_opts = {
        'format': f'bestvideo[height<={resolution}]+bestaudio/best[height<={resolution}]',
        'outtmpl': f'{PYT_FOLDER}/%(title)s.%(ext)s',
        'logger': MyLogger(),
        'progress_hooks': [progress_hook],
        'merge_output_format': 'mp4',
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
        }],
        'postprocessor_args': [
            '-c:v', 'copy',
            '-c:a', 'aac',
            '-b:a', '192k',
        ],
        'prefer_ffmpeg': True,
        'quiet': True,
        'no_warnings': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        print(f"\n{Colors.BLUE}🎬 Downloading {resolution}p video + audio...{Colors.END}\n")
        ydl.download([url])


def progress_hook(d):
    if d['status'] == 'downloading':
        percent = d.get('_percent_str', '0%').strip()
        speed = d.get('_speed_str', 'N/A').strip()
        eta = d.get('_eta_str', 'N/A').strip()
        downloaded = d.get('_downloaded_bytes_str', '0B').strip()
        total = d.get('_total_bytes_str', '?B').strip()

        # Progress bar
        try:
            percent_num = float(percent.replace('%', ''))
            bar_length = 40
            filled = int(bar_length * percent_num / 100)
            bar = '█' * filled + '░' * (bar_length - filled)

            print(f"\r{Colors.CYAN}[{bar}]{Colors.END} {Colors.BOLD}{percent}{Colors.END} │ "
                  f"{Colors.GREEN}{speed}{Colors.END} │ ETA: {Colors.YELLOW}{eta}{Colors.END} │ "
                  f"{downloaded}/{total}", end='', flush=True)
        except:
            print(f"\r⏬ Downloading: {percent} at {speed}", end='', flush=True)

    elif d['status'] == 'finished':
        print(f"\n\n{Colors.YELLOW}🔄 Processing with FFmpeg (optimizing audio)...{Colors.END}")


def test_ffmpeg():
    """Check if FFmpeg is installed"""
    import subprocess
    try:
        result = subprocess.run(['ffmpeg', '-version'],
                                capture_output=True,
                                text=True,
                                timeout=5)
        if result.returncode == 0:
            print_success("FFmpeg detected and ready!")
            return True
    except:
        pass

    print_error("FFmpeg not found in PATH!")
    print_info("Please restart your terminal after installing FFmpeg")
    return False


def main():
    print_header()

    if not test_ffmpeg():
        print(f"\n{Colors.RED}Please restart your terminal and try again.{Colors.END}")
        input("\nPress Enter to exit...")
        return

    print_info(f"Downloads will be saved to: {Colors.BOLD}{PYT_FOLDER}{Colors.END}\n")

    while True:
        print(f"{Colors.BOLD}{'─' * 70}{Colors.END}")
        url = input(f"{Colors.BOLD}🔗 Enter YouTube URL{Colors.END} (or {Colors.RED}'q'{Colors.END} to quit): ").strip()
        print(f"{Colors.BOLD}{'─' * 70}{Colors.END}")

        if url.lower() == 'q':
            print(f"\n{Colors.CYAN}👋 Thanks for using YouTube Downloader Pro!{Colors.END}\n")
            break

        if not url:
            continue

        try:
            options = get_available_formats(url)

            if not options:
                print_error("No formats found for this video.")
                continue

            print_info(f"{Colors.BOLD}Higher numbers = Better quality (but larger files){Colors.END}")
            choice = input(
                f"\n{Colors.BOLD}Pick a number (1-{len(options)}){Colors.END} or press {Colors.GREEN}Enter{Colors.END} for best quality: ").strip()

            if not choice:
                selected_res = options[0]['height']
                print_info(f"Auto-selected best quality: {Colors.BOLD}{selected_res}p{Colors.END}")
            elif choice.isdigit() and 0 < int(choice) <= len(options):
                selected_res = options[int(choice) - 1]['height']
            else:
                print_error("Invalid choice.")
                continue

            download_video(url, selected_res)

            print(f"\n{Colors.GREEN}{'═' * 70}{Colors.END}")
            print(f"{Colors.BOLD}{Colors.GREEN}✨ DOWNLOAD COMPLETE! ✨{Colors.END}")
            print(f"{Colors.GREEN}{'═' * 70}{Colors.END}")
            print_success(f"Video saved to: {Colors.BOLD}{PYT_FOLDER}{Colors.END}")
            print_success(f"Audio format: {Colors.BOLD}AAC 192kbps{Colors.END} (universal compatibility)")
            print(f"{Colors.GREEN}{'═' * 70}{Colors.END}\n")

        except KeyboardInterrupt:
            print(f"\n\n{Colors.YELLOW}⏸️  Download cancelled by user.{Colors.END}\n")
        except Exception as e:
            print(f"\n{Colors.RED}{'═' * 70}{Colors.END}")
            print_error(f"An error occurred: {e}")
            print(f"{Colors.RED}{'═' * 70}{Colors.END}\n")


if __name__ == "__main__":
    main()