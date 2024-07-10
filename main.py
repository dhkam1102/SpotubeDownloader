import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from googleapiclient.discovery import build
import spotify_scraper  
import youtube_searcher 
import downloader

# Load environment variables
load_dotenv()

# Get environment variables
SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
SPOTIPY_REDIRECT_URI = os.getenv('SPOTIPY_REDIRECT_URI')
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')

scope = 'playlist-read-private'
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                               client_secret=SPOTIPY_CLIENT_SECRET,
                                               redirect_uri=SPOTIPY_REDIRECT_URI,
                                               scope=scope))

username = os.getenv('username')
playlist_id = os.getenv('playlist_id')

def main():
    tracks = spotify_scraper.fetch_playlist_tracks(username, playlist_id)
    spotify_scraper.write_tracks_to_file(tracks)

    for i, item in enumerate(tracks):
        track = item['track']
        query = f"{track['name']} {track['artists'][0]['name']}"
        print(f"Searching YouTube for: {query}")
        results = youtube_searcher.youtube_search(query)
        print(f"Results for {query}:")
        for video in results:
            print(video)
        print("\n")

    file_path = 'youtube_urls.txt'  # The file containing YouTube URLs, one per line
    output_path = '/Users/briankam/github_project/SpotubedSongs'  # The folder to save downloaded songs
    downloader.download_songs_from_file(file_path, output_path)

if __name__ == "__main__":
    main()
