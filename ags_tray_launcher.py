import threading
import sys
import os
from PIL import Image
import pystray
from pystray import MenuItem as item

from ags_launcher import main_ags  # Import your main AGS logic

def start_ags():
    main_ags()

def refresh(icon, item):
    print("Refreshing AGS...")
    os.execl(sys.executable, sys.executable, *sys.argv)

def quit_app(icon, item):
    print("Quitting AGS...")
    icon.stop()
    os._exit(0)

def setup_tray():
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")

    icon_path = os.path.join(base_path, "ags_icon.ico")
    try:
        image = Image.open(icon_path)
    except Exception as e:
        print(f"Failed to load icon: {e}")
        image = None

    menu = (
        item("Refresh", refresh),
        item("Exit", quit_app)
    )
    icon = pystray.Icon("AGS", image, "AGS - Advanced Game Status", menu)
    icon.run()

if __name__ == "__main__":
    ags_thread = threading.Thread(target=start_ags, daemon=True)
    ags_thread.start()
    setup_tray()
