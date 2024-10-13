import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()

SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
SPOTIPY_REDIRECT_URI = os.getenv('SPOTIPY_REDIRECT_URI')

# scope = 'playlist-modify-private'  # Change based on your playlist privacy settings
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                               client_secret=SPOTIPY_CLIENT_SECRET,
                                               redirect_uri=SPOTIPY_REDIRECT_URI,
                                               scope = 'playlist-modify-public'))


def get_existing_tracks(playlist_id):
    """Fetch all track IDs from a playlist."""
    track_ids = []
    try:
        results = sp.playlist_tracks(playlist_id, fields='items.track.id,total', additional_types=['track'])
        track_ids.extend([item['track']['id'] for item in results['items']])

        # If there are more than 100 tracks, fetch them in batches
        while 'next' in results and results['next']:
            results = sp.next(results)  # Fetch next batch of results
            track_ids.extend([item['track']['id'] for item in results['items']])

    except spotipy.exceptions.SpotifyException as e:
        print(f"An error occurred while fetching existing tracks: {e}")
    
    return set(track_ids)  # Using a set for faster lookups

def add_songs_to_spotify_playlist(track_names, playlist_id):
    """Adds a list of songs to a specified Spotify playlist, avoiding duplicates."""
    try:
        track_ids_to_add = []
        existing_tracks = get_existing_tracks(playlist_id)  # Fetch existing tracks in the playlist

        for track in track_names:
            results = sp.search(q=track, type='track', limit=1)
            if results['tracks']['items']:
                track_id = results['tracks']['items'][0]['id']
                # Only add the track if it's not already in the playlist
                if track_id not in existing_tracks:
                    track_ids_to_add.append(track_id)

        if track_ids_to_add:
            sp.user_playlist_add_tracks(os.getenv('username'), playlist_id, track_ids_to_add)
            print(f"Added {len(track_ids_to_add)} new tracks to the playlist.")
        else:
            print("No new tracks to add. All tracks are already in the playlist.")

    except spotipy.exceptions.SpotifyException as e:
        print(f"An error occurred while adding tracks: {e}")
