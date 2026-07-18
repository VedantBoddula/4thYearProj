#coverting the videos to mp3 throught ffmpeg

import os
import subprocess
# os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

files = os.listdir("videos")
print(files)

for file in files:
    # print(file)

    tutorial_number = file.split(" #")[1].split(".mp4")[0]
    file_name = file.split(" _ Sigma Web Development Course")[0] 
    # file_name = file.split(" _ Sigma")[0]

    print(tutorial_number,file_name)
    subprocess.run(["ffmpeg", "-i", f"videos/{file}", f"audios/{tutorial_number}_{file_name}.mp3"])



