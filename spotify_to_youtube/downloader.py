import yt_dlp
import zipfile
import os

def download_audio_from_youtube(url, output_path):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_path + '/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def compress_file(file_path):
    """Compresses the given audio file into a ZIP archive."""
    zip_path = f"{file_path}.zip"
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(file_path, os.path.basename(file_path))
    
    # Optionally, delete the original uncompressed file after zipping it
    os.remove(file_path)
    
    return zip_path

def download_songs_from_file(file_path, output_path):
    with open(file_path, 'r') as file:
        urls = file.readlines()

for url in urls:
        url = url.strip()
        download_audio_from_youtube(url, output_path)

        # Find the downloaded file by looking for the MP3 file in the output path
        for file in os.listdir(output_path):
            if file.endswith(".mp3"):
                file_path = os.path.join(output_path, file)
                # Compress the downloaded file
                zip_path = compress_file(file_path)
                print(f"Compressed {file} to {zip_path}")


if __name__ == "__main__":
    file_path = 'youtube_urls.txt'  # The file containing YouTube URLs, one per line
    output_path = '/Users/briankam/github_project/SpotubedSongs'  # The folder to save downloaded songs
    download_songs_from_file(file_path, output_path)
