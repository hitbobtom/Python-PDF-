from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip


# 定义视频文件路径
video_path = "input.mp4"

# 定义切割时间范围（单位为秒）
start_time = 10
end_time = 20

# 设置输出文件名
output_path = "output.mp4"


if __name__ == "__main__":
    # 调用ffmpeg_extract_subclip函数切割视频
    ffmpeg_extract_subclip(video_path, start_time, end_time, targetname=output_path)
