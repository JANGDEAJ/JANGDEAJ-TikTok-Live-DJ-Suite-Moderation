TikTok Live Cross-Platform Media Engine Suite
Developed a high-performance, event-driven automation suite using Python asyncio that connects real-time live chat interactions with low-latency media playback loops across Windows, macOS, and Linux.

Key Technical Achievements:

Headless Architecture (mpv Backend): Engineered a high-efficiency configuration that decouples web runtimes from asset extraction. Utilizes yt-dlp to extract raw audio payloads directly from edge servers, feeding streams into a detached, non-rendering mpv sub-process.

0% Desktop Input Interference: Eliminated active application window generation entirely (CREATE_NO_WINDOW flags on Windows / detached terminal workers on Unix). This completely prevents background stream processes from intercepting keyboard or mouse focus, allowing users to run frame-critical gaming inputs or development tools smoothly.

85% Resource Optimization: Optimized host machine performance, cutting active CPU and memory consumption by up to 85% compared to running multi-process desktop browser window instances.

Desktop Automation (Chrome GUI Engine): Implemented native operating system application hooks to drive front-end web players directly. Leveraged AppleScript automation via osascript on macOS to programmatically inject custom JavaScript payloads into the browser DOM layout, unlocking visual effects and speed manipulations.

Concurrent Event Pipeline: Built entirely on top of an asynchronous loop architecture to handle volatile incoming live socket events (TikTokLive), media data scraping tasks, and background player processes concurrently without blocking thread execution.

Role-Based State Management: Maintained automated memory caching for instant asset length processing while enforcing robust state lists for role-based system permissions (Owner, Admin, and Restricted/Banned user layers).
