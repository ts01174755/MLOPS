from STPython_3_8_16_Server.model.youtube_dl import YoutubeDL
from starlette.concurrency import run_in_threadpool
from fastapi import FastAPI, WebSocket
import logging
import re
import json
import asyncio

class YtVideoInfo:

    @classmethod
    async def get_channel_playlists_info(cls, channel_url, websocket: WebSocket):
        try:
            # 获取频道上的所有播放列表
            playlists = YoutubeDL.get_playlists(channel_url)

            # 遍历播放列表并获取每个播放列表中的视频信息
            all_playlist = []
            processed_videos = 0
            processed_playlists = 0
            for playlist in playlists:
                await run_in_threadpool(logging.info, f"Fetching playlist: {playlist['title']}, url: {playlist['url']}")
                videos = YoutubeDL.get_videos(playlist['url'])
                await run_in_threadpool(logging.info, f"Fetching videos: {videos}")

                playlist['all_videos'] = videos
                all_playlist.append(playlist)

                processed_videos += len(videos)
                processed_playlists += 1
                await websocket.send_text(json.dumps({"progress": processed_videos, "percent": round(processed_playlists / len(playlists), 4) * 100}))

            return all_playlist

        except Exception as e:
            logging.error(e)


    # async def get_channel_all_videos_info(cls, all_video_dict, output_folder, subtitle_langs):
    #     try:
            # # 计算总视频数
            # total_videos = 0
            # for playlist_videos_ in all_video_dict.values():
            #     total_videos += len(playlist_videos_)
            #
            # processed_videos = 0
            # # 遍历所有视频并获取字幕信息
            # for playlist_url_, playlist_videos_ in all_video_dict.items():
            #     # 遍历播放列表中的所有视频
            #     for video_ in playlist_videos_:
            #         await run_in_threadpool(logging.info, f"Fetching subtitles for video: {video_['url']}")
            #         subtitle_filenames = YoutubeDL.get_subtitles(video_['url'], subtitle_langs=subtitle_langs, output_folder=output_folder)
            #
            #         # 使用正則表達式匹配字幕文件名
            #         subtitle_filenames = re.findall(r'/[^/]+\.vtt', "_".join(subtitle_filenames))
            #
            #         # 從完整路徑中提取文件名
            #         subtitle_filenames = [filename.split('/')[-1] for filename in subtitle_filenames]
            #         video_[f'subtitle_filenames'] = subtitle_filenames
            #
            #         # 更新進度
            #         processed_videos += 1
            #         progress = (processed_videos / total_videos) * 100
            #         await websocket.send_text(json.dumps({"progress": round(progress, 2)}))
            #         await run_in_threadpool(websocket.close)  # Add this line to flush the output buffer
            #
            # # 输出所有视频的信息
            # logging.info(all_video_dict)
            # return all_video_dict

        # except Exception as e:
        #     logging.error(e)

    @classmethod
    async def insert_document_mongdb(cls, mongoDBCtrl, collection, document):
        mongoDBCtrl.insert_document(collection, document)
        return 'success'


if __name__ == "__main__":
    # YtVideoInfo().get_channel_all_videos_info()
    pass