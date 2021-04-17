import os
import sys
import shutil
import re
from mutagen.flac import FLAC, FLACNoHeaderError
from mutagen.mp3 import EasyMP3, HeaderNotFoundError
from mutagen.apev2 import APEv2File, APENoHeaderError
from mutagen.asf import ASF, ASFHeaderError


def artist_from_fn(file_path):
    exts = ['.mp3', '.flac', 'ap3', 'lrc', 'xm', 'wma']
    ext_ok = False
    for ext in exts:
        if file[-len(ext):] == ext:
            ext_ok = True
            break
    if not ext_ok:
        return None
    file_name = os.path.basename(file_path)
    segments = file_name.split('-')
    if len(segments) > 1:
        return segments[0].strip()
    segments = file_name.split('_')
    if len(segments) > 1:
        return segments[1].strip()
    return None


def artist_from_id3(audio):
    if audio is None:
        return None
    artist = None
    try:
        artist = str(audio['albumartist'][0])
    except KeyError:
        try:
            artist = str(audio['artist'][0])
        except KeyError:
            return None
    return artist.strip()


def artist_from_audio(file):
    audio = None
    if file[-5:] == '.flac':
        try:
            audio = FLAC(file)
            return artist_from_id3(audio)
        except FLACNoHeaderError:
            pass
    elif file[-4:] == '.mp3':
        try:
            audio = EasyMP3(file)
            return artist_from_id3(audio)
        except HeaderNotFoundError:
            pass
    elif file[-4:] == '.ape':
        try:
            audio = APEv2File(file)
            return artist_from_id3(audio)
        except APENoHeaderError:
            pass
    elif file[-4:] == '.wma':
        try:
            audio = ASF(file)
            if audio is None:
                return None
            artist = None
            try:
                artist = str(audio['WM/AlbumArtist'][0])
            except KeyError:
                try:
                    artist = str(audio['Author'][0])
                except KeyError:
                    return None
            return artist.strip()
        except ASFHeaderError:
            return None
    else:
        return None


def get_artist(path_name):
    # 从音乐文件本身获取艺术家信息
    artist = artist_from_audio(path_name)
    if artist is None:
        # 从文件名获取艺术家信息
        artist = artist_from_fn(path_name)
    if artist:
        # 如果是多位艺术家合作，选第一位
        return re.split('[&,、]', artist)[0].strip()
    else:
        return None


if __name__ == "__main__":
    rootdir = 'E:\\Song'
    #rootdir = 'E:\\ChangTag'
    #rootdir = os.getcwd()
    #rootdir = '.\\Song'
    file_list = map(lambda df: os.path.join(rootdir, df), os.listdir(rootdir))
    file_list = list(filter(os.path.isfile, file_list))  # 列出文件夹下所有文件
    for file in file_list:
        print(file, 'proocessing...')
        artist_folder = get_artist(file)
        if artist_folder:
            folder = os.path.join(rootdir, artist_folder)
            # 如果目标路径不存在，构建它
            if not os.path.exists(folder):
                try:
                    os.makedirs(folder)
                except OSError:
                    folder = None
            if folder:
                # 移动文件
                try:
                    shutil.move(file, folder)
                except Exception as err:
                    print(str(err))






