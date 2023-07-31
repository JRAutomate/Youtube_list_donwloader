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

from mutagen.mp3 import MP3  
from mutagen.easymp4 import EasyMP4
import mutagen
from mutagen.id3 import ID3, TIT2, TIT3, TALB, TPE1, TRCK, TYER 
from mutagen.mp4 import MP4
from mutagen.easyid3 import EasyID3
import os
import pandas as pd
try:
    import pytube as pt
except:
    print("not possible to import")
def get_songs_Youtube(Location_file,playlist_Youtube,media="music",renew="true"):
    playlist_urls=pt.Playlist(playlist_Youtube)
    playlist_old=pd.read_csv(Location_file+'\\'+'Urls_My_Music.csv', sep=',') if renew=="True" else None
    new_songs=[url for url in playlist_urls if  url not in playlist_old['URL'].to_list()] if renew=="True" else playlist_urls
    for url in new_songs:
        yt=pt.YouTube(url)
        t=yt.streams.filter(only_audio=True).first() if media=="music" else yt.streams.filter(res="720",acodec="mp4a.40.2",type="video")
        out_file=t.download(output_path=Location_file+'\\')
        base, ext = os.path.splitext(out_file)
        try:
            title=base.split('-')[1].split(' (')[0]
            artist=base.split('-')[0].replace(Location_file+'\\','')
            MP4_file=EasyMP4(out_file)
            MP4_file["title"]=title
            MP4_file["artist"]=artist
            MP4_file.save()
        except IndexError:
            title=base.replace(Location_file+'\\','')
            artist=base.replace(Location_file+'\\','')
        except:
            continue
        playlist_old=pd.concat([playlist_old, pd.DataFrame.from_records([{'URL':url,'Name':title,'Artist':artist}])])
        print("The song {0} of {1} has been added".format(title,artist))
    playlist_old.to_csv(Location_file+'\\'+'Urls_My_Music.csv',header=True,index=False)

Music_folder='D:\\Users\Jonathan\Music\Playlist_My_music'
my_playlist='https://www.youtube.com/playlist?list=PLtBFGcNa1-9i8A6YpNXuHfZ4M1yfTYsER'
un_verano_sin_ti='https://www.youtube.com/watch?v=wAjHQXrIj9o&list=PLRW7iEDD9RDStpKHAckdbGs3xaCChAL7Z'
get_songs_Youtube(Music_folder,un_verano_sin_ti)
from moviepy.editor import *
for file_mp4 in os.listdir(Music_folder):
    if '.mp4' in file_mp4:
        base, ext=os.path.splitext(file_mp4)
        mp3_file=base+'.mp3'
        os.rename(file_mp4,mp3_file)
        mp3_song=MP3(mp3_file)
        try:
            title=base.split('-')[1].split(' (')[0]
            artist=base.split('-')[0].replace(Location_file+'\\','')
        except IndexError:
            title='u'+base.replace(Location_file+'\\','')
            artist='u'+base.replace(Location_file+'\\','')
        mp3_song["title"]=title
        mp3_song["artist"]=artist
        mp3_song.save()

playlist_old=pd.read_csv(Music_folder+'\\'+'Urls_My_Music.csv', sep=',')