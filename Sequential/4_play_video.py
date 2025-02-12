#!/usr/bin/env python3

import os
import subprocess
import time
import yaml

def load_config():
    """Load settings from variables.yaml."""
    with open("variables.yaml", "r") as file:
        return yaml.safe_load(file)

def play_video(file_basename):
    """
    Look for a downloaded video file with any of the common extensions.
    Play it full-screen using VLC.
    Return the full filename if found/played, otherwise raise an exception.
    """
    for ext in ['mp4', 'mkv', 'webm', 'flv', 'avi']:
        filename = f"{file_basename}.{ext}"
        if os.path.exists(filename):
            env = os.environ.copy()
            env['DISPLAY'] = ':0'  # Ensure VLC knows which display to use
            subprocess.run(['cvlc', '--play-and-exit', '--fullscreen', filename], env=env)
            return filename
    raise FileNotFoundError("Downloaded video file not found.")

def main():
    config = load_config()
    
    # If you still want a short delay before playing, set it here:
    tv_wake_delay = config.get("tv_wake_delay", 60)
    time.sleep(tv_wake_delay)

    file_basename = "latest_video"

    try:
        filename = play_video(file_basename)
        print(f"Video playback completed: {filename}")
    except FileNotFoundError:
        print("No valid video file found for playback.")

if __name__ == "__main__":
    main()

