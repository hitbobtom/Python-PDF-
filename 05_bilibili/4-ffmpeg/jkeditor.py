# jkeditor.py
# coding:utf-8
import sys
import os
import re
import shutil
import subprocess
from datetime import datetime, timedelta
import time

TIME_FROMAT = '%H:%M:%S'

from moviepy.editor import VideoFileClip

def get_video_duration(file_path):
    video = VideoFileClip(file_path)
    duration = video.duration
    video.close()
    return duration

def do_cut(file_input, file_output, s1_time, s2_time):
    start_time = s1_time.strftime(TIME_FROMAT)
    end_time = s2_time.strftime(TIME_FROMAT)
    cmd = '4-ffmpeg -i ' + file_input + ' -ss ' + start_time + ' -to ' + end_time + '  -c:v copy -c:a copy ' + file_output
    print("cmd=", cmd)
    subprocess.call(cmd, shell=True)


def do_edit():
    file_input = sys.argv[1]
    output_dir = sys.argv[2]
    start_time = sys.argv[3]
    # end_time = sys.argv[4]
    print(get_video_duration(file_input))
    # end_time = datetime.timedelta(seconds=get_video_duration(file_input)).strftime(TIME_FROMAT)
    end_time = time.strftime(TIME_FROMAT, time.gmtime(get_video_duration(file_input)))
    print(end_time)
    slice_duration = int(sys.argv[4])
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.mkdir(output_dir)
    (filepath, tempfilename) = os.path.split(file_input)
    (filename, extension) = os.path.splitext(tempfilename)

    s_time = datetime.strptime(start_time, TIME_FROMAT)
    e_time = datetime.strptime(end_time, TIME_FROMAT)
    n_slice = (int)((e_time - s_time).total_seconds() / slice_duration) + 1
    print("n_slice=", n_slice)

    s1_time = s_time
    for i in range(0, n_slice):
        s2_time = s1_time + timedelta(seconds=slice_duration)
        file_output = output_dir + '/' + filename + str(i) + extension
        do_cut(file_input, file_output, s1_time, s2_time)
        s1_time = s2_time


def usage():
    print("usage:", sys.argv[0], "<input> <output_dir> <start_time> <end_time> <slice_duration>")
    exit(0)


if __name__ == "__main__":
    if len(sys.argv) != 5:
        usage()
    else:
        do_edit()
