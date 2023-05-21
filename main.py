#!/usr/bin/env python3

import glob
import os
import pprint
import subprocess
import sys
import time

import anthropic
import jsonpickle
import yt_dlp
from dotenv import load_dotenv
from IPython import embed


class Summarizer:
    def __init__(self):
        pass

    def download_subtitle(self, video_url):
        command = [
            'yt-dlp',
            '--write-subs',
            '--skip-download',
            '--sub-format',
            'vtt',
            # '--sub-langs',
            # 'en',
            video_url
        ]

        subprocess.run(command)

        # Find the downloaded .vtt file
        for file in os.listdir('.'):
            if file.endswith('.vtt'):
                # Read the file
                with open(file, 'r') as f:
                    content = f.read()

                # Delete the file
                os.remove(file)

                # Return the content
                return content

        return None

    def claude_sum(self, input_subs, max_tokens_to_sample: int = 20000):
        load_dotenv()
        anthropic_api_key = os.environ['ANTHROPIC_API_KEY']
        c = anthropic.Client(api_key=anthropic_api_key)

        # input_file = 'subtitles.vtt'

        # with open(input_file) as f:
        #     lines = f.readlines()

        # concatenated_lines = ''

        # for line in lines:
        #     concatenated_lines += line.strip() + '\n'

        user_input = 'Summarize this video transcript and suggest using json what parts of the video are ambigous that you would benefit by having frame descriptions from\n below is the transcript \n'

        user_input += input_subs

        response = c.completion_stream(
            prompt=f'{anthropic.HUMAN_PROMPT} {user_input}{anthropic.AI_PROMPT}',
            stop_sequences=[anthropic.HUMAN_PROMPT],
            max_tokens_to_sample=max_tokens_to_sample,
            model='claude-v1.3-100k',
            stream=True,
        )
        for data in response:
            os.system('clear')
            print(f'prompt: {user_input}')
            print()
            print(data['completion'][1:])
        print()

        if data['stop_reason'] != 'stop_sequence':
            print(f'stop_reason: {data["stop_reason"]}')

        print()
        print()

    def main(self):
        if len(sys.argv) != 2:
            print("Usage: python script.py <video_url>")
            return

        video_url = sys.argv[1]
        subtitle_content = self.download_subtitle(video_url)

        if subtitle_content:
            self.claude_sum(subtitle_content)
        else:
            print("No subtitle file found.")

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
    # summarizer.setup_dirs()
    # link = 'https://www.youtube.com/watch?v=Yf1o0TQzry8'
    # summarizer.run(link)
    summarizer.main()
