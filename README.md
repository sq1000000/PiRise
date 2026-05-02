# PiRise
PiRise is a project aimed to act as an alarm clock by automatically playing the latest video from a set of YouTube channels with a Raspberry Pi.  

## Features
- Automatically plays the latest video from a specified set of YouTube channels.
- Customizable alarm times for each day of the week.
- [HDMI-CEC](https://en.wikipedia.org/wiki/Consumer_Electronics_Control) integration to switch the TV on and off.
- Automatically toggles attached USB lights for the duration of the video.
- Send a discord notification saying what video is being played.
- Customizable video resolution.
  
## Getting Started

### Prerequisites
- Raspberry Pi (any model with HDMI out, but ideally 4+).
- TV or monitor with HDMI input and CEC support.
- Internet connection.
- Basic knowledge of the Raspberry Pi setup process.

### Installation
1. **Install Required Software**:
     ```
     sudo apt install cec-utils yt-dlp python3-yaml ffmpeg screen vlc
     ```
     
2. **Clone the Repository**:
   ```
   git clone https://github.com/sata1000000/PiRise.git
   cd PiRise
   ```

3. **Configure the Application**:
   - Edit the `variables.yaml` file to set your preferred YouTube channels, alarm times, and video resolution.
   - Edit the `variables.yaml` file to set your [Discord webhook](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks) URL to send video information.
   - Add your own `cookies.txt` file. This isn't completely necessary, but it can make the youtube downloader less likely to fail.

4. **Download the first video**:

   Don't worry, the program will take care of this automatically later on.

   ```
   python3 Sequential/8_download_tomorrows_vid.py
   ```

6. **Run on startup** (optional):

   With this step, the program will start in a [screen session](https://linuxize.com/post/how-to-use-linux-screen/) as soon as the RPi boots.

   ```
   cd $HOME
   mkdir -p ~/startup
   git clone https://github.com/sata1000000/AutoRun.git ~/startup
   cd ~/startup/internals/other
   ./install_service.sh $USER
   cd $HOME
   cp ~/PiRise/Extra/PiRise_auto.sh ~/startup/screen/PiRise.sh
   ```

   Since the program starts with the system, all you have to do now is reboot the RPi and wait for the time specified in `variables.yaml` to arrive.

   ```
   sudo reboot
   ```

### Usage (One time)

  Assuming you did steps 1-4, this command will start playing the video on an attached display without waiting for a specified time.
  
  ```
  python3 main.py -n
  ```

## Roadmap
- **Time Warning**: Make some sort of indicator saying you've been watching the video for too long, and you seriously need to get up. Maybe the screen could go grayscale.
- **Add GIF to README**: The README could use a GIF timelapse of the program in action.
- **More YouTube Options**: Add support to only play videos from channels if they have specific keywords, or are a certain length.
- **Sense HAT Lighting**: Add support for a gradual morning light with the Raspberry Pi Sense HAT.
- **Volume Control**: Implement adjustable volume settings for the alarm. Or maybe progressively louder volume.
- **User Interface**: Make a web interface for easier schedule and preference management.

## Contributing
If you modify this code, don't keep it a secret, make a pull request. I love seeing my code get better.

