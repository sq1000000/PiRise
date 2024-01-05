vfi -i testsrc=size=3840x2160:rate=30 -f lavfi -i sine=frequency=1000 -t 10 -c:v libvpx -pix_fmt yuv420p -c:a libvorbis latest_video_4k.webm
