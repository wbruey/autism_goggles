python raw_to_ML_input.py

TIMEOUT 1

C:\ffmpeg\bin\ffmpeg -i dotstatic.mp4 thumb%%d.jpg -hide_banner

TIMEOUT 1

python layer_images.py

TIMEOUT 1

C:\ffmpeg\bin\ffmpeg -y -r 23.975 -f image2 -s 1280x720 -i thumb%%d.jpg -vcodec libx264 -crf 25 -pix_fmt yuv420p dotchase.mp4

TIMEOUT 1

del thumb*