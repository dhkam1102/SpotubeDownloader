
# SpotubeDownloader

## Description

There was a time when I didn't have access to Spotify, but I still wanted to listen to my favorite playlist that I had on Spotify. One solution was to search for each song on YouTube and listen to them individually. However, an even better solution is to automate this process by scraping the songs from my Spotify playlist, finding them on YouTube, downloading the tracks, and uploading them to my phone for easy offline access. SpotubeDownloader does just that, making it perfect for anyone who wants to enjoy their favorite music without being tied to Spotify!

## Features

- Scrape songs from Spotify playlists
- Search for corresponding songs on YouTube
- Retrieve and store YouTube URLs
- Download songs from YouTube
- Upload downloaded songs to your phone

## Technologies Used

- Python
- Spotify API
- YouTube API
- Web Scraping
- File Handling

## Installation

1. **Clone the repository**:
   \`\`\`bash
   git clone https://github.com/yourusername/SpotubeDownloader.git
   cd SpotubeDownloader
   \`\`\`

2. **Set up a virtual environment**:
   \`\`\`bash
   python -m venv venv
   source venv/bin/activate  # On Windows use \`venv\Scripts\activate\`
   \`\`\`

3. **Install required dependencies**:
   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`

4. **Install \`ffmpeg\`**:
   - On MacOS: \`brew install ffmpeg\`
   - On Ubuntu: \`sudo apt-get install ffmpeg\`
   - On Windows: [Download from ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH
