import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()

SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
SPOTIPY_REDIRECT_URI = os.getenv('SPOTIPY_REDIRECT_URI')

#for public playlists
# scope = ''

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

def write_tracks_to_file(tracks, filename="playlist_songs.txt"):
    with open(filename, "w") as file:
        for i, item in enumerate(tracks):
            track = item['track']
            track_name = track['name']
            artist_name = track['artists'][0]['name']
            file.write(f"{i + 1}: {track_name} by {artist_name}\n")
    print(f"Tracks written to {filename}")

if __name__ == "__main__":
    tracks = fetch_playlist_tracks(username, playlist_id)
    write_tracks_to_file(tracks)
