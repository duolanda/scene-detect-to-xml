import os
from PIL import Image
import numpy as np

from scene_cut import find_scenes

class Clip:
    def __init__(self, id, length=None, color=None):
        self.id = id
        self.length = length
        self.color = color

def draw_palette(clip_list):
    width = 1000
    height = 430
    split_line_width = 5
    
    
    split_line = split_line_width * (len(clip_list)-1)
    canvas = np.zeros((height, width+split_line, 3), dtype='uint8')

    total_length = 0
    for clip in clip_list:
        total_length += clip.length
    
    i = 0
    for clip in clip_list:
        length = int(width*clip.length/total_length)
        canvas[0:height, i:i+length] = np.asarray(clip.color)
        i = i + length
        
        if (i+split_line_width) < canvas.shape[1]: #最后一个片段不加分割线
            canvas[0:height, i:i+split_line_width] = np.asarray([255, 255, 255])
            i = i + split_line_width
    
    output = Image.fromarray(canvas)
    output.save('image.jpg')


if __name__ == "__main__":
    all_files = os.listdir(os.getcwd())
    for file in all_files:
        if file[-3:] in ['mp4', 'mov', "MP4", "MOV"]:
            video_path = os.path.abspath(file)
    
    clips_list = []
    scenes = find_scenes(video_path, save_csv=True)
    for i in range(len(scenes)):
        scene = scenes[i]
        clip = Clip(i, scene[1].frame_num - scene[0].frame_num, [211, 82, 48])
        clips_list.append(clip)
        
    draw_palette(clips_list)
    