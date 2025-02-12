#!/usr/bin/env python3
import subprocess

def turn_tv_off():
    """
    Uses the cec-client command to put the TV in standby mode.
    """
    subprocess.run('echo "standby 0" | cec-client -s -d 1', shell=True)

def main():
    turn_tv_off()
    print("TV is now off (standby).")

if __name__ == "__main__":
    main()

