## TikTok Live Cross-Platform Media Engine Suite 

Developed a high-performance, event-driven automation suite using Python asyncio that connects real-time live chat interactions with low-latency media playback loops across Windows, macOS, and Linux.

---

## Core Engineering Implementations

## Headless Architecture (mpv Backend)
Engineered a high-efficiency configuration that decouples web runtimes from asset extraction. Utilizes `yt-dlp` to extract raw audio payloads directly from edge servers, feeding streams into a detached, non-rendering `mpv` sub-process.

## 0% Desktop Input Interference
Eliminated active application window generation entirely using `CREATE_NO_WINDOW` flags on Windows and detached terminal workers on Unix systems. This completely prevents background stream processes from intercepting keyboard or mouse focus, allowing users to run frame-critical gaming inputs or development tools smoothly.

## 85% Resource Optimization
Optimized host machine performance, cutting active CPU and memory consumption by up to 85% compared to running multi-process desktop browser window instances.

## Desktop Automation (Multi-Source Chrome GUI Engine)
Implemented native operating system application hooks to drive front-end web players directly. While official platform alternatives like TikTok Live Studio restrict users to rigid, paid third-party integrations requiring premium subscriptions, this engine provides a 100% free solution capable of natively parsing and opening live-streamed Twitter, TikTok, Instagram, and YouTube source media URLs directly.

## Advanced Browser DOM Injection
Leveraged AppleScript automation via `osascript` on macOS to programmatically inject custom JavaScript payloads into the browser DOM layout, unlocking interactive real-time visual effects, speed manipulations, and software audio gain controls.

## Concurrent Event Pipeline
Built entirely on top of an asynchronous loop architecture to handle volatile incoming live socket events via `TikTokLive`, media data scraping tasks, and background player processes concurrently without blocking thread execution.

## Role-Based State Management
Maintained automated memory caching for instant asset length processing while enforcing robust state lists for role-based system permissions, cleanly segmenting Owner, Admin, and Restricted/Banned user layers.

---
## How to Install & Configure the DJ Engine

Follow these steps to deploy the script. This suite includes both a Browser Edition (for visual effects) and a Headless MPV Edition (for maximum performance).

---

## 1. Choose Your Edition & Prerequisites

## Browser Edition (Google Chrome)
Ensure Google Chrome is installed.
* **Performance Optimization Tip:** For users running older devices who cannot install heavier alternative browsers like Brave, you can simply use standard Google Chrome equipped with an ad-blocker extension. This replicates the ad-blocking protocol advantages natively.

## Headless MPV Edition (Recommended)
* **Windows:** Download the compiled `mpv.exe` binary. For the simplest configuration, place the `mpv.exe` file directly into your project's root folder.
* **macOS / Linux:** Install `mpv` globally via your system's native package manager:
    * **Mac (Homebrew):** `brew install mpv`
    * **Linux (Debian/Ubuntu/Pop!_OS):** `sudo apt install mpv`

---

## 2. Managing Custom Application Paths

If your system uses a non-standard installation path for Google Chrome or `mpv`, you can update the location directly within the script config blocks.

## Modifying the Chrome Binary Path (Mac/Windows)
Locate the environment variables at the top of your script and update the string value to match your custom folder path:
```python

# Example: Adjusting a custom Google Chrome location on macOS
CHROME_PATH = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

Modifying the MPV Binary Path (Windows)
If you do not want to keep mpv.exe in the project root folder, update the execution array with your absolute system path:
# Change "mpv.exe" to your custom absolute location
cmd = ["C:\\CustomFolder\\mpv.exe", url, "--no-video"]

3. Critical Operating System Differences ExplainedWhen deploying the suite, keep these core architectural differences in mind:Feature / BehaviorWindows & Linux (dj_windows_linux.py)macOS (dj_queue_mac.py)Global PathingWindows relies on portable binary files or localized path strings. Linux tracks binaries globally out of the box once installed via apt.macOS tracks binaries globally automatically once installed via Homebrew (brew).Automation LimitsVisual DOM manipulations (!reverse, !dizzy, !cursed) inside standard Chrome GUI windows are restricted on Windows due to OS sandbox security boundaries.Uses native AppleScript (osascript) to directly bypass Chrome's interface barriers, unlocking front-end visual manipulation commands.Audio PipelinesWindows utilizes pycaw to tap into the Win32 Core Audio endpoints. Linux maps directly to ALSA (amixer) systems.Connects to hardware volume channels natively using core macOS AppleScript volume sliders.

4. Run the Engine
Install the standard base packages and execute your chosen script file:

Bash
# Install base requirements
pip install TikTokLive yt-dlp

# Windows-only audio requirements (For Chrome/MPV Windows)
pip install pycaw comtypes
Launch the code via your terminal instance:

Bash
python dj_windows_linux.py      # For Windows/Linux Environments
python3 dj_queue_mac.py         # For macOS Environments
How to Configure the Bot for Moderation
To make sure the bot correctly recognizes who has Owner or Admin privileges, anyone hosting the bot must update the config variables right at the top of the file before launching it.

Step-by-Step Setup
Open your script (.py) file in any text editor.

Locate the # --- Configuration --- and # --- Troll Settings --- blocks.

Update these lines with the correct account details:

Python
# 1. The target live channel you want the bot to join and monitor
TIKTOK_USERNAME = "streamer_username_here"  # Do not include the '@' symbol

# 2. Your personal TikTok credentials (The person hosting/running the bot)
OWNER_USERNAME = "your_tiktok_handle"  # Your exact TikTok @username string
OWNER_NICKNAME = "your_display_name"   # Your exact TikTok profile display name
OWNER_USER_ID  = "1234567890123456"    # Your numeric TikTok user ID
How to find your numeric User ID
Go to a TikTok ID lookup tool online, or view your profile link on a desktop browser to extract your unique numerical string. This ensures the bot recognizes you even if you change your profile nickname!

The Complete DJ Suite Command Matrix
Here is how the permissions are split among viewers, administrators, and the bot owner:

1. Viewer Commands (Open to Everyone)
These commands allow the audience to interact with the media player directly, as long as they are not on the banned list.

!play <link / video ID>
Queues a track from YouTube, YouTube Shorts, TikTok, Twitter/X, or Instagram.

Example: !play https://www.youtube.com/watch?v=dQw4w9WgXcQ or !play dQw4w9WgXcQ

!skip or !next
Immediately cuts the currently playing media asset and advances to the next item waiting in the queue pipeline.

!loop
Toggles repeating the current track indefinitely. Typing it again turns looping off.

!rickroll
Injects a priority Rickroll track straight to position zero of the queue, cuts the active video, and safely pushes all other viewer requests back by one slot.

!lofi
Clears the active playback to instantly inject a 10-minute Lofi study mix, reserving the existing queue to resume right afterward.

!aemeath
Injects a curated personal theme track preset that forces the playback engine to jump straight to the custom timestamp 1:55 dynamically.

!party
Triggers a 5-second party strobe effect that flashes the host machine's system volume rapidly between 40% and 100%.

Meme Overrides
Typing any of these shortcuts skips the active track to instantly blast a short, loud soundbite before returning to the normal queue:
!johncena, !rko, !a10, !mayo, !minecraft, !wesker, !invincible, !dexter, !windows, !ps2

2. Admin & Moderator Commands
These commands bypass restrictions (such as when Chaos mode is turned off) and allow trusted moderators to control the environment.

!ban <@username>
Blacklists a specific chatter. The bot will completely ignore any future !play requests from them.

!unban <@username>
Removes a chatter from the blacklist, restoring their ability to request music.

!enough
The Chaos Toggle. Turning this OFF completely freezes all viewer commands (!party, !slow, !fast, memes, etc.), allowing only standard !play requests to go through. Only Admins can bypass this freeze.

!volume <0-100>
Directly changes the host machine’s core system master volume.

Example: !volume 50 sets the computer to 50% volume.

!reset or !normalspeed
Instantly clears any active playback audio filters, resets playback speeds back to a flat 1.0x, and brings audio levels back to default baselines safely.

3. Owner-Only Commands (The Bot Host)
These commands can only be issued by the person explicitly running the script to manage who has moderator access to the bot.

!addadmin <@username>
Appends a trusted live viewer to the bot's dynamic runtime memory list, giving them full access to all Admin/Moderator commands.

!removeadmin <@username>
Revokes administrative control from a user, dropping them back down to standard viewer permissions.

!admins
Prints a clean layout of all currently designated channel administrators directly into your local terminal console window for easy monitoring.

## Advanced Moderation & AI Chatbot Architecture

The moderation suite operates using a highly efficient **Twin-Bot Architecture**. Instead of cramming all chat, API, and logic features into one massive, slow script, the system splits responsibilities between two distinct Python files: the Chat Bot (`bot.py`) and the Moderation Engine (`mod.py`). 

These two scripts run simultaneously and communicate seamlessly by reading and writing to shared JSON configuration files, ensuring role permissions and settings are synchronized in real-time.

---

## Core Features & Interaction Pipeline

## 1. Automated Spam Detection & Interactive Warnings
The bot continuously scans incoming WebSocket chat packets for repetitive text, restricted words, or malicious link spam. When a violation is detected, the AI bot actively posts a warning message directly into the live TikTok chat to deter the user before escalating to a mute or ban.

## 2. AI-Powered !nuke Command
For severe chat raids, authorized administrators can trigger the `!nuke` command. The AI instantly analyzes the surrounding chat context to identify malicious actors participating in the raid and executes a mass-muting payload through the moderation engine, instantly cleaning the stream.

## 3. Dynamic Immunity Lists
To prevent automated moderation from accidentally silencing the wrong people, the JSON permission structure enforces a strict immunity list. VIPs, the broadcaster, and registered administrators are shielded from automated spam detection filters and mass-nuke commands.

## 4. Shared JSON State Management
Both the AI chat listener and the active moderation script share a localized JSON database. If an admin uses `!addadmin` in the chat, `bot.py` updates the JSON file. A millisecond later, `mod.py` reads that updated file and instantly grants the new admin the authority to execute mute and ban payloads.

---

## How the Bots Interact Under the Hood

1. **The Listener (`bot.py`):** Operates securely on a read-only WebSocket connection via the standard `TikTokLive` library. It passes incoming messages to the AI provider (like OpenAI or DeepSeek) to generate conversational responses or analyze chat context.
2. **The Enforcer (`mod.py`):** Operates entirely via raw HTTP POST requests. When the AI or an admin decides a user needs to be muted, `bot.py` signals the moderation engine. `mod.py` then crafts the required network payload (stitching together the `room_id`, target user ID, and active session cookies) and fires it directly into TikTok's Webcast API.

---

## Installation & Execution Guide

To deploy the twin-bot moderation system, follow these execution steps:

## 1. Install Required Dependencies
Ensure you have the base TikTok library and your chosen AI provider's SDK installed:
```bash
pip install TikTokLive openai google-generativeai anthropic browser-cookie3 requests

2. Configure Your Core Files
Before launching, ensure your localized environment and identity states are established:

.env: Add your AI provider API keys and your TikTok sessionid extraction string.

identity.md: Define your bot's system instructions, strict behavior rules, and chat persona.

config.json: Make sure your shared state file exists in the directory so both scripts can establish base permissions.

3. Launching the Twin-Bot Suite
Because this is a multi-script architecture, you need to open two separate terminal windows and run them concurrently.

Terminal 1 (Start the Listener):

Bash
python bot.py
Terminal 2 (Start the Enforcer):

Bash
python mod.py
Once both terminals indicate a successful connection to the live room, your automated AI moderation and interactive chat responses are fully operational!
