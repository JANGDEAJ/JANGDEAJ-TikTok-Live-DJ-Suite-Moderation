## Digital Twin Bot Script Updates (Unified Configuration & Command Realignment)

The script has been refactored below to remove hardcoded user profiles and switch settings over to standard `.env` variables or system references. The command parsing mechanisms have been realigned to cleanly evaluate DJ commands (`!play`), moderation payloads (`!mute`), and state behaviors without overlapping dependencies.

Additionally, explicit headers and clean spacing rules are enforced throughout to guarantee stability inside terminal environments.

```python
"""
digital_twin_bot_gemini.py — TikTok Live AI Auto-Typer (Absolute API Nuke Edition)
================================================================================
Reads environment settings and executes asynchronous event loops for live chat tracking.
"""

import sys
import asyncio
import re
import os
import time
import logging
import pyperclip
import aiofiles
import json
import requests
import urllib.request
import urllib.parse
from openai import AsyncOpenAI
from pynput import keyboard
from TikTokLive import TikTokLiveClient
from TikTokLive.events import ConnectEvent, CommentEvent, DisconnectEvent

# Fix Windows terminal UTF-8 encoding
import io
try:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', line_buffering=True)
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', line_buffering=True)
except AttributeError:
    pass

def _load_env(path=".env"):
    try:
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ.setdefault(k.strip(), v.strip())
    except FileNotFoundError:
        pass

_load_env()

# ─── CONFIGURATION ────────────────────────────────────────────────────────────
TIKTOK_USERNAME  = os.environ.get("TIKTOK_USERNAME", "@streamer")      
OWNER_USERNAME   = os.environ.get("OWNER_USERNAME", "owner_handle")       
OWNER_NICKNAME   = os.environ.get("OWNER_NICKNAME", "owner_display")      
OWNER_USER_ID    = os.environ.get("OWNER_USER_ID", "0")       

SESSION_ID = os.environ.get("TIKTOK_SESSION_ID", "")
MS_TOKEN   = os.environ.get("TIKTOK_MS_TOKEN", "")

DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY")
DEEPSEEK_MODEL   = "deepseek-chat"  

IDENTITY_FILE    = "identity_context.
