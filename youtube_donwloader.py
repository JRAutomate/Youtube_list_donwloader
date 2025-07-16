import os
import subprocess
import pandas as pd
import random
import sys
from yt_dlp import YoutubeDL
import argparse

def get_songs_ytdlp(Location_file, playlist_Youtube, media="music", renew="false", randomize="false"):
    csv_path = os.path.join(Location_file, 'Urls_My_Music.csv')

    if not os.path.exists(Location_file):
        sys.exit(f"The path {Location_file} does not exist")

    existing_urls = []
    if renew.lower() == "false" and os.path.exists(csv_path):
        existing_urls = pd.read_csv(csv_path)["URL"].tolist()

    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
        'skip_download': True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        playlist_dict = ydl.extract_info(playlist_Youtube, download=False)
        all_entries = playlist_dict.get('entries', [])

    new_entries = [entry for entry in all_entries if entry['url'] not in existing_urls] if renew.lower() == "false" else all_entries

    if not new_entries:
        print(f"The playlist is already fully downloaded.")
        if randomize.lower() == "true":
            _randomize_files(Location_file, reset=False)
        elif randomize.lower() == "reset":
            _randomize_files(Location_file, reset=True)
        sys.exit()

    downloaded = []

    for entry in new_entries:
        video_url = entry['url']
        title = entry.get('title', 'Unknown').replace(' ', '_')
        output_template = os.path.join(Location_file, '%(title)s.%(ext)s')

        if media == "music":
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': output_template,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'quiet': True
            }
        else:
            ydl_opts = {
                'format': '22/18/best',
                'outtmpl': output_template,
                'quiet': True
            }

        try:
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_url])
                downloaded.append({'URL': video_url, 'Name': title, 'Artist': title})
                print(f"Downloaded: {title}")
        except Exception as e:
            print(f"Failed to download {video_url}: {e}")

    if downloaded:
        df_new = pd.DataFrame(downloaded)
        if os.path.exists(csv_path):
            df_old = pd.read_csv(csv_path)
            df_new = pd.concat([df_old, df_new])
        df_new.to_csv(csv_path, index=False)

    if randomize.lower() in ["true", "reset"]:
        _randomize_files(Location_file, reset=(randomize.lower() == "reset"))

def _randomize_files(folder, reset=False):
    files = [f for f in os.listdir(folder) if not f.endswith('.csv') and os.path.isfile(os.path.join(folder,f))]
    total = len(files)
    all_numbers = list(range(1, total + 1))
    random.shuffle(all_numbers)

    for filename in files:
        full_path = os.path.join(folder, filename)
        if '_rd_' not in filename:
            new_filename = f"{all_numbers.pop()}_rd_{filename}"
        else:
            base = filename.split('_rd_')[1]
            new_filename = f"{all_numbers.pop()}_rd_{base}" if not reset else base
        os.rename(full_path, os.path.join(folder, new_filename))
    print("Randomization done.")

# === Example Usage ===

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="🎵 YouTube Playlist Downloader using yt-dlp")

    parser.add_argument("-folder", required=True, help="Path to the folder where files will be saved")
    parser.add_argument("-playlist", required=True, help="YouTube playlist URL")
    parser.add_argument("-media", choices=["music", "video"], default="music", help="Download mode: music (audio) or video")
    parser.add_argument("-renew", choices=["true", "false"], default="false", help="Whether to redownload even if already saved in CSV")
    parser.add_argument("-randomize", choices=["true", "false", "reset"], default="false", help="Rename files with random numbers or reset")

    args = parser.parse_args()

    get_songs_ytdlp(
        Location_file=args.folder,
        playlist_Youtube=args.playlist,
        media=args.media,
        renew=args.renew,
        randomize=args.randomize
    )
