YouTube Playlist Downloader

This Python script allows you to download songs or videos from a YouTube playlist and manage their metadata. You can choose to download either the audio (music) or video content from the playlist.

Usage

To use the script, follow these steps:

    Update the folder and youtube_list variables in the script with your desired download location and the URL of the YouTube playlist you want to download from, respectively.

    Run the script using the following command:

    python youtube_downloader.py

    The script will download the new songs or videos from the YouTube playlist that are not already present in the downloaded list.

    If chg_titles is set to "True," the metadata (title and artist) of the downloaded files will be updated.

Function Parameters

The function get_songs_Youtube takes the following parameters:

    Location_file (str): The path to the folder where the downloaded files will be saved.
    playlist_Youtube (str): The URL of the YouTube playlist to download from.
    media (str, optional): The type of media to download. Default is "music". Possible values: "music" (audio) or "video" (video).
    renew (str, optional): Whether to renew the playlist. Default is "true". Possible values: "true" or "false".
    chg_titles (str, optional): Whether to change the song/video titles. Default is "True". Possible values: "True" or "False".

Notes

    This script uses the PyTube library for downloading YouTube videos.
    If media is set to "music", the audio stream will be downloaded.
    If media is set to "video", the video stream with the highest resolution available will be downloaded.
    If renew is set to "true", only the new songs/videos in the playlist will be downloaded.
    If chg_titles is set to "True", the metadata (title and artist) of the downloaded files will be updated.

Disclaimer

Please use this script responsibly and ensure that you have the right to download and use the content from the YouTube playlist. Respect copyright laws and terms of service. The author is not responsible for any misuse or illegal actions performed using this script.
