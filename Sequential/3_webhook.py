#!/usr/bin/env python3

import requests
import yaml
import os

def load_config():
    """Load main variables from variables.yaml."""
    with open("variables.yaml", "r") as file:
        return yaml.safe_load(file)

def load_latest_video_info():
    """Read metadata from latest_video.yaml."""
    if not os.path.exists("latest_video.yaml"):
        raise FileNotFoundError("No latest_video.yaml found. Run 7_download_tomorrows_vid.py first?")
    with open("latest_video.yaml", "r") as file:
        return yaml.safe_load(file)

def main():
    config = load_config()
    video_info = load_latest_video_info()

    # Ensure we have a Discord webhook URL
    webhook_url = config.get("discord_webhook_url", "")
    if not webhook_url:
        print("No 'discord_webhook_url' found in variables.yaml. Exiting.")
        return

    # Build a message with basic video details
    # You can tweak formatting however you like
    message_lines = []
    message_lines.append("**Now Playing:**")
    message_lines.append(f"**Title**: {video_info.get('video_title', 'Unknown')}")
    message_lines.append(f"**Channel**: {video_info.get('channel_name', 'Unknown')}")
    message_lines.append(f"**Publish Date**: {video_info.get('publish_date', 'Unknown')}")
    message_lines.append(f"**Length**: {video_info.get('video_length', 'Unknown')}")
    message_lines.append(f"**URL**: {video_info.get('url', 'N/A')}")

    # Join them into a single string
    payload_content = "\n".join(message_lines)

    payload = {
        "content": payload_content
    }

    # Send a POST request to the Discord webhook
    try:
        response = requests.post(webhook_url, json=payload)
        if response.status_code == 204:
            print("Discord webhook sent successfully.")
        else:
            print(f"Failed to send webhook. Status code: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error sending Discord webhook: {e}")

if __name__ == "__main__":
    main()

