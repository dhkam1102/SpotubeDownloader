import os
from googleapiclient.discovery import build
from dotenv import load_dotenv
load_dotenv()

YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')

def youtube_search(query, max_results = 1):
    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

    search_response = youtube.search().list(
        q=query,
        part='snippet',
        maxResults=max_results
    ).execute()

    videos = []
    for search_result in search_response.get('items', []):
        if search_result['id']['kind'] == 'youtube#video':
            video_url = f"https://www.youtube.com/watch?v={search_result['id']['videoId']}"
            video_title = search_result['snippet']['title']
            videos.append(f"Title: {video_title}, URL: {video_url}")

            with open('youtube_urls.txt', 'w') as file:
                file.write(video_url + '\n')

    return videos

if __name__ == "__main__":
    # Example: Search for a song
    query = "Supernatural NewJeans"
    results = youtube_search(query)
    for video in results:
        print(video)
