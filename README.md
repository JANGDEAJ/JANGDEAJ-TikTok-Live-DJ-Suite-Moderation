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
