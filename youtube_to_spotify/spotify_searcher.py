import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()

SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
SPOTIPY_REDIRECT_URI = os.getenv('SPOTIPY_REDIRECT_URI')

scope = 'playlist-modify-private'  # Change based on your playlist privacy settings
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                               client_secret=SPOTIPY_CLIENT_SECRET,
                                               redirect_uri=SPOTIPY_REDIRECT_URI,
                                               scope=scope))

def add_songs_to_spotify_playlist(track_names, playlist_id):
    """Adds a list of songs to a specified Spotify playlist."""
    try:
        track_ids = []
        for track in track_names:
            results = sp.search(q=track, type='track', limit=1)
            if results['tracks']['items']:
                track_id = results['tracks']['items'][0]['id']
                track_ids.append(track_id)

        if track_ids:
            sp.user_playlist_add_tracks(os.getenv('username'), playlist_id, track_ids)
        print(f"Added {len(track_ids)} tracks to playlist.")
    except spotipy.exceptions.SpotifyException as e:
        print(f"An error occurred while adding tracks: {e}")
