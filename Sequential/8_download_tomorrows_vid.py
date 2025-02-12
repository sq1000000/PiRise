#!/usr/bin/env python3

import subprocess
import json
import os
import yaml
import random
import time
from datetime import datetime

YELLOW = '\033[93m'
ENDC = '\033[0m'

COOKIES_FILE_PATH = "cookies.txt"
REFERER_URL = "https://www.youtube.com/"

def debug_print(message):
    print(f"{YELLOW}{message}{ENDC}")

def load_config():
    with open("variables.yaml", "r") as file:
        return yaml.safe_load(file)

def get_latest_video_info(channel_url):
    """
    Returns metadata of the most recent video for the given channel_url,
    including its publish date, channel name, title, etc.
    """
    channel_name = channel_url.split('@')[-1].split('/')[0] if '@' in channel_url else channel_url.split('/')[-1]
    command = [
        'yt-dlp', '--dump-json', '--playlist-end', '1',
        '--referer', REFERER_URL, channel_url
    ]

    # Use cookies if available
    if os.path.exists(COOKIES_FILE_PATH):
        command += ['--cookies', COOKIES_FILE_PATH]

    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"Failed to fetch video info from {channel_url}")

    video_info = json.loads(result.stdout)
    if 'upload_date' not in video_info:
        raise Exception(f"No valid date field in video info from {channel_url}")

    publish_date = datetime.strptime(video_info['upload_date'], '%Y%m%d')
    channel_name = video_info.get('uploader', channel_name)
    video_title = video_info.get('title', 'Unknown Title')
    video_length = str(int(video_info.get('duration', 0) / 60)) + ' minutes'

    debug_print(f"Latest video from {channel_name}: {publish_date}")
    return {
        'url': video_info['webpage_url'],
        'publish_date': publish_date,
        'channel_name': channel_name,
        'video_title': video_title,
        'video_length': video_length
    }

def print_winner_info(video_info):
    """
    Log/print the chosen 'winner' video's info before downloading.
    """
    publish_date = video_info['publish_date'].strftime('%Y-%m-%d')
    channel_name = video_info['channel_name']
    video_title = video_info['video_title']
    video_length = video_info['video_length']
    debug_print(f"Winner: {publish_date} - {channel_name} - {video_title} - {video_length}")

def download_video(video_url, max_res, output_basename):
    """
    Downloads a video from 'video_url' into 'output_basename.(ext)'.
    The best matching format under the given max_res is used.
    Returns the name of the downloaded basename (without extension).
    """
    command = [
        'yt-dlp',
        '-f', f'bestvideo[height<={max_res}]+bestaudio/best[height<={max_res}]',
        '-o', output_basename + '.%(ext)s',
        '--referer', REFERER_URL,
        video_url
    ]

    if os.path.exists(COOKIES_FILE_PATH):
        command += ['--cookies', COOKIES_FILE_PATH]

    subprocess.run(command, check=True)  # Raises CalledProcessError if fails
    return output_basename

def get_downloaded_filename(basename):
    """
    After yt-dlp finishes, find the actual file extension used.
    Returns the complete filename if found, else None.
    """
    for ext in ['mp4', 'mkv', 'webm', 'flv', 'avi']:
        full_path = f"{basename}.{ext}"
        if os.path.exists(full_path):
            return full_path
    return None

def remove_old_video(file_basename):
    """
    Delete any old video file matching file_basename.(ext).
    """
    for ext in ['mp4', 'mkv', 'webm', 'flv', 'avi']:
        old_file = f"{file_basename}.{ext}"
        if os.path.exists(old_file):
            os.remove(old_file)
            debug_print(f"Deleted old video file: {old_file}")

def fetch_and_download_latest_video(channel_urls, max_res):
    """
    1) Identify the newest upload among all channels.
    2) Download it to 'latest_video_new.(ext)'.
    3) If that succeeds, remove the old 'latest_video.(ext)'.
    4) Rename 'latest_video_new.(ext)' => 'latest_video.(ext)'.
    5) Write metadata (channel, title, date, length, etc.) to 'latest_video.yaml'.
    """
    latest_videos = []
    for channel_url in channel_urls:
        try:
            video_info = get_latest_video_info(channel_url)
            latest_videos.append(video_info)
            # Short random delay to avoid hitting YouTube too quickly
            wait_time = random.uniform(6, 15)
            debug_print(f"Waiting for {wait_time:.2f} seconds before next request...")
            time.sleep(wait_time)
        except Exception as e:
            debug_print(f"Error fetching video from {channel_url}: {e}")

    if not latest_videos:
        raise Exception("No videos found in the provided channels")

    # Group by publish_date, find the most recent date, then pick a random video from that date
    videos_by_date = {}
    for video in latest_videos:
        videos_by_date.setdefault(video['publish_date'], []).append(video)

    most_recent_date = max(videos_by_date.keys())
    most_recent_videos = videos_by_date[most_recent_date]
    chosen_video = random.choice(most_recent_videos)

    print_winner_info(chosen_video)

    # Download to a temporary new basename (avoid overwriting old file)
    temp_basename = "latest_video_new"
    download_video(chosen_video['url'], max_res, temp_basename)

    # Check what file extension was used for the new download
    new_file = get_downloaded_filename(temp_basename)
    if not new_file:
        raise Exception("Download completed but the new file was not found.")

    # If we successfully have a new file, remove the old file, then rename
    remove_old_video("latest_video")
    extension = os.path.splitext(new_file)[1]  # e.g. ".mp4"
    final_file = f"latest_video{extension}"
    os.rename(new_file, final_file)
    debug_print(f"Renamed {new_file} to {final_file}")

    # Write metadata about the newest video to latest_video.yaml
    latest_video_metadata = {
        'channel_name': chosen_video['channel_name'],
        'video_title': chosen_video['video_title'],
        'publish_date': chosen_video['publish_date'].strftime('%Y-%m-%d'),
        'video_length': chosen_video['video_length'],
        'url': chosen_video['url'],
        'filename': final_file
    }

    with open("latest_video.yaml", "w") as yaml_file:
        yaml.safe_dump(latest_video_metadata, yaml_file)
    debug_print("Wrote latest video metadata to latest_video.yaml.")

    return final_file

def main():
    try:
        config = load_config()
        channel_urls = config['youtube_channels']
        max_res = config['max_resolution']

        new_file = fetch_and_download_latest_video(channel_urls, max_res)
        debug_print(f"New video downloaded and ready: {new_file}")

    except Exception as e:
        debug_print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

