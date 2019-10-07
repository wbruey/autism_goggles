python raw_to_ML_input_tobii.py

TIMEOUT 1

REM C:\ffmpeg\bin\ffmpeg -i man.avi thumb%%d.jpg -hide_banner
C:\ffmpeg\bin\ffmpeg -i mom.mp4 thumb%%d.jpg -hide_banner

TIMEOUT 1

python layer_images.py

TIMEOUT 1

REM C:\ffmpeg\bin\ffmpeg -y -r 23.975 -f image2 -s 1280x720 -i thumb%%d.jpg -vcodec libx264 -crf 25 -pix_fmt yuv420p man_soundless.mp4
C:\ffmpeg\bin\ffmpeg -y -r 30.00 -f image2 -s 1280x720 -i thumb%%d.jpg -vcodec libx264 -crf 25 -pix_fmt yuv420p mom_soundless.mp4

TIMEOUT 1

REM C:\ffmpeg\bin\ffmpeg -i man_soundless.mp4 -i man_audio.mp3 test_i_love_you_man.mp4
C:\ffmpeg\bin\ffmpeg -i mom_soundless.mp4 -i mom_audio.mp3 test_mom.mp4

TIMEOUT 1

del thumb*

python clean_up_tobii.py