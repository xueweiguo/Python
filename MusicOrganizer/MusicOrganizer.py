import os
from mutagen.flac import FLAC
from mutagen.mp3 import EasyMP3

if __name__ == "__main__":
    rootdir = '.\Song'
    file_list = os.listdir(rootdir)  # 列出文件夹下所有的目录与文件

    for file in file_list:
        path = os.path.join(rootdir, file)
        if path[-5:] == '.flac':
            audio = FLAC(path)
        elif path[-4:] == '.mp3':
            audio = EasyMP3(path)
        else:
            audio = None
        print(audio)


