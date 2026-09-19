import os
import re
import asyncio
import aiohttp
import yt_dlp
import config

DOWNLOAD_DIR = config.DOWNLOAD_DIR

def extract_video_id(query: str) -> str:
    if "youtube.com" in query or "youtu.be" in query:
        pattern = r"(?:v=|\/)([0-9A-Za-z_-]{11}).*"
        match = re.search(pattern, query)
        if match:
            return match.group(1)
    return query


async def search_youtube(query: str):
    loop = asyncio.get_event_loop()
    def _search():
        ydl_opts = {
            "quiet": True,
            "skip_download": True,
            "extract_flat": True,
            "default_search": "ytsearch1",
            "noplaylist": True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch1:{query}", download=False)
            if "entries" in info and info["entries"]:
                entry = info["entries"][0]
                return {
                    "id": entry.get("id"),
                    "title": entry.get("title", "Unknown Track"),
                    "duration": int(entry.get("duration") or 0),
                    "thumbnail": entry.get("thumbnail") or f"https://img.youtube.com/vi/{entry.get('id')}/hqdefault.jpg",
                    "url": f"https://www.youtube.com/watch?v={entry.get('id')}"
                }
            return None

    return await loop.run_in_executor(None, _search)


async def download_song(link_or_id: str) -> str:
    video_id = extract_video_id(link_or_id)
    if not video_id or len(video_id) < 3:
        return None

    file_path = os.path.join(DOWNLOAD_DIR, f"{video_id}.mp3")
    if os.path.exists(file_path) and os.path.getsize(file_path) > 10000:
        return file_path

    # Try Yuki API first
    api_url = config.MEOW_API_URL
    api_key = config.MEOW_API_KEY
    if api_key and api_key != "YOUR_API_KEY":
        try:
            async with aiohttp.ClientSession() as session:
                stream_url = f"{api_url}/stream/{video_id}?key={api_key}&type=audio&quality=128"
                async with session.get(stream_url, timeout=aiohttp.ClientTimeout(total=300)) as resp:
                    if resp.status == 200:
                        with open(file_path, "wb") as f:
                            async for chunk in resp.content.iter_chunked(131072):
                                f.write(chunk)
                        if os.path.exists(file_path) and os.path.getsize(file_path) > 10000:
                            return file_path
        except Exception:
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                except Exception:
                    pass

    # Fallback to direct yt-dlp
    loop = asyncio.get_event_loop()
    def _ytdlp_download():
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": os.path.join(DOWNLOAD_DIR, f"{video_id}.%(ext)s"),
            "quiet": True,
            "no_warnings": True,
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }],
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([f"https://www.youtube.com/watch?v={video_id}"])
            if os.path.exists(file_path):
                return file_path
        return None

    try:
        return await loop.run_in_executor(None, _ytdlp_download)
    except Exception:
        return None
