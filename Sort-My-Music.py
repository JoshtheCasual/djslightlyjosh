import os
import shutil
from mutagen.easyid3 import EasyID3

# Specify the source and destination directories
source_dir = r'C:\Users\joshu\Music\Library\Unsorted'
destination_dir = r'C:\Users\joshu\Music\Library'

# Create the destination directory if it doesn't exist
os.makedirs(destination_dir, exist_ok=True)

# Loop through all files in the source directory
for filename in os.listdir(source_dir):
    if filename.lower().endswith(".mp3"):
        filepath = os.path.join(source_dir, filename)
        try:
            audio = EasyID3(filepath)
            genre = audio.get("genre", ["Unknown"])[0]
            artist = audio.get("artist", ["Unknown"])[0]

            # Create subdirectories based on Genre and Artist
            genre_dir = os.path.join(destination_dir, genre)
            artist_dir = os.path.join(genre_dir, artist)
            os.makedirs(artist_dir, exist_ok=True)

            # Move the file to the appropriate directory
            new_filepath = os.path.join(artist_dir, filename)
            shutil.move(filepath, new_filepath)
            print(f"Moved {filename} to {new_filepath}")
        except Exception as e:
            print(f"Error processing {filename}: {e}")

print("Organizing complete!")
