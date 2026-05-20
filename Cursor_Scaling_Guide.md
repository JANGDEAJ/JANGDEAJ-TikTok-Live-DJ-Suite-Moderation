How to Fix Cursor Coordinates for Different Screen Resolutions

If your script uses mouse clicks or automated cursor movements (such as PyAutoGUI or direct Windows API clicks), hardcoded coordinates like (1500, 800) will fail if another user runs the script on a different screen resolution or with Windows display scaling turned on (e.g., 125% or 150% scaling).

Here is how to modify your script to automatically calculate and scale your cursor coordinates for any device.

1. The DPI Scaling Fix (Critical for Windows)

Windows often scales display elements by default (125%, 150%, etc.). This causes Python to read coordinate maps incorrectly. You must force Python to be "DPI Aware" at the very beginning of your script.

Add this code block to the top of your script:

import sys
import ctypes

# Force Windows to use actual physical screen coordinates, bypassing DPI scaling
if sys.platform == "win32":
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(2) # Per-monitor DPI aware
    except Exception:
        try:
            ctypes.windll.user32.SetProcessDPIAware() # Fallback for older Windows
        except Exception:
            pass


2. Dynamic Resolution Scaling Formula

To make your coordinates scale dynamically, you must define the base resolution you used to develop the script (e.g., 1080p) and then calculate a ratio based on the current user's actual screen resolution.

Use this formula to scale your target coordinates:

$$x_{\text{scaled}} = x_{\text{dev}} \times \left(\frac{\text{Width}_{\text{user}}}{\text{Width}_{\text{dev}}}\right)$$

$$y_{\text{scaled}} = y_{\text{dev}} \times \left(\frac{\text{Height}_{\text{user}}}{\text{Height}_{\text{dev}}}\right)$$

Implementation Code:

Replace your hardcoded click coordinates with this automated scaling function:

import pyautogui

# 1. Define the screen resolution you used when writing the script
DEV_WIDTH = 1920
DEV_HEIGHT = 1080

# 2. Grab the current user's actual screen size
USER_WIDTH, USER_HEIGHT = pyautogui.size()

# 3. Create a scaling function
def get_scaled_coords(x_dev, y_dev):
    """
    Translates coordinates from your development screen size (1920x1080)
    to match the current user's actual screen resolution.
    """
    scaled_x = int(x_dev * (USER_WIDTH / DEV_WIDTH))
    scaled_y = int(y_dev * (USER_HEIGHT / DEV_HEIGHT))
    return scaled_x, scaled_y

# --- How to use it in your code ---

# If your target button is at (1500, 800) on your 1080p screen:
target_x, target_y = get_scaled_coords(1500, 800)

# Python will now click the correct spot on 1080p, 2K, 4K, or 720p screens!
pyautogui.click(target_x, target_y)
