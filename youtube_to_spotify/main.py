from youtube_scraper import fetch_video_description, fetch_video_comments, get_song_titles, extract_song_titles
from spotify_searcher import add_songs_to_spotify_playlist
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

playlist_id = os.getenv('playlist_id')

def main():
    video_id = "C9LNocG4Z0w"  # Set this to the ID of the YouTube video you're processing

    # Step 1: Try to extract songs from the video description
    print(f"Fetching description for video ID: {video_id}")
    description = fetch_video_description(video_id)
    if description:
        print("Attempting to extract song titles from description...")
        song_titles = extract_song_titles(description)
    else:
        song_titles = []

    # Step 2: If no song titles found in description, check comments
    if not song_titles:
        print("No song titles found in description, fetching from comments...")
        comments = fetch_video_comments(video_id)
        for comment in comments:
            # Extract song titles from each comment
            song_titles.extend(extract_song_titles(comment))

    # Step 3: Add songs to Spotify Playlist if found
    if song_titles:
        print(f"Found songs: {song_titles}")
        add_songs_to_spotify_playlist(song_titles, playlist_id)
    else:
        print(f"No song titles found for video ID: {video_id}")

if __name__ == "__main__":
    main()
