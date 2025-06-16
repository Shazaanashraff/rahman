
import yt_dlp
//hello world
def list_formats(video_url):
    """Fetch and list all available formats for the video."""
    ydl_opts = {"quiet": True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(video_url, download=False)
        formats = info_dict.get("formats", [])
        
        # Display available formats
        print(f"\n{'ID':<8}{'Resolution':<12}{'FPS':<8}{'Size':<12}{'Note':<20}")
        print("-" * 60)
        for fmt in formats:
            fmt_id = fmt.get("format_id", "Unknown")
            resolution = f"{fmt.get('width', '?')}x{fmt.get('height', '?')}"
            fps = fmt.get("fps", "N/A") or "N/A"  # Handle missing FPS
            filesize = (
                f"{fmt.get('filesize', 0) / (1024 * 1024):.2f} MB"
                if fmt.get("filesize") else "Unknown"
            )
            format_note = fmt.get("format_note", "Unknown") or "Unknown"  # Handle missing notes
            print(f"{fmt_id:<8}{resolution:<12}{fps:<8}{filesize:<12}{format_note:<20}")
        
        return formats

def download_video_with_audio(video_url, format_id):
    """Download the selected video format and merge it with the best audio."""
    ydl_opts = {
        "format": f"{format_id}+bestaudio/best",  # Select video and best audio
        "merge_output_format": "mp4",            # Merge into MP4
        "outtmpl": "%(title)s.%(ext)s",          # Output filename
        "postprocessors": [{                     # Ensure audio is merged
            "key": "FFmpegVideoConvertor",
            "preferedformat": "mp4",
        }],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

def main():
    """Main function to handle user input and download logic."""
    video_url = input("Enter the YouTube video URL: ").strip()
    formats = list_formats(video_url)
    
    if not formats:
        print("No formats available for this video.")
        return
    
    selected_format_id = input("\nEnter the format ID for your desired resolution: ").strip()
    download_video_with_audio(video_url, selected_format_id)
    print("\nDownload completed with video and audio merged!")

if __name__ == "__main__":
    main()
