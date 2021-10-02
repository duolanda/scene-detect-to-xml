from scenedetect import VideoManager
from scenedetect import SceneManager
from scenedetect.detectors import ContentDetector

import os 

def find_scenes(video_path, threshold=30.0):
    video_manager = VideoManager([video_path])
    scene_manager = SceneManager()
    scene_manager.add_detector(
        ContentDetector(threshold=threshold))

    video_manager.set_downscale_factor()

    video_manager.start()
    scene_manager.detect_scenes(frame_source=video_manager)

    return scene_manager.get_scene_list()