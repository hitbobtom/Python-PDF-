import os
from moviepy.editor import VideoFileClip


def split_video(input_file):
    video = VideoFileClip(input_file)  # 加载视频文件
    duration = video.duration  # 获取视频总时长
    clips = []  # 创建一个空列表，用于存储裁剪后的视频片段

    for i in range(0, int(duration), 1200):  # 以20分钟（单位：秒）为间隔循环裁剪视频
        start_time = i  # 计算每个片段的起始时间
        end_time = min(i + 1200, duration)  # 计算每个片段的结束时间，最长为视频总时长
        sub_clip = video.subclip(start_time, end_time)  # 裁剪视频片段
        clips.append(sub_clip)  # 将裁剪后的片段添加到列表中

    for i, clip in enumerate(clips):  # 遍历裁剪后的视频片段列表
        output_file = f"{input_file[:-4]}_{i + 1}.mp4"  # 生成输出文件名，保留原始文件名并加上序号
        clip.write_videofile(output_file, codec="libx264", fps=24)  # 将视频片段导出为mp4格式文件


def process_all_videos(folder_path):
    for file in os.listdir(folder_path):  # 获取文件夹中所有文件
        if file.endswith(".mp4"):  # 确保文件是视频文件
            file_path = os.path.join(folder_path, file)  # 构建完整的文件路径
            split_video(file_path)  # 调用之前定义的函数处理每个视频文件

if __name__ == "__main__":
    # 使用示例，假设视频文件都在名为 "videos" 的文件夹中
    process_all_videos("videos")
