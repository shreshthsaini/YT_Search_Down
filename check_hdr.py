""" 
    Checking the metadata of video file to verify if it is HDR or not.

    - Shreshth Saini, 2022
"""


import subprocess
import json
import os
import argparse
#--------------------------------------------------------------*****--------------------------------------------------------------#

def is_video_hdr(video_path):
    """
    Check if the video at the given path is HDR.
    
    Args:
    - video_path (str): The path to the video file.
    
    Returns:
    - bool: True if the video is HDR, False otherwise.
    """
    cmd = [
        "ffprobe", 
        "-v", "error", 
        "-show_streams",
        "-select_streams", "v:0",
        "-print_format", "json",
        video_path
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    try:
        video_info = json.loads(result.stdout)
    except json.JSONDecodeError:
        print(f"Failed to decode JSON: {result.stdout}")
        
        return False
    print(video_info)
    video_stream = video_info["streams"][0]

    # Checking some common HDR indicators in the metadata
    # This can be extended based on more specific requirements
    if ("color_transfer" in video_stream and video_stream["color_transfer"] == "smpte2084") or \
       ("color_space" in video_stream and video_stream["color_space"] in ["bt2020nc", "bt2020c"]) or \
       ("bits_per_raw_sample" in video_stream and int(video_stream["bits_per_raw_sample"]) > 8):
        return True

    return False

#--------------------------------------------------------------*****--------------------------------------------------------------#
""" 
    Main Function
"""
def main(path):
    # check if path is folder or a file 
    if os.path.isdir(path):
        vid_list = os.listdir(path)
        video_path = [os.path.join(path,v) for v in vid_list if v.split('.')[-1] in ['mp4', 'mkv', 'mov', 'webm']]
    else:
        video_path = [path]

    for v in video_path:
        print(f"Checking {v}...")
        if is_video_hdr(v):
            print(f"{v} is HDR.")
        else:
            print(f"{v} is not HDR.")

        #also print all meta data of video file 
        cmd = [
            "ffprobe", 
            "-v", "error", 
            "-show_streams",
            "-select_streams", "v:0",
            "-print_format", "json",
            v
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        video_info = json.loads(result.stdout)
        #save in json file in same folder
        with open(v.split('.')[0] + '.json', 'w') as f:
            json.dump(video_info, f, indent=4)

#--------------------------------------------------------------*****--------------------------------------------------------------#

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--video_root", type=str, default="sample_hdr_shorts/")
    args = parser.parse_args()
    video_root = args.video_root
    main(video_root)

