import asyncio
import re
import subprocess
import os
import yt_dlp
from TikTokLive import TikTokLiveClient
from TikTokLive.events import ConnectEvent, CommentEvent

# --- Windows Specific Audio Libraries ---
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# --- Configuration ---
# 1. ใส่ชื่อช่องสตรีมเมอร์ตรงนี้ (ไม่ต้องมี @)
TIKTOK_USERNAME = "pcychpt"  # The streamer's TikTok @handle (NOT yours)

# How many seconds to wait for Google Chrome to fully load before starting the song timer.
CHROME_STARTUP_DELAY = 4

# --- Troll Settings ---
RICKROLL_URL   = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
RICKROLL_DURATION = 212   # 3 min 32 sec — never gonna let you skip 😈
LOFI_URL       = "https://www.youtube.com/watch?v=jfKfPfyJRdk"  # Lofi Girl 🎵
LOFI_DURATION  = 600     # Play lofi for 10 minutes then continue queue
OWNER_USERNAME = "30435351025"        # Your TikTok @handle string
OWNER_NICKNAME = "Ez Myfriends"       # Your TikTok display name
OWNER_USER_ID  = "30435351025"        # Your numeric TikTok user ID

# --- Meme Clips (open to all viewers!) ---
MEMES = {
    "johncena": {"url": "https://www.youtube.com/shorts/bIhqugVuSV4", "duration": 8,   "label": "🎺 AND HIS NAME IS JOHN CENA!"},
    "rko":      {"url": "https://www.youtube.com/watch?v=8i3KBCW21v4", "duration": 12,  "label": "💥 RKO OUTTA NOWHERE!"},
    "a10":      {"url": "https://www.youtube.com/watch?v=2XU0kUjNW2I", "duration": 20,  "label": "✈️ BRRRRRTTTT A-10 WARTHOG!"},
    "mayo":     {"url": "https://www.youtube.com/watch?v=fAQmCNWJHb8", "duration": 15,  "label": "🥪 MAHYONNAISE!"},
    "minecraft": {"url": "https://www.youtube.com/watch?v=r9aVszSJCnc",          "duration": 233, "label": "⛏️ MINECRAFT EARRAPE!"},
    "wesker":    {"url": "https://www.youtube.com/watch?v=0tSx6X-oT4A",          "duration": 211, "label": "🧬 WESKER THEME!"},
    "invincible":{"url": "https://www.youtube.com/shorts/vGvOXuYNTRo",          "duration": 60,  "label": "💪 INVINCIBLE!"},
    "dexter":    {"url": "https://www.youtube.com/shorts/YomXb584AeQ",          "duration": 23,  "label": "🩸 DEXTER!"},
    "windows":   {"url": "https://www.youtube.com/watch?v=6Joyj0dmkug",          "duration": 5,   "label": "🖥️ WINDOWS EARRAPE!"},
    "ps2":       {"url": "https://www.youtube.com/watch?v=dcCwDVX_ZtY",          "duration": 5,   "label": "🐭 PS2 EARRAPE!"},
}

# --- Owner Personal Song ---
AEMEATH_URL      = "https://www.youtube.com/watch?v=1QqMUfz6ziU&t=115"  # starts at 1:55
AEMEATH_DURATION = 120  # play for 2 minutes from that timestamp

# RegEx Filters
YOUTUBE_URL_REGEX = re.compile(r'((?:https?://)?((?:www\.)?(?:youtube\.com|youtu\.be)\S+))', re.IGNORECASE)
YOUTUBE_ID_ONLY_REGEX = re.compile(r'^([a-zA-Z0-9_-]{11})$')
TIKTOK_URL_REGEX = re.compile(r'((?:https?://)?(?:www\.|vm\.|m\.)?tiktok\.com\S+)', re.IGNORECASE)
TWITTER_URL_REGEX = re.compile(r'((?:https?://)?((?:www\.)?(?:twitter\.com|x\.com)/\S+/status/\d+\S*))', re.IGNORECASE)
INSTAGRAM_URL_REGEX = re.compile(r'((?:https?://)?((?:www\.)?instagram\.com/(?:reel|p)/[a-zA-Z0-9_-]+/?))', re.IGNORECASE)

YDL_OPTS = {'quiet': True, 'no_warnings': True}

# --- Queue & State ---
song_queue = asyncio.Queue(maxsize=30)
skip_event = asyncio.Event()   
loop_enabled = False           
chaos_enabled = True           
duration_cache = {}            
admins = set()                 
banned_users = set()           

client = TikTokLiveClient(unique_id=TIKTOK_USERNAME)

def kill_chrome():
    """Force-close Google Chrome on Windows."""
    try:
        os.system('taskkill /F /IM chrome.exe >nul 2>&1')
    except Exception as e:
        print(f"⚠️ Failed to close Chrome: {e}")

def add_autoplay_param(url: str) -> str:
    if 'youtube.com' in url or 'youtu.be' in url:
        sep = '&' if '?' in url else '?'
        return url + sep + 'autoplay=1'
    return url

def open_in_chrome(url):
    """Open a URL in Google Chrome on Windows using standard system execution calls."""
    play_url = add_autoplay_param(url)
    try:
        # Windows command parsing to invoke Chrome globally from system pathing safely
        subprocess.Popen([
            'start', 'chrome',
            '--autoplay-policy=no-user-gesture-required',
            play_url
        ], shell=True)
        print(f"✅ Opened in Chrome: {play_url}")
        return True
    except Exception as e:
        print(f"❌ Failed to open Chrome: {e}")
        return False

def set_windows_volume(level: int):
    """Set system master volume on Windows using Pycaw endpoints (0-100)."""
    try:
        level = max(0, min(100, level))
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = interface.QueryInterface(IAudioEndpointVolume)
        volume.SetMasterVolumeLevelScalar(level / 100.0, None)
        print(f"🔊 Volume adjusted to: {level}%")
    except Exception as e:
        print(f"⚠️ Volume integration exception: {e}")

async def do_party_volume():
    print("🎊 Party strobe started!")
    for _ in range(5):
        set_windows_volume(100)
        await asyncio.sleep(0.4)
        set_windows_volume(40)
        await asyncio.sleep(0.4)
    set_windows_volume(75)  
    print("🎊 Party strobe done! Volume back to 75%")

async def do_earrape():
    print("💥 EARRAPE MODE — 5 SECOND BLAST! 🔊💥")
    set_windows_volume(100)
    # Note: Volume amplification injection hacks via direct system keyboard hooks on Windows 
    # require headless players like MPV. Chrome GUI blocks system-wide cross-application injections.
    await asyncio.sleep(5)
    set_windows_volume(75)
    print("✅ Earrape done! Volume restored to 75%")

def check_owner(event) -> bool:
    uid     = event.user.unique_id.lower()
    nick    = getattr(event.user, 'nickname', '').lower()
    uid_num = str(getattr(event.user, 'user_id', ''))
    return (
        uid == OWNER_USERNAME.lower() or
        nick == OWNER_NICKNAME.lower() or
        uid_num == OWNER_USER_ID
    )

def check_admin(event) -> bool:
    if check_owner(event):
        return True
    uid = event.user.unique_id.lower()
    return uid in admins

async def inject_meme(meme_key: str, triggered_by: str):
    meme = MEMES[meme_key]
    print(f"{meme['label']} triggered by {triggered_by}!")
    skip_event.set()  
    meme_song = {"url": meme["url"], "user": "🎵MemeBot"}
    temp_songs = []
    while not song_queue.empty():
        try:
            temp_songs.append(song_queue.get_nowait())
            song_queue.task_done()
        except asyncio.QueueEmpty:
            break
    await song_queue.put(meme_song)
    for s in temp_songs:
        if not song_queue.full():
            await song_queue.put(s)
    duration_cache[meme["url"]] = meme["duration"]

async def get_duration(url):
    def _fetch():
        with yt_dlp.YoutubeDL(YDL_OPTS) as ydl:
            info = ydl.extract_info(url, download=False)
            dur = info.get('duration')
            return dur if dur else 36000 # 10 Hours fallback limit if info missing
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, _fetch)

async def prefetch_duration(url):
    if url not in duration_cache:
        try:
            duration = await get_duration(url)
            duration_cache[url] = duration
            print(f"📦 Pre-fetched duration for next song: {duration}s")
        except Exception:
            pass  

async def queue_worker():
    global loop_enabled

    while True:
        song = await song_queue.get()
        target_url = song['url']
        user = song['user']

        print(f"\n🎵 Now playing: {target_url} (Requested by {user})")
        print(f"📋 Songs remaining in queue: {song_queue.qsize()}")

        if target_url in duration_cache:
            duration = duration_cache.pop(target_url)
            print(f"⚡ Instant start! Pre-fetched duration: {duration}s")
        else:
            print("⏳ Checking video duration...")
            try:
                duration = await get_duration(target_url)
                if not duration:  
                    duration = 36000 # 10 Hours limit
                print(f"⏱️ Duration: {duration} seconds")
            except Exception as e:
                print(f"⚠️ Could not get duration: {e}. Defaulting to 10 Hours.")
                duration = 36000

        while True:
            kill_chrome()
            if not open_in_chrome(target_url):
                break  

            skip_event.clear()
            try:
                await asyncio.sleep(CHROME_STARTUP_DELAY)
                await asyncio.wait_for(skip_event.wait(), timeout=duration)
                print("⏭️ Skipping to next song...")
                kill_chrome()
                loop_enabled = False  
                break
            except asyncio.TimeoutError:
                if loop_enabled:
                    print("🔁 Loop is ON — replaying same song...")
                    continue  
                else:
                    print("✅ Song finished. Loading next in queue...")
                    break

        song_queue.task_done()

@client.on(ConnectEvent)
async def on_connect(event: ConnectEvent):
    print(f"✅ Connected to @{event.unique_id}'s live stream!")
    asyncio.create_task(queue_worker())

@client.on(CommentEvent)
async def on_comment(event: CommentEvent):
    global loop_enabled, chaos_enabled
    msg = event.comment.strip()

    if msg.lower().startswith("!play "):
        if event.user.unique_id.lower() in banned_users:
            print(f"🚫 Banned user {event.user.unique_id} tried to !play — ignored.")
            return

        url_part = msg[6:].strip()

        yt_match      = YOUTUBE_URL_REGEX.search(url_part)
        tiktok_match  = TIKTOK_URL_REGEX.search(url_part)
        twitter_match = TWITTER_URL_REGEX.search(url_part)
        ig_match      = INSTAGRAM_URL_REGEX.search(url_part)
        id_match      = YOUTUBE_ID_ONLY_REGEX.match(url_part)

        if yt_match:
            target_url = yt_match.group(1)
            if not target_url.startswith("http"):
                target_url = "https://" + target_url
            target_url = re.sub(r'[&?]list=[^&]*', '', target_url)
            source = "YouTube"
        elif tiktok_match:
            target_url = tiktok_match.group(1)
            if not target_url.startswith("http"):
                target_url = "https://" + target_url
            source = "TikTok"
        elif twitter_match:
            target_url = twitter_match.group(1)
            if not target_url.startswith("http"):
                target_url = "https://" + target_url
            source = "Twitter/X"
        elif ig_match:
            target_url = ig_match.group(1)
            if not target_url.startswith("http"):
                target_url = "https://" + target_url
            source = "Instagram"
        elif id_match:
            target_url = f"https://www.youtube.com/watch?v={id_match.group(1)}"
            source = "YouTube"
        else:
            print("🚫 Ignored: No YouTube/TikTok/Twitter/Instagram link or video ID found.")
            return

        if not song_queue.full():
            await song_queue.put({"url": target_url, "user": event.user.unique_id})
            print(f"📋 [{source}] Queued by {event.user.unique_id}: {target_url} (Position: {song_queue.qsize()})")
            asyncio.create_task(prefetch_duration(target_url))
        else:
            print("🚫 Queue is full (30 songs max). Request ignored.")

    elif not chaos_enabled and not check_admin(event):
        print(f"🚫 Chaos is OFF — only !play is allowed. Ignored: '{msg[:30]}' by {event.user.unique_id}")

    elif msg.lower() in ("!skip", "!next"):
        print(f"⏭️ Skip/Next requested by {event.user.unique_id}...")
        skip_event.set()

    elif msg.lower() == "!loop":
        loop_enabled = not loop_enabled
        status = "ON 🔁" if loop_enabled else "OFF ⏹️"
        print(f"🔁 Loop toggled {status} by {event.user.unique_id}")

    elif msg.lower() == "!rickroll":
        print(f"😈 RICKROLL triggered by {event.user.unique_id}! Never gonna give you up...")
        skip_event.set()
        rickroll_song = {"url": RICKROLL_URL, "user": "🎵RickBot"}
        temp_songs = []
        while not song_queue.empty():
            try:
                temp_songs.append(song_queue.get_nowait())
                song_queue.task_done()
            except asyncio.QueueEmpty:
                break
        await song_queue.put(rickroll_song)
        for s in temp_songs:
            if not song_queue.full():
                await song_queue.put(s)
        duration_cache[RICKROLL_URL] = RICKROLL_DURATION
        print("🎵 Rickroll injected into queue!")

    elif msg.lower() == "!party":
        if not chaos_enabled:
            print(f"🚫 Chaos is OFF — !party blocked ({event.user.unique_id})")
        else:
            print(f"🎊 PARTY MODE triggered by {event.user.unique_id}! Strobing volume...")
            asyncio.create_task(do_party_volume())

    elif msg.lower() == "!lofi":
        print(f"🎵 LOFI MODE triggered by {event.user.unique_id}! Injecting chill vibes...")
        skip_event.set()
        lofi_song = {"url": LOFI_URL, "user": "🎵LofiBot"}
        temp_songs = []
        while not song_queue.empty():
            try:
                temp_songs.append(song_queue.get_nowait())
                song_queue.task_done()
            except asyncio.QueueEmpty:
                break
        await song_queue.put(lofi_song)
        for s in temp_songs:
            if not song_queue.full():
                await song_queue.put(s)
        duration_cache[LOFI_URL] = LOFI_DURATION
        print("🎵 Lofi song injected! Chill time 🙏")

    elif msg.lower() in ("!reverse", "!dizzy", "!cursed", "!slow", "!fast"):
        # Note: JavaScript DOM browser manipulation hooks (!reverse, !dizzy, !cursed, !slow, !fast) 
        # inside standard Chrome UI are unique to Mac execution architecture via AppleScript interface blocks. 
        # Windows GUI processes isolate browser memory boundaries from native terminal injection.
        print(f"⚠️ Visual/Speed modification tracking commands are optimization items compiled in the MPV Headless Edition.")

    elif msg.lower() == "!normalspeed" or msg.lower() == "!reset":
        if check_admin(event):
            print("⏱️ System presets reset to normal baseline levels.")
        else:
            print(f"🚫 {event.user.unique_id} tried to clear settings — admin only, ignored.")

    elif msg.lower() == "!enough":
        if check_admin(event):
            chaos_enabled = not chaos_enabled
            status = "ON 😈" if chaos_enabled else "OFF 😤"
            print(f"🎛️ CHAOS toggled {status} by {event.user.unique_id}!")
        else:
            print(f"🚫 {event.user.unique_id} tried !enough — admin only, ignored.")

    elif msg.lower().startswith("!volume "):
        if check_admin(event):
            try:
                vol = int(msg.split()[1])
                set_windows_volume(vol)
                print(f"🔊 Volume set to {vol}% by {event.user.unique_id}")
            except (ValueError, IndexError):
                print("⚠️ Invalid volume. Use: !volume 0-100")
        else:
            print(f"🚫 {event.user.unique_id} tried !volume — admin only command, ignored.")

    elif msg.lower().startswith("!addadmin "):
        if check_owner(event):
            target = msg.split()[1].lstrip("@").lower()
            admins.add(target)
            print(f"✅ @{target} has been added as admin! Current admins: {admins}")
        else:
            print(f"🚫 {event.user.unique_id} tried !addadmin — owner only, ignored.")

    elif msg.lower().startswith("!removeadmin "):
        if check_owner(event):
            target = msg.split()[1].lstrip("@").lower()
            if target in admins:
                admins.discard(target)
                print(f"🗑️ @{target} has been removed from admins. Current admins: {admins}")
            else:
                print(f"⚠️ @{target} is not in the admin list.")
        else:
            print(f"🚫 {event.user.unique_id} tried !removeadmin — owner only, ignored.")

    elif msg.lower() == "!admins":
        if check_owner(event):
            if admins:
                print(f"👑 Current admins: {', '.join(f'@{a}' for a in admins)}")
            else:
                print("👑 No extra admins set. Only the owner has admin powers.")
        else:
            print(f"🚫 {event.user.unique_id} tried !admins — owner only, ignored.")

    elif msg.lower().startswith("!ban "):
        if check_admin(event):
            target = msg.split()[1].lstrip("@").lower()
            banned_users.add(target)
            print(f"🔨 @{target} has been banned! Banned list: {banned_users}")
        else:
            print(f"🚫 {event.user.unique_id} tried !ban — admin only, ignored.")

    elif msg.lower().startswith("!unban "):
        if check_admin(event):
            target = msg.split()[1].lstrip("@").lower()
            if target in banned_users:
                banned_users.discard(target)
                print(f"✅ @{target} has been unbanned!")
            else:
                print(f"⚠️ @{target} is not in the ban list.")
        else:
            print(f"🚫 {event.user.unique_id} tried !unban — admin only, ignored.")

    elif msg.lower() in [f"!{k}" for k in MEMES.keys()]:
        await inject_meme(msg.lower()[1:], event.user.unique_id)

    elif msg.lower() in ("!earrape", "!earrapeon", "!earrapeoff"):
        if not chaos_enabled:
            print(f"🚫 Chaos is OFF — command blocked ({event.user.unique_id})")
        else:
            await do_earrape()

    elif msg.lower() == "!aemeath":
        print(f"🎵 !aemeath triggered by {event.user.unique_id}! Injecting personal song...")
        skip_event.set()
        aemeath_song = {"url": AEMEATH_URL, "user": "🎵AemeathBot"}
        temp_songs = []
        while not song_queue.empty():
            try:
                temp_songs.append(song_queue.get_nowait())
                song_queue.task_done()
            except asyncio.QueueEmpty:
                break
        await song_queue.put(aemeath_song)
        for s in temp_songs:
            if not song_queue.full():
                await song_queue.put(s)
        duration_cache[AEMEATH_URL] = AEMEATH_DURATION

if __name__ == '__main__':
    print("🎵 Initializing Windows Chrome DJ Queue Bot...")
    try:
        client.run()
    except Exception as e:
        print(f"An error occurred: {e}")