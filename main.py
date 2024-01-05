import datetime
import time
import yaml
import logging
import DownloadVideo
import subprocess
import os

# ANSI escape code for yellow color
YELLOW = '\033[93m'
ENDC = '\033[0m'

def debug_print(message):
    print(YELLOW + message + ENDC)

def switch_to_pi_input():
    subprocess.run('echo "as" | cec-client -s -d 1', shell=True)

def control_tv(command):
    if command == "standby":
        subprocess.run('echo "standby 0" | cec-client -s -d 1', shell=True)

def play_video(file_basename):
    for ext in ['mp4', 'mkv', 'webm', 'flv', 'avi']:
        filename = f"{file_basename}.{ext}"
        if os.path.exists(filename):
            env = os.environ.copy()
            env['DISPLAY'] = ':0'
            subprocess.run(['cvlc', '--play-and-exit', '--fullscreen', filename], env=env)
            return filename
    raise Exception("Downloaded video file not found")

def delete_video(file_basename):
    for ext in ['mp4', 'mkv', 'webm', 'flv', 'avi']:
        filename = f"{file_basename}.{ext}"
        if os.path.exists(filename):
            os.remove(filename)

def is_time_to_trigger(current_time, target_hour, target_minute, pre_download_time):
    download_time = current_time.replace(hour=target_hour, minute=target_minute, second=0, microsecond=0) - datetime.timedelta(minutes=pre_download_time)
    return download_time <= current_time < download_time + datetime.timedelta(minutes=1)

def log_error(message):
    logging.error(message)

def load_config():
    with open("variables.yaml", "r") as file:
        return yaml.safe_load(file)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

already_triggered = False
video_downloaded = False
file_basename = "latest_video"

while True:
    try:
        current_time = datetime.datetime.now()
        config = load_config()

        current_day = current_time.strftime("%A").lower()
        start_time_key = f"start_time_{current_day}"

        if start_time_key in config:
            target_hour = config[start_time_key]["hour"]
            target_minute = config[start_time_key]["minute"]
        else:
            raise Exception(f"Start time not configured for {current_day}")

        if is_time_to_trigger(current_time, target_hour, target_minute, config["pre_download_time"]) and not video_downloaded:
            debug_print("Initiating video download process...")
            file_basename = DownloadVideo.fetch_and_download_latest_video(config['youtube_channels'], config["max_resolution"])
            video_downloaded = True
            debug_print(f"Video downloaded: {file_basename}")

        if is_time_to_trigger(current_time, target_hour, target_minute, 0) and not already_triggered:
            debug_print("Triggering video playback...")
            switch_to_pi_input()
            time.sleep(config.get("tv_wake_delay", 60))

            filename = play_video(file_basename)
            if filename:
                time.sleep(config.get("tv_wake_delay", 60))
                control_tv("standby")
                delete_video(file_basename)
                already_triggered = True
                debug_print(f"Video playback completed and TV turned off: {filename}")
            else:
                log_error("Video not downloaded in time")

        if current_time >= current_time.replace(hour=target_hour, minute=target_minute + 1, second=0, microsecond=0):
            already_triggered = False
            video_downloaded = False
            # debug_print("Resetting triggers for the next cycle.")  # This line is now commented out

        time.sleep(10)
    except Exception as e:
        log_error(f"An error occurred: {e}")

