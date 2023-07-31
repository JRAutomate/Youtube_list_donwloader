# -*- coding: utf-8 -*-

needed_libraries=["mutagen","pytube","os","pandas","moviepy"]
for lib in needed_libraries:
    try:
    # Try to import the library
        import lib
    except ImportError:
    # If the library is not installed, install it
        try:
            import subprocess
            import sys
            subprocess.check_call([sys.executable, "-m", "pip", "install",lib])
        except Exception as e:
            print("Error installing the library:", e)

import os
import pandas as pd
import pytube as pt
from mutagen.mp3 import MP3
from mutagen.easymp4 import EasyMP4
from mutagen.id3 import ID3, TIT2, TIT3, TALB, TPE1, TRCK, TYER
from mutagen.mp4 import MP4
from mutagen.easyid3 import EasyID3

def get_songs_Youtube(Location_file, playlist_Youtube, media="music", renew="true", chg_titles="True"):
    """
    Download songs or videos from a YouTube playlist and manage metadata.

    Parameters:
        Location_file (str): The path to the folder where the downloaded files will be saved.
        playlist_Youtube (str): The URL of the YouTube playlist to download from.
        media (str, optional): The type of media to download. Default is "music".
                               Possible values: "music" (audio) or "video" (video).
        renew (str, optional): Whether to renew the playlist. Default is "true".
                               Possible values: "true" or "false".
        chg_titles (str, optional): Whether to change the song/video titles. Default is "True".
                                    Possible values: "True" or "False".

    Returns:
        None

    Notes:
        - This function uses the PyTube library for downloading YouTube videos.
        - If media is set to "music", the audio stream will be downloaded.
        - If media is set to "video", the video stream with the itag 22 will be downloaded.
        - If renew is set to "true", only the new songs/videos in the playlist will be downloaded.
        - If chg_titles is set to "True", the metadata (title and artist) of the downloaded files will be updated.

    """
    playlist_urls = pt.Playlist(playlist_Youtube)
    playlist_old = pd.read_csv(os.path.join(Location_file, 'Urls_My_Music.csv'), sep=',') if renew == "True" else None
    new_songs = [url for url in playlist_urls if url not in playlist_old['URL'].to_list()] if renew == "True" else playlist_urls

    for url in new_songs:
        yt = pt.YouTube(url)
        t = yt.streams.filter(only_audio=True).first() if media == "music" else yt.streams.get_by_itag(22)
        out_file = t.download(output_path=Location_file)
        base, ext = os.path.splitext(out_file)

        if chg_titles == "True":
            try:
                title = base.split('-')[1].split(' (')[0]
                artist = base.split('-')[0].replace(Location_file, '')
                MP4_file = EasyMP4(out_file)
                MP4_file["title"] = title
                MP4_file["artist"] = artist
                MP4_file.save()
            except IndexError:
                title = base.replace(Location_file, '')
                artist = base.replace(Location_file, '')
            except Exception as e:
                continue

            if renew == "True" and media == "music":
                playlist_old = pd.concat([playlist_old, pd.DataFrame.from_records([{'URL': url, 'Name': title, 'Artist': artist}])])

            playlist_old = playlist_old.append({'URL': url, 'Name': title, 'Artist': artist})
            print("The song {0} of {1} has been added".format(title, artist))
        print("The video {0} has been added to  {1}".format(base,Location_file))

    try:
        playlist_old.to_csv(os.path.join(Location_file, 'Urls_My_Music.csv'), header=True, index=False)
    except Exception as e:
        pass

# Example Usage
# deport_folder = 'C:/Users/Jonathan/OneDrive/Escritorio/Spnning'
# deport_list = 'https://youtube.com/playlist?list=PLtBFGcNa1-9gENyHUu_sDkZjEzurigc1Y'

programming_folder='C:/Users/Jonathan/OneDrive/Escritorio/Python'
programming_list='https://youtube.com/playlist?list=PLtBFGcNa1-9gIwBACKBzRxsGtOodZncfS'
get_songs_Youtube(Location_file=programming_folder, playlist_Youtube=programming_list, chg_titles="False", media="video", renew="False")


#########################################################################################################################################

from moviepy.editor import *

def change_mp4_to_mp3(Music_folder, Location_file):
    """
    Convert mp4 files in a folder to mp3 and update metadata (title and artist).

    Parameters:
        Music_folder (str): The path to the folder containing the mp4 files.
        Location_file (str): The path to the folder where the mp3 files will be saved.

    Returns:
        None

    Notes:
        - This function uses the moviepy.editor library for converting mp4 to mp3.
        - The title and artist metadata are extracted from the mp4 file name.
        - The mp4 files are renamed to mp3 format and saved in the Location_file folder.
        - The metadata (title and artist) of the mp3 files are updated based on the mp4 file names.
    """
    for file_mp4 in os.listdir(Music_folder):
        if '.mp4' in file_mp4:
            base, ext = os.path.splitext(file_mp4)
            mp3_file = base + '.mp3'
            os.rename(os.path.join(Music_folder, file_mp4), os.path.join(Location_file, mp3_file))
            mp3_song = MP3(os.path.join(Location_file, mp3_file))
            try:
                title = base.split('-')[1].split(' (')[0]
                artist = base.split('-')[0].replace(Location_file + '\\', '')
            except IndexError:
                title = 'u' + base.replace(Location_file + '\\', '')
                artist = 'u' + base.replace(Location_file + '\\', '')
            mp3_song["title"] = title
            mp3_song["artist"] = artist
            mp3_song.save()

