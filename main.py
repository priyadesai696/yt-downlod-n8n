from fastapi import FastAPI, HTTPException
import yt_dlp

app = FastAPI()

@app.get("/")
def home():
    return {"status": "running"}

@app.get("/download")
def download(url: str):
    ydl_opts = {'format': 'best', 'quiet': True}
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
