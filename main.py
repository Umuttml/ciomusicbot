from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
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
    # 1. Aşama: YouTube IP engeline takılmamak için Piped/Invidious API'den Arama Yap
    search_nodes = [
        f"https://pipedapi.kavin.rocks/search?q={q}&filter=all",
        f"https://inv.tux.pizza/api/v1/search?q={q}&type=video"
    ]
    
    video_id = None
    title = None
    artist = None
    thumbnail = None

    for node_url in search_nodes:
        try:
            res = requests.get(node_url, timeout=5)
            if res.status_code == 200:
                data = res.json()
                # Piped Formatı
                if "items" in data and len(data["items"]) > 0:
                    for item in data["items"]:
                        if item.get("type") == "stream":
                            video_id = item["url"].split("v=")[-1]
                            title = item.get("title")
                            artist = item.get("uploaderName")
                            thumbnail = item.get("thumbnail")
                            break
                # Invidious Formatı
                elif isinstance(data, list) and len(data) > 0:
                    video_id = data[0].get("videoId")
                    title = data[0].get("title")
                    artist = data[0].get("author")
                    if "videoThumbnails" in data[0] and len(data[0]["videoThumbnails"]) > 0:
                        thumbnail = data[0]["videoThumbnails"][0].get("url")
                
                if video_id:
                    break
        except Exception:
            continue

    # Eğer tünelden Video ID bulunduysa doğrudan URL'sini al
    target_url = f"https://www.youtube.com/watch?v={video_id}" if video_id else f"ytsearch1:{q}"

    # 2. Aşama: Direct MP3 Stream URL'sini Çek
    ydl_opts = {
        'format': 'ba/ba*',
        'quiet': True,
        'no_warnings': True,
        'nocheckcertificate': True,
        'geo_bypass': True,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(target_url, download=False)
            if 'entries' in info and len(info['entries']) > 0:
                info = info['entries'][0]

            return {
                "success": True,
                "title": title or info.get('title'),
                "artist": artist or info.get('uploader'),
                "thumbnail": thumbnail or info.get('thumbnail'),
                "url": info.get('url')
            }
    except Exception as e:
        return {"success": False, "error": str(e)}

    return {"success": False, "message": "Şarkı bulunamadı"}
