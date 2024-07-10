import yt_dlp

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

def download_songs_from_file(file_path, output_path):
    with open(file_path, 'r') as file:
        urls = file.readlines()

    for url in urls:
        download_audio_from_youtube(url.strip(), output_path)

if __name__ == "__main__":
    file_path = 'youtube_urls.txt'  # The file containing YouTube URLs, one per line
    output_path = '/Users/briankam/github_project/SpotubedSongs'  # The folder to save downloaded songs
    download_songs_from_file(file_path, output_path)
