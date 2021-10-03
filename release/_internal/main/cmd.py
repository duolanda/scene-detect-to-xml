import subprocess as sp
import os

#########################
# 修改 exe 信息
sd_path = './_internal/python-3.6.8/Scripts/scenedetect.exe'
python_path = os.path.abspath('./_internal/python-3.6.8/python.exe')


# 二进制读写文件
with open(sd_path, 'rb+') as bin_file:
    bytes_str = bin_file.read()
    # print(bytes_str)
    # 字符串前面有加上b，转为bytes类型
    try: 
        bytes_str = bytes_str.replace(b'd:\\anaconda3\\python.exe', python_path.encode('utf-8'))
        # print(bytes_str)
        # 定位到文件开头
        bin_file.seek(0)
        # bin_file.truncate() # 清空文件
        bin_file.write(bytes_str)
        bin_file.flush()
    except:
        pass
    
#########################
# 调用命令行生成视频


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