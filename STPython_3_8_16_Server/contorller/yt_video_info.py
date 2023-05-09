from STPython_3_8_16_Server.model.youtube_dl import YoutubeDL


class YtVideoInfo:

    @classmethod
    async def get_channel_all_videos_info(cls, channel_url, output_folder, subtitle_langs):
        # 获取频道上的所有播放列表
        playlists = YoutubeDL.get_playlists(channel_url)

        # 遍历播放列表并获取每个播放列表中的视频信息
        all_video_dict = {}
        for playlist in playlists:
            print(f"Fetching videos for playlist: {playlist}")
            if playlist['url'] not in all_video_dict:
                all_video_dict[playlist['url']] = []
            videos = YoutubeDL.get_videos(playlist['url'])
            all_video_dict[playlist['url']].extend(videos)

        # 输出所有视频的信息
        # pprint(all_video_dict)

        for playlist_url_, playlist_videos_ in all_video_dict.items():
            for video_ in playlist_videos_:
                print(f"Fetching subtitles for video: {video_['url']}")
                YoutubeDL.get_subtitles(video_['url'], subtitle_langs=subtitle_langs, output_folder=output_folder)


if __name__ == "__main__":
    # YtVideoInfo().get_channel_all_videos_info()
    pass