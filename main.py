from fastapi import FastAPI, HTTPException
import yt_dlp
import shutil
import os

app = FastAPI()

COOKIES_PATH = "/tmp/cookies.txt"
if os.path.exists("/etc/secrets/cookies.txt"):
    shutil.copy("/etc/secrets/cookies.txt", COOKIES_PATH)

@app.get("/")
def home():
    return {"status": "running"}

@app.get("/download")
def download(url: str):
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'cookiefile': COOKIES_PATH,
        'extractor_args': {
            'youtube': {
                'player_client': ['android', 'web']
            }
        }
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return {
                "title": info.get("title"),
                "video_url": info.get("url"),
                "duration": info.get("duration")
            }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
