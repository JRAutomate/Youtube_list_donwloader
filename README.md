# YouTube Playlist Downloader with yt-dlp

This Python script allows you to download songs or videos from a YouTube playlist using [`yt-dlp`](https://github.com/yt-dlp/yt-dlp) and optionally convert them to MP3. It also manages duplicates using a CSV file, and can randomize filenames to avoid repeated order.

## 🔧 Features

- ✅ Supports **audio (MP3)** or **video** download  
- ✅ Only downloads **new videos** not present in your existing `Urls_My_Music.csv`  
- ✅ Auto-converts downloaded `.mp4` files to `.mp3` using `ffmpeg`  
- ✅ Renames files with a random prefix (optional)  
- ✅ Compatible with any YouTube playlist  
- ✅ Now supports **command-line arguments**

---

## 📦 Requirements

- Python 3.8 or higher  
- [`yt-dlp`](https://github.com/yt-dlp/yt-dlp)  
- [`ffmpeg`](https://ffmpeg.org/) (only needed if downloading audio)

Install the required Python packages with:

```bash
pip install yt-dlp pandas
```

Also ensure that `ffmpeg` is installed and added to your system's PATH.

---

## 🚀 Usage (Command Line)

Run the script with arguments:

```bash
python youtube_downloader_ytdlp.py \
  -media music \
  -renew false \
  -randomize true \
  -folder "D:/Files/Music" \
  -playlist "https://youtube.com/playlist?list=YOUR_LIST_ID"
```

### 🎛 Available Arguments

| Argument       | Description                                                    |
|----------------|----------------------------------------------------------------|
| `-folder`      | Path to the folder where files will be saved                   |
| `-playlist`    | URL of the YouTube playlist to download                        |
| `-media`       | `"music"` for audio or `"video"` for full videos               |
| `-renew`       | `"true"` = redownload all, `"false"` = skip URLs in CSV        |
| `-randomize`   | `"true"` = rename with random prefix, `"reset"` = revert names |

---

## ⚙️ Script Behavior

- Downloads are saved in the folder defined by `-folder`.
- Already downloaded URLs are tracked in a CSV file: `Urls_My_Music.csv`.
- Only new videos not present in that CSV will be downloaded (if `-renew=false`).
- If `-media=music`, the file will be converted to `.mp3`.
- If `-randomize=true`, filenames will be renamed using a random prefix like `34_rd_YourSong.mp3`.

---

## 🧩 Function Overview (if used as a module)

```python
get_songs_ytdlp(
    Location_file: str,
    playlist_Youtube: str,
    media: str = "music",
    renew: str = "false",
    randomize: str = "false"
)
```

---

## 🛑 Disclaimer

This script is for educational and personal use only. Ensure that you have the right to download and use the content from the YouTube playlist. Respect copyright laws and YouTube's terms of service. The author is not responsible for any misuse or illegal actions performed using this script.