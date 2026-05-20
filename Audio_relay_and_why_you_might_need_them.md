## AudioRelay User Guide for Windows, Linux, and macOS
(Route audio from your bot-hosting computer to OBS or other devices)

---

## Why AudioRelay?
This application connects your devices—PC to PC, mobile to mobile, or PC to mobile—to share audio seamlessly. For example, if your main PC has very little RAM to spare for a browser, you can offload those tasks to a second device like a phone, tablet, or another laptop. AudioRelay lets you bring music or voice chat from those secondary devices directly into your main system. It gives you easy control over your audio while saving your primary PC's resources for what matters most.

---

## Prerequisites

* **Windows:**
    1. Download and install **AudioRelay**: `https://audiorelay.net/`
    2. Download and install **VB-CABLE** (Free Virtual Audio Driver): `https://vb-audio.com/Cable/` *(Restart your computer once after installation)*
* **Linux:**
    1. Download AudioRelay `.deb` or `.AppImage`: `https://audiorelay.net/`
    2. Install PulseAudio and its controller panel:
       ```bash
       sudo apt install pulseaudio pavucontrol
       ```
* **macOS:**
    1. Download and install **AudioRelay**: `https://audiorelay.net/`
    2. Install the **BlackHole (2ch)** virtual audio driver to act as your Virtual Mic/Audio Input (Install via Homebrew):
       ```bash
       brew install blackhole-2ch
       ```

---

## Setup Scenarios

### Scenario 1: Windows (Bot PC) → Another Windows PC (OBS Stream PC)
* **Bot PC (Server):** Open AudioRelay > Click **Start Server** > Set Audio Source to **Desktop Audio** or **Stereo Mix** > Note the IP Address displayed (e.g., `192.168.1.10`).
* **OBS PC (Client):** Open AudioRelay > Click **Connect to Server** > Type the Bot PC's IP > Set Output to **CABLE Input (VB-Audio Virtual Cable)**.
* **OBS Configuration:** Go to OBS > Settings > Audio > Desktop Audio and select **CABLE Output**.

### Scenario 2: Windows (Bot PC) → Mobile Phone (Android / iOS)
* **Windows PC (Server):** Open AudioRelay > Click **Start Server** > Set Audio Source to **Desktop Audio** > Note the IP Address.
* **Phone (Client):** Download AudioRelay from the Play Store / App Store > Open the app and tap **Connect** > Type the Windows PC's IP > Plug in your headphones and listen.

### Scenario 3: Mobile Phone → Windows PC (Phone Audio Out to PC/OBS)
* **Windows PC (Server):** Open AudioRelay > Click **Start Server** > Set Output to **CABLE Input (VB-CABLE)** or your main system speakers.
* **Phone (Client):** Open the AudioRelay app > Tap **Connect** and enter the Windows IP > Press **Play** on your phone to stream its audio directly to the PC.

### Scenario 4: Linux (Bot PC) → Target Device
* **Linux PC (Server):** Open AudioRelay > Click **Start Server** > Set Audio Source to **PulseAudio Monitor** or **Default** > Note the IP Address and connect from your client device using the steps in Scenarios 1–3.

### Scenario 5: macOS (Bot PC) → Target Device (or Receiving Audio into Mac OBS)
*macOS is a bit different; it handles audio permissions strictly and needs a third-party plugin because the OS cannot natively capture or route virtual mic lines directly through AudioRelay alone.*
* **Streaming Audio Out (Mac as Server):** Open AudioRelay > Click **Start Server** > Set Audio Source to **BlackHole 2ch**. Then, change your Mac's system sound output (System Settings > Sound > Output) to **BlackHole 2ch** so the audio routes properly to your client devices.
* **Receiving Audio In (Mac as Client):** Open AudioRelay > Click **Connect to Server** and enter the Bot PC's IP > Set Output to **BlackHole 2ch**. In **OBS**, add a new **Audio Input Capture** source and select **BlackHole 2ch** to bring the stream audio into your live broadcast.

---

## Troubleshooting

* **No Audio / Connection Failed:** Ensure all devices are connected to the exact same local Wi-Fi or LAN network.
* **Audio Delay (Latency):** Using a wired LAN cable instead of Wi-Fi will significantly improve performance and reduce delay.
* **Blocked by Firewall:** Make sure to allow AudioRelay through your Windows Firewall or OS security settings when prompted on your first launch.

Got questions? Just DM me.
