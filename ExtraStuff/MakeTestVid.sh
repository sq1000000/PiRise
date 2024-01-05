#!/bin/bash

echo "Select the resolution for the test video:"
echo "1) 480p (Standard Definition)"
echo "2) 720p (HD)"
echo "3) 1080p (Full HD)"
echo "4) 1440p (Quad HD)"
echo "5) 4K (Ultra HD)"
echo "6) 8K (Super Ultra HD)"
read -p "Enter your choice (1/2/3/4/5/6): " choice

filename="latest_video.webm"

case $choice in
    1)
        resolution="640x480"
        ;;
    2)
        resolution="1280x720"
        ;;
    3)
        resolution="1920x1080"
        ;;
    4)
        resolution="2560x1440"
        ;;
    5)
        resolution="3840x2160"
        ;;
    6)
        resolution="7680x4320"
        ;;
    *)
        echo "Invalid choice."
        exit 1
        ;;
esac

ffmpeg -f lavfi -i testsrc=size=$resolution:rate=30 -f lavfi -i sine=frequency=1000 -t 10 -c:v libvpx -pix_fmt yuv420p -c:a libvorbis $filename

echo "Test video generated: $filename"