from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import yt_dlp

app = FastAPI()

# Frontend'inden (Vercel/GitHub Pages) gelen istekleri kabul etmek için CORS izni
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "ok", "message": "Cio Müzik API Aktif"}

@app.get("/api/search")
def search_music(q: str):
    ydl_opts = {
        'format': 'ba/ba*', # Sadece ses formatını çek
        'quiet': True,
        'no_warnings': True,
        'default_search': 'ytsearch1',
        'nocheckcertificate': True,
        'geo_bypass': True,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch1:{q}", download=False)
            if 'entries' in info and len(info['entries']) > 0:
                video = info['entries'][0]
                return {
                    "success": True,
                    "title": video.get('title'),
                    "artist": video.get('uploader'),
                    "thumbnail": video.get('thumbnail'),
                    "url": video.get('url') # Doğrudan MP3 akış URL'si
                }
    except Exception as e:
        return {"success": False, "error": str(e)}
    
    return {"success": False, "message": "Şarkı bulunamadı"}
