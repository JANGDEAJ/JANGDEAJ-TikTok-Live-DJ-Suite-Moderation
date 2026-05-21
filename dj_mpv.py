"""
tiktok_dj_mpv.py — TikTok Live Headless DJ Bot
====================================================
"""
import sys
import asyncio
import os
import re
import subprocess
import traceback
from TikTokLive import TikTokLiveClient
from TikTokLive.events import ConnectEvent, CommentEvent

# Fix Windows Event Loop
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# ─── CONFIGURATION ────────────────────────────────────────────────────────────
TIKTOK_USERNAME = "pcychpt"

# Full path to mpv.exe — same folder as this script
MPV_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mpv.exe")

# Only accept real YouTube / TikTok / youtu.be URLs
VALID_URL_REGEX = re.compile(
    r'https?://(www\.)?(youtube\.com|youtu\.be|tiktok\.com|vm\.tiktok\.com|x\.com|twitter\.com|instagram\.com)',
    re.IGNORECASE
)
# Also accept plain 11-char YouTube video IDs
YOUTUBE_ID_REGEX = re.compile(r'^([a-zA-Z0-9_-]{11})$')

song_queue = []
current_process = None
is_playing     = False

client = TikTokLiveClient(unique_id=TIKTOK_USERNAME)

# ─── MPV ENGINE ───────────────────────────────────────────────────────────────
def _run_mpv(url: str):
    """Blocking call — runs mpv and waits for it to finish. Runs in a thread."""
    cmd = [
        MPV_PATH,
        "--no-video",
        "--audio-display=no",
        "--really-quiet",
        "--ytdl-format=bestaudio/best",
        url
    ]
    print(f"▶️  Running: {' '.join(cmd)}")
    proc = subprocess.Popen(cmd)
    return proc

async def play_next():
    global current_process, is_playing
    if is_playing or not song_queue:
        return
    is_playing = True
    url = song_queue.pop(0)
    print(f"🎵 Now Playing: {url}")

    try:
        if not os.path.exists(MPV_PATH):
            print(f"❌ mpv.exe not found at: {MPV_PATH}")
            return

        # Run mpv in a thread so it doesn't block the async event loop
        loop = asyncio.get_running_loop()
        current_process = await loop.run_in_executor(None, _run_mpv, url)

        # Wait for it to finish (also in thread so we don't block)
        await loop.run_in_executor(None, current_process.wait)
        print("✅ Song finished. Loading next...")

    except Exception as e:
        print(f"❌ MPV Error: {e}")
        traceback.print_exc()
    finally:
        current_process = None
        is_playing = False
        asyncio.create_task(play_next())

# ─── EVENTS ───────────────────────────────────────────────────────────────────
@client.on(ConnectEvent)
async def on_connect(event: ConnectEvent):
    print(f"✅ Connected to @{event.unique_id}!")
    print(f"🔍 MPV path: {MPV_PATH} ({'FOUND ✅' if os.path.exists(MPV_PATH) else 'NOT FOUND ❌'})")

@client.on(CommentEvent)
async def on_comment(event: CommentEvent):
    try:
        msg       = event.comment.strip()
        msg_lower = msg.lower()
        user      = event.user.unique_id

        # ─── !play ───────────────────────────────────────────────────────────
        if msg_lower.startswith("!play "):
            raw = msg.split(" ", 1)[1].strip()

            # Plain 11-char YouTube ID  →  convert to full URL
            if YOUTUBE_ID_REGEX.match(raw):
                url = f"https://www.youtube.com/watch?v={raw}"

            # Must start with http and match a known video site
            elif raw.startswith("http") and VALID_URL_REGEX.match(raw):
                url = raw

            # www.youtube.com without http
            elif VALID_URL_REGEX.match("https://" + raw):
                url = "https://" + raw

            else:
                print(f"🚫 Ignored invalid URL from {user}: '{raw[:60]}'")
                return

            song_queue.append(url)
            print(f"📋 Queued by {user}: {url}  (position {len(song_queue)})")
            if not is_playing:
                asyncio.create_task(play_next())

        # ─── !skip ───────────────────────────────────────────────────────────
        elif msg_lower == "!skip":
            if current_process:
                print(f"⏭️  {user} skipped!")
                current_process.kill()
            else:
                print(f"⏭️  {user} tried !skip but nothing is playing.")

        # ─── !stop ───────────────────────────────────────────────────────────
        elif msg_lower == "!stop":
            print(f"⏹️  {user} stopped the queue!")
            song_queue.clear()
            if current_process:
                current_process.kill()

    except Exception as e:
        print(f"⚠️ Comment Error: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    print(f"🎵 Connecting to @{TIKTOK_USERNAME}...")
    print(f"🔍 MPV path: {MPV_PATH}")
    try:
        client.run()
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        if "UserNotFound" in str(e):
            print("→  Check TIKTOK_USERNAME and make sure the stream is LIVE")
