from collections import namedtuple
from datetime import date
import threading as th
import subprocess
import json
import sys
from pathlib import Path

Detail = namedtuple('Detail', 'bit_rate sample_rate fps codec width height duration')
data = {}

def run_command(command, display_op=True):
    try:
        if display_op:
            return subprocess.check_output(command.split())
        else:
            subprocess.call(command.split(), stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError:
        print("File not found:")
        sys.exit()



def get_bit_rates(file_name, v_bit_rate, a_bit_rate):
    command = f'ffprobe -v quiet -show_streams -of json=compact=1 {file_name}'
    run = run_command(command)
    run = json.loads(run)
    for i in run['streams']:
        data[i.get('codec_type')] = Detail(
            i.get('bit_rate'),
            i.get('sample_rate'),
            i.get('r_frame_rate'),
            i.get('codec_name'),
            i.get('width'),
            i.get('height'),
            i.get('duration'),
        )
    try:
        frame, sec = data['video'].fps.split('/')
        fps = int(frame) // int(sec)
        fps -= fps * 0.05
        v_bit_rate = abs(int(int(data['video'].bit_rate) - (int(data['video'].bit_rate) * int(v_bit_rate) ) / 100))
        a_bit_rate = abs(int(int(data['audio'].bit_rate) - (int(data['audio'].bit_rate) * int(a_bit_rate) ) / 100))
        return v_bit_rate, a_bit_rate, fps
    except TypeError:
        if data['video'].bit_rate is None:
            return 0, 0, fps

def compress_video(file_name, v_bit_rate=20, a_bit_rate=5):
    o_file_name = file_name.parent / (file_name.stem + f'-{date.today()}' + file_name.suffix)
    v_bit_rate, a_bit_rate, fps = get_bit_rates(file_name, v_bit_rate, a_bit_rate)
    command = f""" ffmpeg -i {file_name} -y 
                    -vcodec {data['video'].codec} 
                    -acodec {data['audio'].codec} 
                    -b:v {v_bit_rate} 
                    -b:a {a_bit_rate} 
                    {o_file_name}"""
    run_command(command, False)
    return o_file_name


def compress_audio(file_name):
    o_file_name = file_name.parent / (file_name.stem + f'-{date.today()}.' + file_name.suffix)
    command = f""" ffmpeg -i {file_name} -y 
                    -b:a 128k
                    -ac 1
                    -ar 44100 
                    {o_file_name}"""
    run_command(command, False)


def get_audio_file(file_name):
    o_file_name = file_name.parent / (file_name.stem + f'-{date.today()}.' + file_name.suffix)
    command = f"""
        ffmpeg -i {file_name}
        -y
        -vn
        -f mp3
        {o_file_name}
    """
    run_command(command, False)

if __name__ == '__main__':
    file_name1 = 'iPhone_12_Pro_-_4K_-_video_sample_-_camera_test.mp4'
    file_name2 = 'big_bunny.mp4'
    o_file_name1 = ''.join(file_name1.split('.')[:-1]) + f'-{date.today()}.' + file_name1.split('.')[-1]
    o_file_name2 = '7.' + file_name2.split('.')[-1]
    o_file_name_mp3 = ''.join(file_name1.split('.')[:-1]) + '.mp3'


    # print(get_bit_rates(Path.cwd() / file_name1, 20, 5))
    compress_video(Path.cwd() / file_name1)
    # get_audio_file(file_name1, 'output/' + o_file_name_mp3)
    # compress_audio('output/' +  o_file_name_mp3, 'output/' +  'compress_audio.mp3')

    # t1 = th.Thread(target=compress_video, args=(file_name1, '71.mp4'))
    # t2 = th.Thread(target=compress_video, args=(file_name2, '72.mp4'))

    # t1.start()
    # t2.start()
