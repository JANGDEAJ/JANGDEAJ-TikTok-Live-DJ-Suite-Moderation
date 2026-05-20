DJ Suite & Moderation Commands Reference

This guide details the commands divided cleanly by engine (DJ, Mod, Bot) and explains the immunity and safeguard rules.

PART 1: DJ ENGINE COMMANDS (Media & Audio)

These commands control the background media playback (via Chrome or Headless MPV).

Viewer DJ Commands (Open to Everyone)

!play <link / video ID> - Queues a track from YouTube, TikTok, Twitter/X, or Instagram.

!skip or !next - Skips the currently playing song or video.

!loop - Toggles repeating the current track indefinitely.

!rickroll - Injects Rickroll at position zero, skips the active track, and pushes the rest of the queue back.

!lofi - Clears active playback to play a 10-minute Lofi study mix.

!aemeath - Plays the designated personal theme track starting at timestamp 1:55.

!party - Flashes system volume between 40% and 100% for 5 seconds.

Meme Overrides: Type any of these triggers to play a quick soundbite and return to the normal queue:
!johncena, !rko, !a10, !mayo, !minecraft, !wesker, !invincible, !dexter, !windows, !ps2

Admin DJ Commands

!enough - The Chaos Toggle. Turning this OFF completely freezes all viewer-only commands (memes, speed changes, !party), allowing only standard !play requests.

!volume <0-100> - Directly changes the host machine's master system volume.

!reset or !normalspeed - Clears any active audio filters and resets playback speed to a flat 1.0x.

PART 2: MODERATION ENGINE COMMANDS (mod.py)

These commands control live chat safety and execute actions directly through the reverse-engineered Webcast API.

Admin Moderation Commands

!ban <@username> - Blacklists a specific user from using the DJ system (!play).

!unban <@username> - Removes a user from the DJ blacklist.

!mute <@username> [duration] - Mutes a user in live chat via raw HTTP POST payload (e.g., !mute @user 5m).

!unmute <@username> - Unmutes a user in live chat.

!warn <@username> [reason] - Sends a warning to a user in live chat. Repeated warnings trigger automated muting actions.

!nuke - Triggers an AI sweep of the recent chat logs to identify raid accounts and mass-mutes them instantly.

PART 3: AI CHATBOT COMMANDS (bot.py)

These commands control the conversational AI responses and automated monitoring.

Viewer Chat Commands

!ask <prompt> or !ai <prompt> - Queries the AI provider (DeepSeek/Gemini) to generate a conversational response.

Admin Chat Commands

!say <message> - Forces the AI bot to send a specific announcement message into live chat.

!sleep - Temporarily pauses the AI chatbot responses and halts automated spam checks.

!wakeup - Resumes AI chatbot responses and automated spam checking.

PART 4: OWNER-ONLY COMMANDS (System Host)

These commands can only be typed by the primary bot host to manage administrators.

!addadmin <@username> - Dynamically grants a viewer full Admin/Moderator privileges.

!removeadmin <@username> - Revokes Admin/Moderator privileges from a user.

!admins - Outputs the list of active administrators directly into the local terminal window.

PART 5: SYSTEM SAFEGUARDS & IMMUNITY RULES

1. How the !nuke Command Works

When an admin type !nuke, the following sequence triggers:

bot.py reads the last 50-100 chat messages from memory.

The chat log is analyzed by the AI to look for patterns (e.g., identical spam strings, rapid-fire bot accounts, or coordinated raids).

The AI returns a list of target usernames.

mod.py immediately fires parallel HTTP POST payloads to TikTok's API, mass-muting all raiders within milliseconds.

2. The Immunity Hierarchy

To prevent the AI or other admins from accidentally muting, warning, or banning vital stream members, a strict immunity protocol is hardcoded into config.json:

Tier 1: Broadcaster / Streamer

Absolute 100% immunity. Cannot be warned, muted, banned, or nuked under any circumstances.

Tier 2: Bot Owner (Host Account)

Full immunity. Cannot be demoted or moderated by other admins.

Tier 3: Admins / Moderators

Exempt from all automated spam-detection filters and !nuke sweeps.

Tier 4: VIPs / Whitelisted Users

Shielded from automated spam-detection filters (e.g., repeating characters or excessive symbols) to prevent false-positives, but can still be manually moderated by an admin if needed.
