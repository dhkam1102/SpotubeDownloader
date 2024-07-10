import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from googleapiclient.discovery import build
import spotify_scraper  
import youtube_searcher 


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

if __name__ == "__main__":
    main()
