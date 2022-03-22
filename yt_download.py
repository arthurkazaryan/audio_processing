import os
import sys
from pytube import YouTube
from pydub import AudioSegment
from pathlib import Path
from settings import paths_data


def download(links: list):

    links_paths = []
    for link in links:
        yt = YouTube(link)

        audio = yt.streams.filter(only_audio=True).first()
        out_file = audio.download(paths_data.yt_folder)

        base, ext = os.path.splitext(out_file)
        mp3_file = Path('_'.join([x.lower() for x in base.split(' ')]) + '.mp3')
        wav_file = Path('_'.join([x.lower() for x in base.split(' ')]) + '.wav')

        if not mp3_file.is_file():
            os.rename(out_file, mp3_file)
        audio = AudioSegment.from_file(str(mp3_file))
        audio.export(wav_file, format='wav')
        mp3_file.unlink()
        links_paths.append(str(wav_file))

    return links_paths


if __name__ == '__main__':

    download(sys.argv[1:])
