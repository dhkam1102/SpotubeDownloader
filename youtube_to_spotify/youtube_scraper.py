import os
from googleapiclient.discovery import build
from dotenv import load_dotenv
import re

load_dotenv()

YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')

def fetch_video_description(video_id):
    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
    response = youtube.videos().list(part="snippet", id=video_id).execute()
    
    if 'items' in response and len(response['items']) > 0:
        return response['items'][0]['snippet']['description']
    return None
def extract_song_titles(text):
    """
    Extract song titles from text (description or comment).
    Handles multiple patterns and formats.
    """
    patterns = [
        r'(\d{1,2}:\d{2}(?::\d{2})?)\s*[-–—]\s*(.+?)(?=\n\d{1,2}:\d{2}|\Z)',  # Matches '00:00 - Song Title'
        r'(\d{1,2}:\d{2}(?::\d{2})?)\s*(.+?)\s*[-–—]\s*(.+?)(?=\n\d{1,2}:\d{2}|\Z)',  # Matches '00:00 Artist - Song Title'
        r'(\d{1,2}:\d{2}(?::\d{2})?)\s*(.+?)(?=\n\d{1,2}:\d{2}|\Z)',  # Matches '00:00 Song Title'
        r'^[^:\n]+?\s*[-–—]\s*.+?(?=\n|$)',  # Fixed: Matches 'Artist - Song Title' without timestamp
        r'"(.+?)"\s*(?:by|[-–—])\s*(.+?)(?=\n|$)',  # Matches '"Song Title" by Artist'
        r'(\d{1,2}:\d{2}(?::\d{2})?)\s*[|\[]\s*(.+?)\s*[|\]]',  # Matches '00:00 | Song Title' or '00:00 [Song Title]'
        r'^\d+[.)\s]\s*(.+?)(?=\n|$)',  # Fixed: Matches '1. Song Title' or '1) Song Title'
        r'^Track\s*\d+\s*[:.-]\s*(.+?)(?=\n|$)',  # Fixed: Matches 'Track 1: Song Title'
        r'^\[(.+?)\]\s*[-–—]\s*(.+?)(?=\n|$)',  # Fixed: Matches '[Artist] - Song Title'
        r'^(.+?)\s*//\s*(.+?)(?=\n|$)',  # Fixed: Matches 'Artist // Song Title'
        r'^(.+?)\s*[:]\s*(.+?)(?=\n|$)',  # Fixed: Matches 'Artist: Song Title'
        r'^(.+?)\s*[-–—]\s*"(.+?)"(?=\n|$)',  # Fixed: Matches 'Artist - "Song Title"'
        r'^(\d{1,2}:\d{2}(?::\d{2})?)\s*(.+?)\s*[-–—]\s*(.+?)\s*[(](.+?)[)](?=\n|$)'  # Fixed: Matches '00:00 Artist - Song Title (Album)'
    ]


    song_titles = []
    for pattern in patterns:
        matches = re.finditer(pattern, text, re.MULTILINE)
        for match in matches:
            if len(match.groups()) == 4:  # Timestamp, Artist, Song title, Album
                artist = match.group(2).strip()
                song = match.group(3).strip()
                album = match.group(4).strip()
                song_titles.append(f"{artist} - {song} ({album})")
            elif len(match.groups()) == 3:  # Timestamp, Artist, and Song title
                artist = match.group(2).strip()
                song = match.group(3).strip()
                song_titles.append(f"{artist} - {song}")
            elif len(match.groups()) == 2:  # Various two-group matches
                if match.group(1).strip().replace(':', '').isdigit():  # If first group is timestamp or track number
                    song_titles.append(match.group(2).strip())
                else:  # Artist - Song Title format
                    artist = match.group(1).strip()
                    song = match.group(2).strip()
                    song_titles.append(f"{artist} - {song}")

    return list(dict.fromkeys(song_titles))  # Remove duplicates while preserving order


def fetch_video_comments(video_id):
    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
    comments = []
    request = youtube.commentThreads().list(part="snippet", videoId=video_id, maxResults=10)
    
    while request:
        response = request.execute()
        for item in response['items']:
            comment = item['snippet']['topLevelComment']['snippet']['textOriginal']
            comments.append(comment)
        request = youtube.commentThreads().list_next(request, response)
    return comments

def get_song_titles(video_id):
    description = fetch_video_description(video_id)
    comments = fetch_video_comments(video_id)
    
    description_titles = extract_song_titles(description) if description else []
    comment_titles = []
    for comment in comments:
        comment_titles.extend(extract_song_titles(comment))
    
    all_titles = description_titles + comment_titles
    return list(dict.fromkeys(all_titles))  # Remove duplicates while preserving order

# Example usage
video_id = "6_p7BEFMdFs"  # Replace with actual video ID
song_titles = get_song_titles(video_id)
for title in song_titles:
    print(title)