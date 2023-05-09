from STPython_3_8_16_Server.model.youtube_dl import YoutubeDL
import logging
from pprint import pprint
import re

class YtVideoInfo:

    @classmethod
    async def get_channel_all_videos_info(cls, channel_url, output_folder, subtitle_langs):
        try:
            # 获取频道上的所有播放列表
            playlists = YoutubeDL.get_playlists(channel_url)

            # 遍历播放列表并获取每个播放列表中的视频信息
            all_video_dict = {}
            for playlist in playlists:
                logging.info(f"Fetching videos for playlist: {playlist}")
                if playlist['url'] not in all_video_dict:
                    all_video_dict[playlist['url']] = []
                videos = YoutubeDL.get_videos(playlist['url'])
                all_video_dict[playlist['url']].extend(videos)

            for playlist_url_, playlist_videos_ in all_video_dict.items():
                for video_ in playlist_videos_:
                    logging.info(f"Fetching subtitles for video: {video_['url']}")
                    subtitle_filenames = YoutubeDL.get_subtitles(video_['url'], subtitle_langs=subtitle_langs, output_folder=output_folder)

                    # 使用正則表達式匹配字幕文件名
                    subtitle_filenames = re.findall(r'/[^/]+\.vtt', "_".join(subtitle_filenames))

                    # 從完整路徑中提取文件名
                    subtitle_filenames = [filename.split('/')[-1] for filename in subtitle_filenames]

                    video_[f'subtitle_filenames'] = subtitle_filenames

            # 输出所有视频的信息
            logging.info(all_video_dict)

        except Exception as e:
            logging.error(e)


if __name__ == "__main__":
    # YtVideoInfo().get_channel_all_videos_info()
    pass