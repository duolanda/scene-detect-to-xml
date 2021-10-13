from scenedetect import VideoManager
from scenedetect import SceneManager
from scenedetect.scene_manager import write_scene_list

from scenedetect.detectors import ContentDetector

import os 
import cv2

from xml_creator import create_xml

def find_scenes(video_path, threshold=30.0, save_csv=False):
    video_manager = VideoManager([video_path])
    scene_manager = SceneManager()

    scene_manager.add_detector(
        ContentDetector(threshold=threshold))

    video_manager.set_downscale_factor()

    video_manager.start()
    scene_manager.detect_scenes(frame_source=video_manager)
    
    scene_list = scene_manager.get_scene_list()
    
    if save_csv:
        csv_file_path = '%s.csv' % video_path
        with open(csv_file_path, 'w') as csv_file:
            write_scene_list(csv_file, scene_list)

    return scene_list


if __name__ == "__main__":
    video_list = []
    all_files = os.listdir(os.getcwd())
    for file in all_files:
        if file[-3:] in ['mp4', 'mov', "MP4", "MOV"]:
            video_list.append(os.path.abspath(file))
    
    seq_data_list = []
    for video_path in video_list:
        seq_data = {}
        cap = cv2.VideoCapture(video_path)
        seq_data["fps"] = str(round(cap.get(cv2.CAP_PROP_FPS))) 
        seq_data["duration"] = str(round(cap.get(cv2.CAP_PROP_FRAME_COUNT)))
        seq_data["name"] = video_path.split('\\')[-1][0:-4]
        seq_data["size"] = [str(round(cap.get(cv2.CAP_PROP_FRAME_WIDTH))), str(round(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))]
        seq_data["file_path"] = "file://localhost/" + video_path.replace('\\', '/')
        
        clips = []
        scenes = find_scenes(video_path)
        for scene in scenes:
            clip = {}
            clip["raw_duration"] = seq_data["duration"]
            clip["start"] = clip["in"] = str(scene[0].frame_num)
            clip["end"] = clip["out"] = str(scene[1].frame_num)
            clips.append(clip)
        
        seq_data["clips"] = clips
        seq_data_list.append(seq_data)
    
    for seq_data in seq_data_list:
        create_xml(seq_data, seq_data["name"]+".xml")
    
    
    