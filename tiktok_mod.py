"""
tiktok_mod.py — TikTok Live Moderation Bot
Executes real TikTok bans/mutes via the webcast API using your session cookie.

SETUP (one-time):
  1. Open Brave Browser → go to tiktok.com → log in as Ez Myfriends
  2. Press F12 → Application tab → Cookies → https://www.tiktok.com
  3. Copy 'sessionid' and 'msToken' values and paste below
  4. Install dependency: pip install requests TikTokLive pyautogui pyperclip pynput
"""

import asyncio
import json
import os
import requests
import time
import pyperclip
from pynput import keyboard
from TikTokLive import TikTokLiveClient
from TikTokLive.events import ConnectEvent, CommentEvent

# ── Configuration ──────────────────────────────────────────────────────────
TIKTOK_USERNAME = "pcychpt"        # Streamer's @handle (who you're monitoring)
OWNER_USERNAME  = "30435351025"    # Your TikTok @handle
OWNER_NICKNAME  = "Ez Myfriends"   # Your TikTok display name
OWNER_USER_ID   = "30435351025"    # Your numeric TikTok user ID

# Paste from Brave DevTools → F12 → Application → Cookies → tiktok.com
SESSION_ID = "504c6501f3e728e51127fd1122f0e683"
MS_TOKEN   = "Zb0E5RoCxuDLDavtf69UU9adadGK6CR4wUSM6U0mXfmhd8cgqNs9LIcM8_ECwedTTiHnDWjqxCHrC76qJIgt8GHtpocRppUA-KZzOluw5AOwAJZbp4lbkkP1vD0biJrIHUhy5IySs2-Q0QUL7jbDfU8dBQ=="

# ── Persistence ────────────────────────────────────────────────────────────
MOD_FILE = os.path.join(os.path.dirname(__file__), "mod_list.json")
IMMUNE_FILE = os.path.join(os.path.dirname(__file__), "immune_list.json")

def load_lists():
    """Load superadmins, admins, and immune users from disk."""
    sups = set()
    ads = set()
    imm = set()
    
    if os.path.exists(MOD_FILE):
        try:
            with open(MOD_FILE, "r") as f:
                data = json.load(f)
                sups = set(data.get("superadmins", []))
                ads = set(data.get("admins", []))
        except Exception as e:
            print(f"⚠️ Could not load mod_list.json: {e}")
            
    if os.path.exists(IMMUNE_FILE):
        try:
            with open(IMMUNE_FILE, "r") as f:
                data = json.load(f)
                imm = set(data.get("immune_users", []))
        except Exception as e:
            print(f"⚠️ Could not load immune_list.json: {e}")
            
    return sups, ads, imm

def save_lists():
    """Save all lists to disk."""
    try:
        with open(MOD_FILE, "w") as f:
            json.dump({"superadmins": list(superadmins), "admins": list(admins)}, f, indent=2)
        with open(IMMUNE_FILE, "w") as f:
            json.dump({"immune_users": list(immune_list)}, f, indent=2)
    except Exception as e:
        print(f"⚠️ Could not save configuration lists: {e}")

# ── State ──────────────────────────────────────────────────────────────────
_loaded_sups, _loaded_admins, _loaded_immune = load_lists()
superadmins   = _loaded_sups   # Can: !ban, !unban, !mute, !unmute
admins        = _loaded_admins  # Can: !mute, !unmute only
immune_list   = _loaded_immune  # Immune to bans and mutes
ban_log       = {}     # {user_id: username}
banned_sec_uids = {}   # {user_id: sec_uid}
mute_log      = {}     # {user_id: username}
user_id_cache = {}     # {username: user_id}
sec_uid_cache = {}     # {username: sec_uid}
room_id       = None   

print(f"📂 Loaded mod list — Superadmins: {superadmins or '(none)'} | Mods: {admins or '(none)'}")
print(f"🛡️ Loaded immune list — Users: {immune_list or '(none)'}")

client = TikTokLiveClient(unique_id=TIKTOK_USERNAME)

# ── Role Checks ────────────────────────────────────────────────────────────
def check_owner(event) -> bool:
    uid  = event.user.unique_id.lower().strip()
    nick = getattr(event.user, "nickname", "").lower().strip()
    uid_num = str(getattr(event.user, "id", 0) or 0)
    return uid == OWNER_USERNAME.lower() or nick == OWNER_NICKNAME.lower() or uid_num == OWNER_USER_ID or uid_num == "30435351025" or "ez" in uid

def check_superadmin(event) -> bool:
    return check_owner(event) or event.user.unique_id.lower().strip() in superadmins

def check_admin(event) -> bool:
    return check_superadmin(event) or event.user.unique_id.lower().strip() in admins

# ── API ────────────────────────────────────────────────────────────────────
def _headers():
    return {
        "Cookie": f"sessionid={SESSION_ID}; msToken={MS_TOKEN}",
        "Referer": "https://www.tiktok.com/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    }

def ban_user(uid: str, uname: str):
    """Kick/ban a user from the live room via confirmed /room/kick/user/ endpoint."""
    if uname.lower().strip() in immune_list or uid == OWNER_USER_ID or uname.lower().strip() == OWNER_USERNAME.lower():
        print(f"🛡️ [IMMUNE BLOCK] sorry cannot mute ban vip: @{uname}")
        bot_announce(f"sorry cannot mute ban vip @{uname} 🛡️❌")
        return

    sec_uid = sec_uid_cache.get(uname.lower(), "")
    params  = {"aid": "1988", "app_language": "en", "app_name": "tiktok_web",
               "device_platform": "web_pc", "region": "TH", "msToken": MS_TOKEN}
    payload = {"room_id": room_id, "kick_uid": uid, "sec_kick_uid": sec_uid}
    try:
        r = requests.post("https://webcast.tiktok.com/webcast/room/kick/user/",
                          params=params, json=payload, headers=_headers(), timeout=10)
        data = r.json()
        if data.get("status_code") == 0:
            ban_log[uid] = uname
            banned_sec_uids[uid] = sec_uid  
            print(f"🔨 @{uname} BANNED (kicked from live)!")
        else:
            print(f"⚠️ Ban failed (status {data.get('status_code')}): {data}")
    except Exception as e:
        print(f"❌ Ban error: {e}")

def unban_user(uid: str, uname: str):
    """Unkick/unban a user — uses sec_uid stored at ban time."""
    sec_uid = banned_sec_uids.get(uid) or sec_uid_cache.get(uname.lower(), "")
    params  = {"aid": "1988", "app_language": "en", "app_name": "tiktok_web",
               "device_platform": "web_pc", "region": "TH", "msToken": MS_TOKEN}
    payload = {"room_id": room_id, "kick_uid": uid, "sec_kick_uid": sec_uid}
    try:
        r = requests.post("https://webcast.tiktok.com/webcast/room/unkick/user/",
                          params=params, data=payload, headers=_headers(), timeout=10)
        data = r.json()
        if data.get("status_code") == 0:
            ban_log.pop(uid, None)
            print(f"✅ @{uname} UNBANNED!")
        else:
            print(f"⚠️ Unban failed (status {data.get('status_code')}): {data}")
    except Exception as e:
        print(f"❌ Unban error: {e}")

def mute_user(uid: str, sec_uid: str, uname: str):
    """Silence a user in the live room via the confirmed /room/silence/ endpoint."""
    if uname.lower().strip() in immune_list or uid == OWNER_USER_ID or uname.lower().strip() == OWNER_USERNAME.lower():
        print(f"🛡️ [IMMUNE BLOCK] sorry cannot mute ban vip: @{uname}")
        bot_announce(f"sorry cannot mute ban vip @{uname} 🛡️❌")
        return

    params  = {"aid": "1988", "app_language": "en", "app_name": "tiktok_web",
               "device_platform": "web_pc", "region": "TH", "msToken": MS_TOKEN}
    payload = {"room_id": room_id, "user_id": uid,
               "sec_user_id": sec_uid, "silence_type": 0, "duration": 0}
    try:
        r = requests.post("https://webcast.tiktok.com/webcast/room/silence/",
                          params=params, json=payload, headers=_headers(), timeout=10)
        data = r.json()
        if data.get("status_code") == 0:
            mute_log[uid] = uname
            print(f"🔇 @{uname} MUTED!")
        else:
            print(f"⚠️ Mute failed (status {data.get('status_code')}): {data}")
    except Exception as e:
        print(f"❌ Mute error: {e}")

def unmute_user(uid: str, sec_uid: str, uname: str):
    """Unsilence a user via /room/unsilence/ endpoint."""
    params  = {"aid": "1988", "app_language": "en", "app_name": "tiktok_web",
               "device_platform": "web_pc", "region": "TH", "msToken": MS_TOKEN}
    payload = {"room_id": room_id, "user_id": uid, "sec_user_id": sec_uid}
    try:
        r = requests.post("https://webcast.tiktok.com/webcast/room/unsilence/",
                          params=params, json=payload, headers=_headers(), timeout=10)
        data = r.json()
        if data.get("status_code") == 0:
            mute_log.pop(uid, None)
            print(f"🔊 @{uname} UNMUTED!")
        else:
            print(f"⚠️ Unmute failed (status {data.get('status_code')}): {data}")
    except Exception as e:
        print(f"❌ Unmute error: {e}")

# ── ระบบค้นหาและเลือกหน้าต่างช่องแชท TikTok (Windows OS Sync) ─────────────────
def _find_tiktok_hwnd():
    try:
        import win32gui
        results = []
        def _cb(hwnd, _):
            if win32gui.IsWindowVisible(hwnd) and "tiktok" in win32gui.GetWindowText(hwnd).lower():
                results.append((hwnd, win32gui.GetWindowText(hwnd).lower()))
        win32gui.EnumWindows(_cb, None)
        if not results: return None
        for hwnd, title in results:
            if "brave" in title: return hwnd
        for hwnd, title in results:
            if "code" not in title and "tiktokbot" not in title: return hwnd
        return results[0][0]
    except Exception: return None

def bot_announce(text: str):
    """Focuses the TikTok browser window, clicks input, and pastes the text safely."""
    try:
        import pyautogui
        import win32gui
        import win32con
        
        pyperclip.copy(text)
        kb = keyboard.Controller()
        
        # ค้นหาและดึงสิทธิ์หน้าต่างหน้าเว็บ TikTok ขึ้นมาเป็นโฟกัสหลักก่อนส่งคำสั่งคีย์บอร์ด
        hwnd = _find_tiktok_hwnd()
        if hwnd:
            try:
                win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
                win32gui.SetForegroundWindow(hwnd)
                time.sleep(0.4)  
                
                # นำพิกัดคลิกตำแหน่งช่องแชทแบบสัมพัทธ์ (Relative Layout) มาสั่งงานเพื่อความแม่นยำ
                left, top, right, bottom = win32gui.GetWindowRect(hwnd)
                pyautogui.click(left + int((right - left) * 0.75), top + int((bottom - top) * 0.92))
                time.sleep(0.2)
            except Exception:
                pass
                
        # ส่งชุดคำสั่งกดวางข้อความลงในช่องแชทจริง
        time.sleep(0.1)
        with kb.pressed(keyboard.Key.ctrl):
            kb.tap('v')
        time.sleep(0.15)
        kb.tap(keyboard.Key.enter)
        print(f"📢 [CHAT OUT] Sent to chat: {text}")
    except Exception as e:
        print(f"⚠️ Chat shortcut injection failed: {e}")

def resolve(raw: str):
    """Return (user_id, sec_uid, username) from a @mention."""
    uname   = raw.lstrip("@").lower().strip()
    uid     = user_id_cache.get(uname)
    sec_uid = sec_uid_cache.get(uname, "")
    
    if not uid:
        uid = uname
        
    return uid, sec_uid, uname

# ── Events ─────────────────────────────────────────────────────────────────
@client.on(ConnectEvent)
async def on_connect(event: ConnectEvent):
    global room_id
    room_id = str(getattr(client, "room_id", ""))
    print(f"✅ Mod bot connected to @{event.unique_id}'s live! Room ID: {room_id}")

@client.on(CommentEvent)
async def on_comment(event: CommentEvent):
    uname   = event.user.unique_id.lower().strip()
    uid_num = str(getattr(event.user, "id", 0) or 0)
    sec_uid = str(getattr(event.user, "sec_uid", "") or "")
    
    if uname and uid_num and uid_num != "0":
        user_id_cache[uname] = uid_num
        if sec_uid:
            sec_uid_cache[uname] = sec_uid

    msg = event.comment.strip()
    msg_lower = msg.lower()

    # ── !ban @user — Superadmin+ ──────────────────────────────────────────
    if msg_lower.startswith("!ban "):
        if not check_superadmin(event):
            print(f"🚫 {event.user.unique_id} tried !ban — superadmin only.")
            return
        uid, sec_uid, uname = resolve(msg.split()[1])
        if uid: ban_user(uid, uname)

    # ── !unban @user — Superadmin+ ────────────────────────────────────────
    elif msg_lower.startswith("!unban "):
        if not check_superadmin(event):
            print(f"🚫 {event.user.unique_id} tried !unban — superadmin only.")
            return
        uid, sec_uid, uname = resolve(msg.split()[1])
        if uid: unban_user(uid, uname)

    # ── !mute @user OR !timeout @user — Admin+ ────────────────────────────
    elif msg_lower.startswith("!mute ") or msg_lower.startswith("!timeout "):
        if not check_admin(event):
            print(f"🚫 {event.user.unique_id} tried !mute — admin only.")
            return
        uid, sec_uid, uname = resolve(msg.split()[1])
        if uid: mute_user(uid, sec_uid, uname)

    # ── !unmute @user — Admin+ ────────────────────────────────────────────
    elif msg_lower.startswith("!unmute "):
        if not check_admin(event):
            print(f"🚫 {event.user.unique_id} tried !unmute — admin only.")
            return
        uid, sec_uid, uname = resolve(msg.split()[1])
        if uid and uid != uname: unmute_user(uid, sec_uid, uname)

    # ── !immune @user — Owner Only ─────────────────────────────────────────
    elif msg_lower.startswith("!immune "):
        if not check_owner(event):
            print(f"🚫 Refused !immune command from unauthorized user: @{event.user.unique_id}")
            return
        target = msg.split()[1].lstrip("@").lower().strip()
        immune_list.add(target)
        save_lists()
        print(f"🛡️ [IMMUNE ADDED] @{target} is now granted permanent immunity!")

    # ── !removeimmune @user — Owner Only ───────────────────────────────────
    elif msg_lower.startswith("!removeimmune "):
        if not check_owner(event):
            print(f"🚫 Refused !removeimmune from unauthorized user: @{event.user.unique_id}")
            return
        target = msg.split()[1].lstrip("@").lower().strip()
        immune_list.discard(target)
        save_lists()
        print(f"🗑️ [IMMUNE REMOVED] Permanent immunity revoked from @{target}")

    # ── !addsup @user — Owner only ─────────────────────────────────────────
    elif msg_lower.startswith("!addsup "):
        if not check_owner(event):
            print(f"🚫 {event.user.unique_id} tried !addsup — owner only.")
            return
        target = msg.split()[1].lstrip("@").lower().strip()
        superadmins.add(target)
        save_lists()
        print(f"⭐ @{target} is now SUPERADMIN. Current List: {list(superadmins)}")

    # ── !removesup @user — Owner only ──────────────────────────────────────
    elif msg_lower.startswith("!removesup "):
        if not check_owner(event):
            print(f"🚫 {event.user.unique_id} tried !removesup — owner only.")
            return
        target = msg.split()[1].lstrip("@").lower().strip()
        superadmins.discard(target)
        save_lists()
        print(f"🗑️ @{target} removed from superadmins.")

    # ── !addmod @user — Owner only ─────────────────────────────────────────
    elif msg_lower.startswith("!addmod "):
        if not check_owner(event):
            print(f"🚫 {event.user.unique_id} tried !addmod — owner only.")
            return
        target = msg.split()[1].lstrip("@").lower().strip()
        admins.add(target)
        save_lists()
        print(f"🛡️ @{target} is now MOD. Current List: {list(admins)}")

    # ── !removemod @user — Owner only ──────────────────────────────────────
    elif msg_lower.startswith("!removemod "):
        if not check_owner(event):
            print(f"🚫 {event.user.unique_id} tried !removemod — owner only.")
            return
        target = msg.split()[1].lstrip("@").lower().strip()
        admins.discard(target)
        save_lists()
        print(f"🗑️ @{target} removed from mods.")

    # ── !list ──────────────────────────────────────────────────────────────
    elif msg_lower == "!list":
        print("─── ⭐ SUPERADMINS ─────────────────────────")
        for user in superadmins:
            print(f"  ⭐ @{user}")
        if not superadmins: print("  (none)")
        print("─── 🛡️ MODS ────────────────────────────────")
        for user in admins:
            print(f"  🛡️ @{user}")
        if not admins: print("  (none)")
        print("─── 👑 IMMUNE USERS (VIP) ──────────────────")
        for user in immune_list:
            print(f"  👑 @{user}")
        if not immune_list: print("  (none)")
        print("────────────────────────────────────────────")

    # ── !banlist — Owner only ─────────────────────────────────────────────
    elif msg_lower == "!banlist":
        if not check_owner(event):
            print(f"🚫 {event.user.unique_id} tried !banlist — owner only.")
            return
        print("─── 🔨 BANNED ─────────────────────────────")
        for uid, un in ban_log.items(): print(f"  🔨 @{un}  (ID: {uid})")
        if not ban_log: print("  (empty)")
        print("─── 🔇 MUTED ──────────────────────────────")
        for uid, un in mute_log.items(): print(f"  🔇 @{un}  (ID: {uid})")
        if not mute_log: print("  (empty)")

if __name__ == "__main__":
    print("🛡️ TikTok Mod Bot starting...")
    try:
        client.run()
    except Exception as e:
        print(f"An error occurred: {e}")