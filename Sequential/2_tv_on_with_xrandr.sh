#!/bin/bash

# Set the DISPLAY variable
export DISPLAY=:0


echo 'as' | cec-client -s -d 1

sleep 25

# Find connected HDMI display
HDMI_OUTPUT=$(xrandr | grep " connected" | grep HDMI | cut -d" " -f1)

# If HDMI_OUTPUT is not empty, then proceed
if [ ! -z "$HDMI_OUTPUT" ]; then
    # Turn off HDMI output
    xrandr --output $HDMI_OUTPUT --off

    # Wait a bit
    sleep 1

    # Turn on HDMI output and set preferred mode
    xrandr --output $HDMI_OUTPUT --auto
else
    echo "No HDMI output found."
fi

