#!/usr/bin/env python3

import datetime
import time
import yaml
import logging
import subprocess
import os
import sys

YELLOW = '\033[93m'
ENDC = '\033[0m'

def debug_print(message):
    print(f"{YELLOW}{message}{ENDC}")

def log_error(message):
    logging.error(message)

def load_config():
    with open("variables.yaml", "r") as file:
        return yaml.safe_load(file)

def is_time_to_trigger(current_time, target_hour, target_minute):
    """Return True if current_time is within the 1-minute window of target."""
    trigger_start = current_time.replace(
        hour=target_hour, minute=target_minute, second=0, microsecond=0
    )
    return trigger_start <= current_time < trigger_start + datetime.timedelta(minutes=1)

def run_sequential_scripts():
    """
    Runs all scripts in the 'Sequential' folder in sorted order.
    Executes .sh with bash, .py with python3, and skips others.
    """
    debug_print("Running all scripts in Sequential folder...")
    for filename in sorted(os.listdir("Sequential")):
        script_path = os.path.join("Sequential", filename)
        if filename.endswith(".sh"):
            debug_print(f"Executing Bash script: {filename}")
            subprocess.run(["bash", script_path])
        elif filename.endswith(".py"):
            debug_print(f"Executing Python script: {filename}")
            subprocess.run(["python3", script_path])
        else:
            debug_print(f"Skipping unrecognized file type: {filename}")
    debug_print("All Sequential scripts have been executed.")

def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Check for the "-n" flag to run immediately
    run_now = ("-n" in sys.argv)
    already_triggered = False
    first_run = True  # Will let us print a "waiting" message once at start (if not -n)

    while True:
        try:
            current_time = datetime.datetime.now()
            config = load_config()

            # Determine which day's alarm we should look for
            current_day = current_time.strftime("%A").lower()
            start_time_key = f"start_time_{current_day}"

            if start_time_key not in config:
                raise Exception(f"Start time not configured for {current_day}")

            target_hour = config[start_time_key]["hour"]
            target_minute = config[start_time_key]["minute"]

            # If first run and user did not specify -n, show waiting message
            if first_run and not run_now:
                debug_print(f"Waiting for {target_hour}:{target_minute:02d} to start over.")
                first_run = False

            # If the user passed -n and we haven't run yet, do an immediate run
            if run_now and not already_triggered:
                run_sequential_scripts()
                already_triggered = True
                run_now = False  # Reset this so we don't keep triggering repeatedly
                debug_print(f"Waiting for {target_hour}:{target_minute:02d} to start over.")

            # Normal daily alarm check: trigger if it's that time
            if is_time_to_trigger(current_time, target_hour, target_minute) and not already_triggered:
                run_sequential_scripts()
                already_triggered = True
                debug_print(f"Waiting for {target_hour}:{target_minute:02d} to start over.")

            # Once we move past the alarm time by at least 1 minute, reset the trigger
            after_alarm = current_time.replace(
                hour=target_hour, minute=target_minute, second=0, microsecond=0
            )
            if current_time >= after_alarm + datetime.timedelta(minutes=1):
                already_triggered = False

            time.sleep(10)

        except Exception as e:
            log_error(f"An error occurred: {e}")
            time.sleep(10)

if __name__ == "__main__":
    main()

