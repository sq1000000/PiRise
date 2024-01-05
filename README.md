# PiRise
PiRise is a project aimed to act as an alarm clock by automatically playing the latest video from a set of YouTube channels.  

## Features
- Automatically plays the latest video from a specified set of YouTube channels.
- Customizable alarm times for each day of the week.
- HDMI-CEC integration to switch the TV on and off.
- Adaptive video resolution.
  
## Getting Started

### Prerequisites
- Raspberry Pi (any model with HDMI out, but preferably 4+).
- TV or monitor with HDMI input and CEC support.
- Internet connection.
- Basic knowledge of Python and Raspberry Pi setup.

### Installation
1. **Install Required Software**:

     ```
     sudo apt install cec-utils yt-dlp python3-yaml ffmpeg screen vlc
     ```
     
2. **Clone the Repository**:
   ```
   git clone https://github.com/sq1000000/PiRise.git
   cd PiRise
   ```

3. **Configure the Application**:
   - Edit the `variables.yaml` file to set your preferred YouTube channels, alarm times, and video resolution.

### Usage

- **Start the Alarm Clock**:
  Run the script with:
  
  ```
  python3 main.py
  ```
- The script will run continuously, checking for the alarm trigger.

## Roadmap
- **Fix Desktop loading Bug**:  Sometimes on the Pi 4, and every time on the Pi 5, the system goes into some neutral sleep/awake state when the TV is woken back up. This disables the audio, and can only be fixed with a system restart.
- **Auto Start**: Figure out a way to make main.py start as soon as the Pi boots.
- **Time Warning**: Make some sort of indicator saying you've been watching the video for too long, and seriously need to get up. Maybe the screen could go grayscale.
- **More YouTube Options**: Add support to only play videos from channels if they have specific keywords, or are a cerain length.
- **Sense HAT Lighting**: Add support for a gradual morning light with the Raspberry Pi Sense HAT.
- **Volume Control**: Implement adjustable volume settings for the alarm. Or maybe progressively louder volume.
- **Notification System**: Integrate notifications for alarm status and error messages. Perhaps with Discord webhooks?
- **User Interface**: Develop a user-friendly interface for easier schedule and preference management.

## Contributing
If you modify this code, don't keep it a secret, make a pull request. I love seeing my code get better.
