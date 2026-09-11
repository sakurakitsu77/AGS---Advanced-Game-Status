import os
import time
from core import discord_rich_presence

SAVE_DIR = r"C:\Users\Sakura_Kitsune\Documents\My Games\Skyrim Special Edition\Saves"

def get_latest_save():
    saves = [f for f in os.listdir(SAVE_DIR) if f.lower().endswith(".ess")]
    if not saves:
        return None
    saves_full_path = [os.path.join(SAVE_DIR, save) for save in saves]
    saves_with_time = [(save, os.path.getmtime(save)) for save in saves_full_path]
    latest_save = max(saves_with_time, key=lambda x: x[1])[0]
    return latest_save

def extract_info_from_ess(filepath):
    with open(filepath, "rb") as f:
        data = f.read(4096)
        try:
            text = data.decode("utf-8", errors="ignore")
            parts = text.split("\x00")
            player_name = parts[1].strip() if len(parts) > 1 else "Unknown"
            location = parts[2].strip() if len(parts) > 2 else "Unknown Location"
        except Exception:
            player_name = "Unknown"
            location = "Unknown Location"
    return player_name, location

def run(stop_event):
    discord_rich_presence.connect()
    time.sleep(2)  # Wait for Discord to fully connect
    print("Started monitoring Skyrim save files...")

    while not stop_event.is_set():
        try:
            save_file = get_latest_save()
            if not save_file:
                print("No Skyrim saves found.")
                time.sleep(10)
                continue

            save_path = os.path.join(SAVE_DIR, save_file)
            player_name, location = extract_info_from_ess(save_path)
            player_name = player_name or "Unknown"
            location = location or "Unknown Location"

            discord_rich_presence.update_status(
                details="Playing Skyrim (via AGS)",
                state=f"{player_name} | {location}",
                large_image="tesvskyrim",
                large_text="Credit: Sakura_Kitsu",
                small_image="tesvskyrim",
                small_text="Adventuring"
            )

            print(f"🔄 Updated status: details='Playing Skyrim (via AGS)', state='{player_name} | {location}'")
            print(f"Status updated: Player={player_name}, Location={location}")

        except Exception as e:
            print(f"Error reading save or updating status: {e}")

        time.sleep(30)

    print("Stopping Skyrim presence updater.")
