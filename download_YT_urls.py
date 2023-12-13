import os 
import subprocess
import pandas as pd 
import numpy as np
from tqdm import tqdm
from joblib import Parallel, delayed
from glob import glob
import argparse

#--------------------------------------------------------------*****--------------------------------------------------------------#
""" 
    Obtaining the key for the highest video quality for the given url 

"""

def get_best_mp4_format(url): # sometimes MP4 does not contain any metadata 
    command = ["yt-dlp", "-F", url]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    
    if result.returncode != 0:
        print(f"Failed to get formats: {result.stderr}")
        return None

    best_format = None
    for line in result.stdout.split("\n"):
        if line.strip():
            if "mp4" in line:
                best_format = line.split()[0]
    
    return best_format

def get_best_format(url):
    command = ["yt-dlp", "-F", url]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    
    if result.returncode != 0:
        print(f"Failed to get formats: {result.stderr}")
        return None

    best_format = None
    for line in result.stdout.split("\n"):
        if line.strip():
            best_format = line.split()[0]
    return best_format

#--------------------------------------------------------------*****--------------------------------------------------------------#
""" 
    Core function to download the video from the url and save it in the folder
"""
def download_video(save_folder, d, duration, urls, files, i, format_vid='any'):
    
    # save the video in the folder with id_duration
    file_name = save_folder + d + "_" + duration[i] + ".%(ext)s"
    
    # If file already exists, skip
    if d in files:
        print("File already exists: ",d)
        return

    # Download format options from the url from function: avoid MP4 format as it does not contain any metadata
    if format_vid == 'MP4':
        format = get_best_mp4_format(urls[i])
    else: 
        format = get_best_format(urls[i])

    command = [
        "yt-dlp",
        "-f",
        str(format),
        urls[i],
        "-o",
        file_name
    ]
    
    # Print the processed id 
    print("\nProcessing: ",d)
    # Try to download the video or raise error
    process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    #os.system("yt-dlp -f \"bv\"  \"" + urls[i] + "\" -o \"" + file_name + "\"")

    error_occurred = False 
    for output_line in process.stderr.splitlines():
        print(output_line)  # Print the output line to the console
        if "fragment not found" in output_line:
            print("Fragment not found, aborting download...")
            # Here, since the process has already completed, you can't "abort" it as it's already done.
            error_occured = True
            break

    if error_occurred:
        for filepath in glob(save_folder + d + "_" + duration[i] + "*.*"):
            try:
                os.remove(filepath)  
                print("Downloaded file removed.")
            except FileNotFoundError:
                print("No file found to remove.")

    if process.returncode == 0:
        print("Downloaded: ",d)
    else:
        print(f"Download failed: {process.returncode}")
        print("Error occured: ",urls[i])   

    return 


#--------------------------------------------------------------*****--------------------------------------------------------------#
""" 
    Main function to read the csv file and download the videos
"""
def main():
    parser = argparse.ArgumentParser(description='Download YouTube videos') 
    parser.add_argument('--csv_file', type=str, help='Path to the CSV file') # /home/ss223464/Desktop/LIVE/SantaFe/Data_Scrapping/searched_csv/CC_HDR_4K__10k_wordlist_10_20_mins_1200.csv
    parser.add_argument('--save_folder', type=str, default= "./Downloaded_videos/", help='Path to the folder to save the videos')
    parser.add_argument('--format', type=str, default= "any", help='Format of the video to download')
    parser.add_argument('--n_jobs', type=int, default= 10, help='Number of parallel jobs')
    args = parser.parse_args()

    # read the csv file
    file = args.csv_file
    df = pd.read_csv(file)

    # read ids and urls from the dataframe
    ids = df['id'].values
    urls = df['link'].values
    # extract duration from "duration" column
    duration = df['duration'].values
    # convert duration to total seconds
    # duration = [str(int(i.split(':')[0])*60 + int(i.split(':')[1])) for i in duration] 
    for i,j in enumerate(duration):
        try:  
            duration[i] = str(int(j.split(':')[0])*60 + int(j.split(':')[1]))
        except:
            print(i,j)
            duration[i] = 'None'

    # create the save folder if it does not exist
    if not os.path.exists(args.save_folder):
        os.mkdir(args.save_folder)
    
    # list of files in the save folder
    files = os.listdir(args.save_folder)
    # strip the duration from the file name
    files = [i.split('_')[0] for i in files]
    print("Total files already present: ", len(files))

    # download each video and save as id_shape_duration
    tasks = [(args.save_folder, d, duration, urls, files, i, args.format) for i, d in enumerate(ids)]
    Parallel(n_jobs=args.n_jobs)(delayed(download_video)(*t) for t in tqdm(tasks))

#--------------------------------------------------------------*****--------------------------------------------------------------#
if __name__ == '__main__':
    main()
