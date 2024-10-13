import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import spotify_scraper as spotify_scraper  
import youtube_searcher as youtube_searcher 
import downloader as downloader
from db_manager import create_table, insert_song, check_song_exists

# Load environment variables
load_dotenv()

# Get environment variables
SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
SPOTIPY_REDIRECT_URI = os.getenv('SPOTIPY_REDIRECT_URI')
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')

# Spotify scope for reading private playlists
scope = 'playlist-read-private'
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                               client_secret=SPOTIPY_CLIENT_SECRET,
                                               redirect_uri=SPOTIPY_REDIRECT_URI,
                                               scope=scope))

# Set user credentials
username = os.getenv('username')
playlist_id = os.getenv('playlist_id')

# Set output paths
file_path = 'youtube_urls.txt'  # File containing YouTube URLs
output_path = '/Users/briankam/github_project/SpotubedSongs'  # Folder to save downloaded songs

def search_and_download(tracks):
    """Searches for tracks on YouTube, downloads them, and logs in the database."""
    
    for i, item in enumerate(tracks):
        track = item['track']
        song_name = track['name']
        query = f"{track['name']} {track['artists'][0]['name']}"

        # Check if the song has already been downloaded
        if check_song_exists(song_name):
            print(f"Song '{song_name}' already exists in the database. Skipping download.")
            continue

        # Search for the song on YouTube
        print(f"Searching YouTube for: {query}")
        results = youtube_searcher.youtube_search(query)

        if not results:
            print(f"No results for '{query}' on YouTube.")
            continue

        # Extract video URL and add to download queue
        video_url = results[0].split(", URL: ")[1]
        youtube_url = video_url  # For storing in the database

        with open(file_path, 'a') as f:
            f.write(f"{video_url}\n")

        # Download the song from YouTube
        downloader.download_songs_from_file(file_path, output_path)

        # Log the song in the SQLite database
        spotify_id = track['id']  # Store Spotify ID for reference
        insert_song(song_name, youtube_url, spotify_id, output_path)
        print(f"Inserted '{song_name}' into the database.")

def main():
    create_table()

    print("Fetching Spotify playlist tracks...")
    tracks = spotify_scraper.fetch_playlist_tracks(username, playlist_id)
    spotify_scraper.write_tracks_to_file(tracks)

    search_and_download(tracks)

if __name__ == "__main__":
    main()
