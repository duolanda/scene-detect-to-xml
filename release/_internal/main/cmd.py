import subprocess as sp
import os

video_folder = './workspace/'
output_dir = video_folder + '/output/'


video_list = []
all_files = os.listdir(video_folder)
for file in all_files:
    if file[-3:] in ['mp4', 'mov', "MP4", "MOV"]:
        video_list.append(os.path.abspath(video_folder+file))

for video_path in video_list:
    sd_command = ['scenedetect',
            '--input', video_path,
            '--output', output_dir,
            'detect-content',
            # 'list-scenes',
            # 'save-images',
            'split-video',
            ]


    p = sp.Popen(sd_command, stdin=sp.PIPE) 
    while True:
        if p.poll() != None:
            print("视频片段已生成！")
            break