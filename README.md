
# SpotubeDownloader

## Description

SpotubeDownloader is a Python-based tool that automates the process of transferring playlists from Spotify to YouTube. It scrapes songs from a Spotify playlist, searches for corresponding tracks on YouTube, downloads them, and compresses the audio files for offline use. With seamless integration between Spotify and YouTube, SpotubeDownloader makes it easy to enjoy your favorite playlists without requiring access to Spotify.

Originally, the tool was inspired by the need to access music from a personal Spotify playlist when Spotify wasn’t available. Now, with SpotubeDownloader, you can automate the entire process of fetching music from Spotify, searching for it on YouTube, and downloading it to your device—all while ensuring media retention through SQLite database tracking and file compression.

## Features

- **Scrape songs from Spotify playlists**: Automatically retrieve song names and artist details from your Spotify playlists.
- **Search for corresponding songs on YouTube**: Use the YouTube API to search for matching songs based on the Spotify data.
- **Retrieve and store YouTube URLs**: Track YouTube video links for easy access and downloads.
- **Download songs from YouTube**: Use `yt-dlp` to download the highest-quality audio from YouTube videos.
- **File compression**: Automatically compress downloaded audio files to save space while retaining media for offline access.
- **SQLite database integration**: Track downloaded songs and metadata in a SQLite database to avoid redundant downloads and ensure 100% media retention.

## Technologies Used

- **Python**: Core programming language for the project.
- **Spotify API**: Used to scrape playlist data from your Spotify account.
- **YouTube Data API**: Used to search for songs on YouTube.
- **yt-dlp**: Command-line tool to download audio from YouTube.
- **SQLite**: Local database for storing media metadata and tracking downloads.
- **FFmpeg**: Tool used to convert and extract audio.
- **File Compression**: Compress downloaded audio files to reduce storage usage.

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/SpotubeDownloader.git
   cd SpotubeDownloader
   ```

2. **Set up a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Install `ffmpeg`**:
   - On MacOS: `brew install ffmpeg`
   - On Ubuntu: `sudo apt-get install ffmpeg`
   - On Windows: [Download from ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH

5. **Create a `.env` file**:
   You'll need to create a `.env` file in the root directory of the project with the following values:
   ```
   SPOTIPY_CLIENT_ID=your_spotify_client_id
   SPOTIPY_CLIENT_SECRET=your_spotify_client_secret
   SPOTIPY_REDIRECT_URI=http://localhost:8888/callback
   YOUTUBE_API_KEY=your_youtube_api_key
   username=your_spotify_username
   playlist_id=your_spotify_playlist_id
   ```

## Usage

1. **Fetch and download songs**:
   Once you have set up everything, simply run the main script to fetch songs from your Spotify playlist, search for them on YouTube, download them, and compress the audio files:
   ```bash
   python main.py
   ```

2. **Track downloaded media**:
   All downloaded media will be tracked in an SQLite database, ensuring that you don’t download the same song twice. File compression is applied automatically after download to save storage space.

## Project Structure

```
SpotubeDownloader/
├── spotify_to_youtube/
│   ├── spotify_scraper.py    # Handles scraping data from Spotify playlists
│   ├── youtube_searcher.py   # Handles searching YouTube for corresponding songs
│   ├── downloader.py         # Downloads songs from YouTube and compresses the files
│   └── db_manager.py         # Manages the SQLite database for tracking downloaded media
├── youtube_to_spotify/
│   └── (Future Implementation)
├── venv/                     # Virtual environment
├── .env                      # API keys and configuration (not included in the repo)
├── requirements.txt          # List of required Python packages
├── README.md                 # Project documentation
├── youtube_urls.txt          # Stores the YouTube URLs to download
└── main.py                   # Main script to run the downloader
```

## Future Features

- **YouTube to Spotify**: Add functionality to parse YouTube video descriptions for song titles and automatically add those songs to a Spotify playlist.
- **Error Handling**: Improve error handling for better resilience with API calls and downloads.
- **Playlist Comparison**: Allow users to compare Spotify and YouTube playlists to identify missing tracks.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
