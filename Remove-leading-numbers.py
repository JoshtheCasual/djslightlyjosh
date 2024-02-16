import os
from mutagen.easyid3 import EasyID3
import tkinter as tk
from tkinter.filedialog import askdirectory
import re

# Create a Tkinter root window (hidden)
root = tk.Tk()
root.withdraw()

# Specify the directory where your music files are located
music_directory = askdirectory(title="Select the directory of ")
print(f"Selected directory: {music_directory}")

# Regular expression to match artist names with leading numbers, dots, and spaces
pattern = re.compile(r"^\d+\.\s+")

# Loop through all files in the specified directory
for filename in os.listdir(music_directory):
    if filename.lower().endswith(".mp3"):
        filepath = os.path.join(music_directory, filename)
        try:
            audio = EasyID3(filepath)
            artist = audio.get("artist", ["Unknown Artist"])[0]

            # Remove leading numbers, dots, and spaces from the artist tag
            new_artist = pattern.sub("", artist)

            # Update the artist tag
            audio["artist"] = new_artist
            audio.save()

            # Remove leading numbers, dots, and spaces from the filename
            new_filename = pattern.sub("", filename)
            new_filepath = os.path.join(music_directory, new_filename)
            os.rename(filepath, new_filepath)

            print(f"Updated artist for {filename}: {new_artist}")
            print(f"Renamed file to: {new_filename}")
        except Exception as e:
            print(f"Error processing {filename}: {e}")

print("Artist tags and filenames updated successfully!")