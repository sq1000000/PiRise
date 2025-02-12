ffmpeg -f lavfi -i testsrc=size=2560x1440:rate=30 -f lavfi -i sine=frequency=1000 -t 10 -c:v libvpx -pix_fmt yuv420p -c:a libvorbis latest_video_1440p.webm
