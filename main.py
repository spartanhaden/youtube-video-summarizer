#!/usr/bin/env python3

import pprint
import glob
import jsonpickle
import time
import os

from dotenv import load_dotenv
from IPython import embed
import yt_dlp

class Summarizer:
    def __init__(self):
        pass

    def setup_dirs(self):
        # make downloads dir if not exists
        if not os.path.exists('downloads'):
            os.makedirs('downloads')

        # make processed-medium dir if not exists
        if not os.path.exists('processed-medium'):
            os.makedirs('processed-medium')

    def download_audio(self, link):
        # chdir to downloads
        os.chdir('downloads')

        URLS = ['https://www.youtube.com/watch?v=BaW_jenozKc']

        ydl_opts = {
            'format': 'm4a/bestaudio/best',
            # ℹ️ See help(yt_dlp.postprocessor) for a list of available Postprocessors and their arguments
            'postprocessors': [{  # Extract audio using ffmpeg
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'm4a',
            }]
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            error_code = ydl.download([link])

    def get_text(self):
        # run the downloaded audio through the whisper model with medium settings

        # save the output to downloads
        pass

    def run(self, link):
        self.download_audio(link)
        # self.get_text()
        # save the output to processed-medium


if __name__ == '__main__':
    summarizer = Summarizer()
    summarizer.setup_dirs()
    link = 'https://www.youtube.com/watch?v=Yf1o0TQzry8'
    summarizer.run(link)
