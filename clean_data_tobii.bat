python raw_to_ML_input_tobii.py

TIMEOUT 1

C:\ffmpeg\bin\ffmpeg -i man.avi thumb%%d.jpg -hide_banner
REM C:\ffmpeg\bin\ffmpeg -i dotstaticsmall.mp4 thumb%%d.jpg -hide_banner
REM C:\ffmpeg\bin\ffmpeg -i dotcircle.mp4 thumb%%d.jpg -hide_banner

TIMEOUT 1

python layer_images.py

TIMEOUT 1

C:\ffmpeg\bin\ffmpeg -y -r 23.975 -f image2 -s 1280x720 -i thumb%%d.jpg -vcodec libx264 -crf 25 -pix_fmt yuv420p man_soundless.mp4
REM C:\ffmpeg\bin\ffmpeg -y -r 23.975 -f image2 -s 1280x720 -i thumb%%d.jpg -vcodec libx264 -crf 25 -pix_fmt yuv420p dotchase.mp4

TIMEOUT 1

C:\ffmpeg\bin\ffmpeg -i man_soundless.mp4 -i man_audio.mp3 test_i_love_you_man.mp4

TIMEOUT 1

del thumb*

python clean_up_tobii.py