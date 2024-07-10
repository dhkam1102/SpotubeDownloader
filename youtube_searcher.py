import os
from googleapiclient.discovery import build
from dotenv import load_dotenv
load_dotenv()

YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')

def youtube_search(query, max_results=2):
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

if __name__ == "__main__":
    # Example: Search for a song
    query = "Supernatural NewJeans"
    results = youtube_search(query)
    for video in results:
        print(video)
