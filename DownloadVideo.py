import subprocess
import json
from datetime import datetime
import yaml
import random
import time
import os

# ANSI escape code for yellow color
YELLOW = '\033[93m'
ENDC = '\033[0m'

# Assuming cookies file is stored in the same directory as the script
COOKIES_FILE_PATH = "cookies.txt"
# Static referer URL for demonstration
REFERER_URL = "https://www.youtube.com/"

def debug_print(message):
    print(YELLOW + message + ENDC)

def get_latest_video_info(channel_url):
    channel_name = channel_url.split('@')[-1].split('/')[0] if '@' in channel_url else channel_url.split('/')[-1]

    command = ['yt-dlp', '--dump-json', '--playlist-end', '1', '--referer', REFERER_URL, channel_url]
    
    # Check if cookies.txt exists and add --cookies option accordingly
    if os.path.exists(COOKIES_FILE_PATH):
        command += ['--cookies', COOKIES_FILE_PATH]
    
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode == 0:
        video_info = json.loads(result.stdout)
        if 'upload_date' in video_info:
            publish_date = datetime.strptime(video_info['upload_date'], '%Y%m%d')
        else:
            raise Exception(f"No valid date field in video info from {channel_url}")
        
        # Extracting additional details
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
    else:
        raise Exception(f"Failed to fetch video info from {channel_url}")

def print_winner_info(video_info):
    publish_date = video_info['publish_date'].strftime('%Y-%m-%d')
    channel_name = video_info['channel_name']
    video_title = video_info['video_title']
    video_length = video_info['video_length']
    debug_print(f"Winner: {publish_date} - {channel_name} - {video_title} - {video_length}")

def download_video(video_url, max_res):
    output_filename = "latest_video"
    command = ['yt-dlp', '-f', f'bestvideo[height<={max_res}]+bestaudio/best[height<={max_res}]', '-o', output_filename + '.%(ext)s', '--referer', REFERER_URL, video_url]
    
    # Check if cookies.txt exists and add --cookies option accordingly
    if os.path.exists(COOKIES_FILE_PATH):
        command += ['--cookies', COOKIES_FILE_PATH]
    
    subprocess.run(command, check=True)
    return output_filename

def fetch_and_download_latest_video(channel_urls, max_res):
    latest_videos = []
    for channel_url in channel_urls:
        try:
            video_info = get_latest_video_info(channel_url)
            latest_videos.append(video_info)
            wait_time = random.uniform(6, 15)
            debug_print(f"Waiting for {wait_time:.2f} seconds before next request...")
            time.sleep(wait_time)
        except Exception as e:
            debug_print(f"Error fetching video from {channel_url}: {e}")

    if latest_videos:
        videos_by_date = {}
        for video in latest_videos:
            videos_by_date.setdefault(video['publish_date'], []).append(video)

        most_recent_date = max(videos_by_date.keys())
        most_recent_videos = videos_by_date[most_recent_date]

        most_recent_video = random.choice(most_recent_videos)
        
        print_winner_info(most_recent_video)  # Print winner info
        
        video_url = most_recent_video['url']
        return download_video(video_url, max_res)
    else:
        raise Exception("No videos found in the provided channels")

if __name__ == "__main__":
    try:
        with open("variables.yaml", "r") as file:
            config = yaml.safe_load(file)

        channel_urls = config['youtube_channels']
        max_res = config['max_resolution']
        file_basename = fetch_and_download_latest_video(channel_urls, max_res)
        debug_print(f"Downloaded video: {file_basename}")
    except Exception as e:
        debug_print(f"An error occurred: {e}")
