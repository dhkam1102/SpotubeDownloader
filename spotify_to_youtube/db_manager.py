import sqlite3

def create_table():
    conn = sqlite3.connect('media_library.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS media (
                        id INTEGER PRIMARY KEY,
                        song_name TEXT,
                        youtube_url TEXT,
                        spotify_id TEXT,
                        file_path TEXT
                      )''')
    conn.commit()
    conn.close()

def insert_song(song_name, youtube_url, spotify_id, file_path):
    conn = sqlite3.connect('media_library.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO media (song_name, youtube_url, spotify_id, file_path) VALUES (?, ?, ?, ?)',
                   (song_name, youtube_url, spotify_id, file_path))
    conn.commit()
    conn.close()

def check_song_exists(song_name):
    conn = sqlite3.connect('media_library.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM media WHERE song_name = ?', (song_name,))
    song = cursor.fetchone()
    conn.close()
    return song
