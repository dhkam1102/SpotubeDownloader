import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from googleapiclient.discovery import build

load_dotenv()

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

def fetch_playlist_tracks(username, playlist_id):
    results = sp.user_playlist_tracks(username, playlist_id)
    tracks = results['items']
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    return tracks

def youtube_search(query, max_results=5):
    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

    search_response = youtube.search().list(
        q=query,
        part='snippet',
        maxResults=max_results
    ).execute()

    videos = []
    for search_result in search_response.get('items', []):
        if search_result['id']['kind'] == 'youtube#video':
            videos.append(f"Title: {search_result['snippet']['title']}, URL: https://www.youtube.com/watch?v={search_result['id']['videoId']}")

    return videos

def write_tracks_to_file(tracks, filename="playlist_songs.txt"):
    with open(filename, "w") as file:  # Change "w" to "a" to append instead of overwrite
        for i, item in enumerate(tracks):
            track = item['track']
            track_name = track['name']
            artist_name = track['artists'][0]['name']
            file.write(f"{i + 1}: {track_name} by {artist_name}\n")
    print(f"Tracks written to {filename}")

def main():
    tracks = fetch_playlist_tracks(username, playlist_id)
    write_tracks_to_file(tracks)

    for i, item in enumerate(tracks):
        track = item['track']
        query = f"{track['name']} {track['artists'][0]['name']}"
        print(f"Searching YouTube for: {query}")
        results = youtube_search(query)
        print(f"Results for {query}:")
        for video in results:
            print(video)
        print("\n")

if __name__ == "__main__":
    main()
