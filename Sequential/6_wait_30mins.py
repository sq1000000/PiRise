import time

# Set the countdown duration (in seconds)
countdown_time = 30 * 60  # 30 minutes

print(f"Waiting 30 minutes ({countdown_time} seconds)")

# Countdown loop
for remaining in range(countdown_time, 0, -1):
    mins, secs = divmod(remaining, 60)
    timer = f"{mins}:{secs:02}"  # Format as M:SS
    print(f"\r{timer}", end="")  # Overwrite the line
    time.sleep(1)

print("\nDone!")

