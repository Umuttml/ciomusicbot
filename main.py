from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import yt_dlp

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.api_route("/", methods=["GET", "HEAD"])
def root():
    return {"status": "ok", "message": "Cio Müzik API Aktif"}

@app.get("/api/search")
def search_music(q: str):
    ydl_opts = {
        'format': 'ba/ba*',
        'quiet': True,
        'no_warnings': True,
        'default_search': 'ytsearch1',
        'nocheckcertificate': True,
        'geo_bypass': True,
        # YouTube IP engellerini aşmak için HTTP başlıkları
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept-Language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
        }
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch1:{q}", download=False)
            
            if info and 'entries' in info and len(info['entries']) > 0:
                video = info['entries'][0]
                return {
                    "success": True,
                    "title": video.get('title'),
                    "artist": video.get('uploader'),
                    "thumbnail": video.get('thumbnail'),
                    "url": video.get('url')
                }
    except Exception as e:
        print(f"Arama hatası: {str(e)}")
        return {"success": False, "error": str(e)}
    
    return {"success": False, "message": "Şarkı bulunamadı"}
