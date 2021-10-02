import xml.etree.ElementTree as ET
from xml.dom import minidom

# def subElement(root, tag, text):
#     ele = ET.SubElement(root, tag)
#     ele.text = text
#     return ele


def save_xml(root, filename):
    rawText = ET.tostring(root)
    dom = minidom.parseString(rawText)
    with open(filename, 'w', encoding="utf-8") as f:
        dom.writexml(f, indent="\t", addindent="\t", newl="\n")

def create_xml(seq_data, clips, file_name):
    root = ET.Element("xmeml")
    root.set("version", "4")
    
    sequence = ET.SubElement(root, "sequence")
    sequence.set("id", "sequence-1")
    
    seq_duration = ET.SubElement(sequence, "duration")
    seq_duration.text = seq_data["duration"]
    
    rate = ET.SubElement(sequence, "rate")
    timebase = ET.SubElement(rate, "timebase")
    timebase.text = seq_data["fps"]
    ntsc = ET.SubElement(rate, "ntsc")
    ntsc.text = "FALSE"
    
    seq_name = ET.SubElement(sequence, "name")
    seq_name.text = seq_data["name"]
    
    # media 开始
    media = ET.SubElement(sequence, "media")
    # video 开始
    video = ET.SubElement(media, "video")
    format = ET.SubElement(video, "format")
    samplecharacteristics = ET.SubElement(format, "samplecharacteristics")
    samplecharacteristics.append(rate)
    
    width = ET.SubElement(samplecharacteristics, "width")
    width.text = seq_data["size"][0]
    height = ET.SubElement(samplecharacteristics, "height")
    height.text = seq_data["size"][1]
    anamorphic = ET.SubElement(samplecharacteristics, "anamorphic")
    anamorphic.text = "FALSE"
    ratio = ET.SubElement(samplecharacteristics, "pixelaspectratio")
    ratio.text = "square"
    
    # track 开始
    track = ET.SubElement(video, "track")
    for i in range(len(clips)):
        num = str(i+1)
        audio_num = str(i+len(clips)+1)
        
        
        clip = clips[i]
        clipitem = ET.SubElement(track, "clipitem")
        clipitem.set("id", "clipitem-" + num)
        
        name = ET.SubElement(clipitem, "name")
        name.text = seq_data["file_path"].split('/')[-1]
        
        enabled = ET.SubElement(clipitem, "enabled")
        enabled.text = "TRUE"
        
        raw_duration = ET.SubElement(clipitem, "duration")
        raw_duration.text = clip["raw_duration"]
        
        clipitem.append(rate)
        
        start = ET.SubElement(clipitem, "start")
        start.text = clip["start"]
        end = ET.SubElement(clipitem, "end")
        end.text = clip["end"]
        raw_in = ET.SubElement(clipitem, "in")
        raw_in.text = clip["in"]
        raw_out = ET.SubElement(clipitem, "out")
        raw_out.text = clip["out"]
        
        alpha = ET.SubElement(clipitem, "alphatype")
        alpha.text = "none"
        
        clipitem.append(ratio)
        clipitem.append(anamorphic)
        
        # file 开始
        file = ET.SubElement(clipitem, "file")
        file.set("id", "file-1")
        if i == 0:
            file.append(name)
            
            path = ET.SubElement(file, "pathurl")
            path.text = seq_data["file_path"]
            
            file.append(rate)
            file.append(raw_duration)
            
            timecode = ET.SubElement(file, "timecode")
            timecode.append(rate)
            
            string = ET.SubElement(timecode, "string")
            string.text = "00:00:00:00"
            
            frame = ET.SubElement(timecode, "frame")
            frame.text = "0"
            
            displayformat = ET.SubElement(timecode, "displayformat")
            displayformat.text = "NDF"
            
            # media 开始
            file_media = ET.SubElement(file, "media")
            video = ET.SubElement(file_media, "video")
            video.append(samplecharacteristics)
            
            audio = ET.SubElement(file_media, "audio")
            audio_samplecharacteristics = ET.SubElement(audio, "samplecharacteristics")
            depth = ET.SubElement(audio_samplecharacteristics, "depth")
            depth.text = "16"
            samplerate = ET.SubElement(audio_samplecharacteristics, "samplerate")
            samplerate.text = "48000"
            channel = ET.SubElement(audio, "channel")
            channel.text = "2"
        
        # 音视频链接
        link = ET.SubElement(clipitem, "link")
        linkclipref = ET.SubElement(link, "linkclipref")
        linkclipref.text = "clipitem-"+ num
        mediatype = ET.SubElement(link, "mediatype")
        mediatype.text = "video"
        trackindex = ET.SubElement(link, "trackindex")
        trackindex.text = "1"
        clipindex = ET.SubElement(link, "clipindex")
        clipindex.text = num
        
        link = ET.SubElement(clipitem, "link")
        linkclipref = ET.SubElement(link, "linkclipref")
        linkclipref.text = "clipitem-" + audio_num
        mediatype = ET.SubElement(link, "mediatype")
        mediatype.text = "audio"
        trackindex = ET.SubElement(link, "trackindex")
        trackindex.text = "1"
        clipindex = ET.SubElement(link, "clipindex")
        clipindex.text = num
        
    # audio 开始
    audio = ET.SubElement(media, "audio")
    
    numOutputChannels = ET.SubElement(audio, "numOutputChannels")
    numOutputChannels.text = "2"
    
    format = ET.SubElement(audio, "format")
    audio_samplecharacteristics = ET.SubElement(format, "samplecharacteristics")
    depth = ET.SubElement(audio_samplecharacteristics, "depth")
    depth.text = "16"
    samplerate = ET.SubElement(audio_samplecharacteristics, "samplerate")
    samplerate.text = "48000"
    
    # audio_track 开始
    track = ET.SubElement(audio, "track")
    for i in range(len(clips)):
        num = str(i+1)
        audio_num = str(i+len(clips)+1)
        
        clip = clips[i]
        clipitem = ET.SubElement(track, "clipitem")
        clipitem.set("id", "clipitem-"+ audio_num)
        clipitem.set("premiereChannelType", "stereo")
        
        name = ET.SubElement(clipitem, "name")
        name.text = seq_data["file_path"].split('/')[-1]
        
        enabled = ET.SubElement(clipitem, "enabled")
        enabled.text = "TRUE"
        
        raw_duration = ET.SubElement(clipitem, "duration")
        raw_duration.text = clip["raw_duration"]
        
        clipitem.append(rate)
        
        start = ET.SubElement(clipitem, "start")
        start.text = clip["start"]
        end = ET.SubElement(clipitem, "end")
        end.text = clip["end"]
        raw_in = ET.SubElement(clipitem, "in")
        raw_in.text = clip["in"]
        raw_out = ET.SubElement(clipitem, "out")
        raw_out.text = clip["out"]
        
        file = ET.SubElement(clipitem, "file")
        file.set("id", "file-1")
        
        sourcetrack = ET.SubElement(clipitem, "sourcetrack")
        mediatype = ET.SubElement(sourcetrack, "mediatype")
        mediatype.text = "audio"
        trackindex = ET.SubElement(sourcetrack, "trackindex")
        trackindex.text = "1"
    

    # subElement(root, "from", "marry")
    # subElement(root, "heading", "Reminder")
    # subElement(root, "body", "Don't forget the meeting!")

    # 保存xml文件
    save_xml(root, file_name)

if __name__ == "__main__":
    clip1 = {
    "raw_duration": "178321",
    "start": "0", #在序列中的位置
    "end": "275", 
    "in": "15531", #在原视频中的入点出点
    "out": "15806",
    }

    clip2 = {
        "raw_duration": "178321",
        "start": "275", 
        "end": "982", 
        "in": "15806", 
        "out": "16513",
    }

    clip3 = {
        "raw_duration": "178321",
        "start": "982", 
        "end": "3187", 
        "in": "16513", 
        "out": "18718",
    }

    clip4 = {
        "raw_duration": "178321",
        "start": "3187", 
        "end": "4701", 
        "in": "18718", 
        "out": "20232",
    }

    clips = []
    
    clips.append(clip1)
    clips.append(clip2)
    clips.append(clip3)
    clips.append(clip4)


    seq_data = {
        "fps": "24",
        "duration": "4701",
        "name": "第一次聚餐",
        "size": ["1920", "1080"],
        "file_path": r"file://localhost/G%3a/Documents/%e7%a0%94%e7%a9%b6%e7%94%9f/%e9%95%9c%e5%a4%b4%e8%af%ad%e8%a8%80%e7%a0%94%e7%a9%b6/%e9%a5%ae%e9%a3%9f%e7%94%b7%e5%a5%b3/218644200-1-112.mp4",
        "clips": clips,
    }
    
    create_xml(seq_data, clips, "test.xml")
    

    