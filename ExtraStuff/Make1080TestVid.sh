ffmpeg -f lavfi -i testsrc=size=1920x1080:rate=30 -f lavfi -i sine=frequency=1000 -t 10 -c:v libvpx -pix_fmt yuv420p -c:a libvorbis latest_video.webm
