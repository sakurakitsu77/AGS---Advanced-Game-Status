import os
import time
import json
from core import discord_rich_presence, save_watcher

SAVE_DIR = r"C:\Users\Sakura_Kitsune\Saved Games\Arkane Studios\Dishonored2\base\savegame"
CHECK_INTERVAL = 10  # seconds

def parse_save_details(file_path):
    """Reads the game.details file and returns a dict of save data."""
    details = {}
    with open(file_path, "r") as file:
        for line in file:
            if "=" in line:
                key, value = line.strip().split("=", 1)
                details[key] = value
    return details

def find_latest_save():
    """Finds the most recently modified save folder and reads its game.details."""
    latest_save = None
    latest_time = 0

    for folder in os.listdir(SAVE_DIR):
        folder_path = os.path.join(SAVE_DIR, folder)
        details_path = os.path.join(folder_path, "game.details")

        if os.path.isdir(folder_path) and os.path.isfile(details_path):
            modified_time = os.path.getmtime(details_path)
            if modified_time > latest_time:
                latest_time = modified_time
                latest_save = details_path

    if latest_save:
        return parse_save_details(latest_save)
    return {}

def run():
    """Main loop for Dishonored 2 status updates."""
    discord_rich_presence.connect("your_discord_app_id_here")  # Replace with your App ID
    print("Started monitoring Dishonored 2 save files...")

    while True:
        details = find_latest_save()

        if details:
            chaos_level = int(details.get("chaosLevel", 0))
            chaos_label = (
                "Ghost" if chaos_level == 0 else
                "Low Chaos" if chaos_level == 1 else
                "High Chaos"
            )

            # Extract cleaned map name:
            map_name = details.get("mapName", "Unknown Map")
            map_name_cleaned = map_name.split("/")[-1].replace("_", " ").title()

            playtime_seconds = int(details.get("time", 0))
            playtime_hours = playtime_seconds // 3600
            playtime_minutes = (playtime_seconds % 3600) // 60
            playtime_hhmm = f"{playtime_hours:02d}h {playtime_minutes:02d}m"

            discord_rich_presence.update_status(
                details="Playing Dishonored 2 (via AGS)",
                state=f"Mission: {map_name_cleaned} | Chaos: {chaos_label}",
                large_image="dishonored2",
                large_text="Dishonored 2",
                small_image="ags_main_logo",
                small_text=f"Playtime: {playtime_hhmm}"
            )

            print(f"Status updated: Mission={map_name_cleaned}, Chaos={chaos_label}, Playtime={playtime_hhmm}")
        else:
            print("No save files found.")

        time.sleep(CHECK_INTERVAL)

