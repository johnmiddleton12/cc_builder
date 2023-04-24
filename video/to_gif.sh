ffmpeg -y \
    -ss 00:00:30.000 \
    -to 00:03:46.000 \
    -i screencap.mov \
    -filter_complex "fps=10,setpts=PTS/10" \
    -pix_fmt rgb24 \
    -r 10 \
    -s 1280x800 \
    -loop 0 \
    output.gif

# -t 00:00:20.000 \

convert -layers Optimize output.gif output_optimized.gif

# ffplay output_optimized.gif
