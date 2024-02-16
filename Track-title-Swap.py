import os
from mutagen.easyid3 import EasyID3
import re
import tkinter as tk
from tkinter.filedialog import askdirectory

# Create a Tkinter root window (hidden)
root = tk.Tk()
root.withdraw()

# Set the path to the directory containing your music tracks
path = askdirectory(title="Select the directory of ")
print(f"Selected directory: {path}")

# Regular expression to match artist, title, optional mix (in parentheses), and optional BPM
pattern = re.compile(r"(.+) - (.+?)( \((.+?)\))?( \d+)?\.mp3$")

# Loop through all the music tracks in the directory
for filename in os.listdir(path):
    if filename.endswith(".mp3"):
        filepath = os.path.join(path, filename)
        audio = EasyID3(filepath)
        
        # Check if necessary tags are present; if not, create them
        if 'title' not in audio:
            audio['title'] = filename
        if 'artist' not in audio:
            audio['artist'] = 'Unknown Artist'
        
        # Extract components of the filename
        match = pattern.match(filename)
        if match:
            original_artist = match.group(1).strip()
            original_title = match.group(2).strip()
            mix = match.group(4).strip() if match.group(4) else ""
            bpm = match.group(5).strip() if match.group(5) else ""
            
            # Swap the artist and title, append mix and bpm if they exist
            new_title = f"{original_artist} ({mix})" if mix else original_artist
            new_title = f"{new_title} {bpm}".strip() if bpm else new_title.strip()
            new_artist = original_title
            
            # Log the changes to be made (for verification)
            print(f"Updating file: {filename}")
            print(f"Old title: {audio['title'][0]}, Old artist: {audio['artist'][0]}")
            print(f"New title: {new_title}, New artist: {new_artist}")
            
            # Update the metadata
            audio["title"] = new_title
            audio["artist"] = new_artist
            
            # Save the changes to the metadata
            try:
                audio.save()
                print("Metadata updated successfully.")
            except Exception as e:
                print(f"Error saving changes to file {filename}: {e}")
                
            # Create new filename and rename the file
            new_filename = f"{new_artist} - {new_title}.mp3"
            new_filepath = os.path.join(path, new_filename)
            try:
                os.rename(filepath, new_filepath)
                print(f"File renamed successfully to {new_filename}")
            except Exception as e:
                print(f"Error renaming file {filename} to {new_filename}: {e}")
        else:
            print(f"Filename pattern didn't match for file {filename}")