import os
import subprocess
import csv
from pytubefix import YouTube
from pytubefix.cli import on_progress
import ffmpeg
import sys

# Ensure required folders exist
def ensure_folder_exists(path):
    """
    Ensures the specified folder exists. Creates it if it doesn't.
    """
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Folder created: {path}")
    elif not os.path.isdir(path):
        raise FileExistsError(f"A file with the same name as the folder exists: {path}")

# Set up folder paths
MP4_FOLDER = "mp4_downloads"
MP3_FOLDER = "mp3_conversions"
ensure_folder_exists(MP4_FOLDER)
ensure_folder_exists(MP3_FOLDER)

# Get the FFmpeg path
def get_ffmpeg_path():
    if getattr(sys, 'frozen', False):
        # If the script is frozen by PyInstaller
        base_path = sys._MEIPASS  # Temporary extraction folder for PyInstaller
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, 'bin', 'ffmpeg.exe')

ffmpeg_path = get_ffmpeg_path()

def download_vid(url, custom_name=None):
    """
    Downloads a video from YouTube to the MP4_FOLDER. 
    If custom_name is provided, it saves the video with that name.
    """
    error = None
    try:
        yt = YouTube(url, on_progress_callback=on_progress)
        ys = yt.streams.get_highest_resolution()
        try:
            license = yt.metadata.raw_metadata[0]["contents"][0]["runs"][0]["text"]
            if "Creative Commons Attribution license" not in license:
                error = f"\nAltert: the video {url} is not appear to be creative commons licensed, double check this video to ensure you have the proper license for this video\n"
        except:
            error = f"\nCould not fetch license for video {url}\nPlease double check license and ensure you have permission to download this video\n"
        # Use custom name if provided, otherwise use YouTube title
        file_name = custom_name if custom_name else yt.title
        file_name = file_name + ".mp4"  # Ensure file name has .mp4 extension
        file_path = os.path.join(MP4_FOLDER, file_name)
        
        ys.download(output_path=MP4_FOLDER, filename=file_name)
        print(f"Downloaded: {yt.title} to {file_path}")
    except Exception as e:
        print(f"\n    I couldn't download the video. Error: {e}\n    Are you connected to the internet?\n    If you are and it isn't working, this program may need to be updated\n")
        
    return error
        
def convert_mp4_to_mp3():
    """
    Converts all MP4 files in MP4_FOLDER to MP3 in MP3_FOLDER.
    """
    # Loop through all files in the MP4 folder
    for root, dirs, files in os.walk(MP4_FOLDER):
        for file in files:
            # Check if the file ends with .mp4
            if file.endswith(".mp4"):
                input_path = os.path.join(root, file)
                output_file_name = file.replace(".mp4", ".mp3")
                output_path = os.path.join(MP3_FOLDER, output_file_name)
                if os.path.exists(output_path):
                    print(f"Already converted: {output_file_name}, skipping.")
                    continue
                try:
                    # Convert MP4 to MP3
                    ffmpeg.input(input_path).output(output_path).run(cmd=ffmpeg_path)
                    print(f"Converted: {input_path} -> {output_path}")
                except subprocess.CalledProcessError as e:
                    print(f"Error converting {input_path}: {e}")

def process_song_list():
    """
    Processes a CSV file containing a list of songs to download and convert.
    """
    csv_file = "song_list.csv"

    # Check if the CSV file exists, if not, create it
    if not os.path.exists(csv_file):
        with open(csv_file, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Name", "URL", "Downloaded"])  # Header row
        print(f"{csv_file} created. Please add songs to it.")
        return

    # Read and process the CSV file
    updated_rows = []
    errors = []
    
    with open(csv_file, mode="r") as file:
        reader = csv.reader(file)
        header = next(reader)  # Skip the header row
        updated_rows.append(header)
        
        for row in reader:
            name, url, downloaded = row
            if downloaded.strip().lower() != "true":  # Check if not downloaded
                print(f"Downloading: {name}")
                try:
                    error = download_vid(url=url, custom_name=name)  # Download video
                    errors.append(error)
                    row[2] = "True"  # Mark as downloaded
                except subprocess.CalledProcessError as e:
                    print(f"Error downloading {name}: {e}")
            else:
                print(f"Already downloaded: {name}")
            updated_rows.append(row)

    # Write back to the CSV file
    with open(csv_file, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(updated_rows)

    # Convert all downloaded videos to MP3
    convert_mp4_to_mp3()
    
    if len(errors)>=1:
        for error in errors:
            print(error)


# Menu system
while True:
    choice = input("do what?\n 1: download vid\n 2: convert vids\n 3: Sync list\n 4: exit\nchoice: ")
    match choice:
        case "1":
            url = input("paste url: ")
            download_vid(url)
        case "2":
            convert_mp4_to_mp3()
        case "3":
            process_song_list()
        case "4":
            break
