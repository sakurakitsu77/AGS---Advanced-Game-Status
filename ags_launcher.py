import time
import psutil
import threading
import importlib
import os
from core import discord_rich_presence

GAME_PROCESS_MAP = {
    "Dishonored2.exe": "games.dishonored2",
    "SkyrimSE.exe": "games.skyrim",
    "Skyrim.exe": "games.skyrim",
}

def main_ags():
    class GamePresenceManager:
        def __init__(self):
            self.current_game = None
            self.thread = None
            self.stop_event = threading.Event()
            self.idle_set = False

        def is_process_running(self, process_name):
            for proc in psutil.process_iter(['name']):
                try:
                    if proc.info['name'] and proc.info['name'].lower() == process_name.lower():
                        return True
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            return False

        def run_game_presence(self, module_name):
            game_module = importlib.import_module(module_name)
            game_module.run(self.stop_event)

        def start_game_presence(self, module_name):
            if self.thread and self.thread.is_alive():
                self.stop_event.set()
                self.thread.join()
            self.stop_event.clear()
            self.thread = threading.Thread(target=self.run_game_presence, args=(module_name,), daemon=True)
            self.thread.start()
            self.idle_set = False

        def set_idle_status(self):
            try:
                discord_rich_presence.connect()
                discord_rich_presence.update_status(
                    details="Waiting for games to play",
                    state="No game detected for status.",
                    large_image="ags_main_logo",
                    large_text="Advanced Game Status (AGS) by Sakura_Kitsu"
                )
                self.idle_set = True
                print("\u23f3 Idle status set: Waiting for games to play")
            except Exception as e:
                print(f"Error setting idle status: {e}")

        def monitor_games(self):
            os.system('cls' if os.name == 'nt' else 'clear')
            print("=========================================")
            print("     AGS - Advanced Game Status")
            print("     Created by Sakura_Kitsu")
            print("=========================================")

            self.set_idle_status()

            try:
                while True:
                    active_game = None
                    for exe_name, module_name in GAME_PROCESS_MAP.items():
                        if self.is_process_running(exe_name):
                            active_game = module_name
                            break

                    if active_game != self.current_game:
                        if self.current_game:
                            print(f"\n\u274c Game closed: {self.current_game}")
                            self.stop_event.set()
                            if self.thread:
                                self.thread.join()

                        if active_game:
                            game_name = active_game.split('.')[-1].capitalize()
                            print(f"\n\u2705 Game detected: {game_name}")
                            print("\ud83c\udfae Discord Rich Presence activated.\n")
                            self.start_game_presence(active_game)
                        else:
                            if not self.idle_set:
                                self.set_idle_status()
                            else:
                                print("\n\u23f3 No monitored game detected. Idle status active.")

                        self.current_game = active_game

                    time.sleep(10)

            except KeyboardInterrupt:
                print("\nExiting AGS Game Process Monitor.")
                self.stop_event.set()
                if self.thread:
                    self.thread.join()

    manager = GamePresenceManager()
    manager.monitor_games()

if __name__ == "__main__":
    main_ags()
