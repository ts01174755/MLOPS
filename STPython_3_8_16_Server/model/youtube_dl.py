import json
import subprocess
import re

class YoutubeDL:

    @classmethod
    def get_playlists(cls, channel_url):
        playlists_command = [
            "youtube-dl",
            "--flat-playlist",
            "--skip-download",
            "--dump-json",
            channel_url,
        ]

        playlists_output = subprocess.run(playlists_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        json_objects = playlists_output.stdout.strip().split("\n")

        playlists = []
        for json_obj in json_objects:
            playlists.append(json.loads(json_obj))

        return playlists

    @classmethod
    def get_videos(cls, video_url):
        videos_command = [
            "youtube-dl",
            "--flat-playlist",
            "--skip-download",
            "--dump-json",
            video_url,
        ]
        videos_output = subprocess.run(videos_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        json_objects = videos_output.stdout.strip().split("\n")

        videos = []
        for json_obj in json_objects:
            if json_obj:
                videos.append(json.loads(json_obj))

        return videos

    @classmethod
    def get_subtitles(cls, video_url, subtitle_langs, output_folder):
        subtitles_command = [
            "youtube-dl",
            "--skip-download",
            "--write-sub",
            f"--sub-lang {subtitle_langs}",
            f"-o '{output_folder}/%(title)s-%(id)s.%(ext)s'",
            video_url,
        ]
        cmd_str = " ".join(subtitles_command)
        subtitles_output = subprocess.run(cmd_str, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # 提取字幕檔案名稱
        subtitle_filenames = []

        if subtitles_output.stdout:
            for line in subtitles_output.stdout.strip().split("\n"):
                if re.search(r'\.(vtt|srt)$', line):
                    subtitle_filenames.append(line)

        return subtitle_filenames