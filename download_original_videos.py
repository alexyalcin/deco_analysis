from http_request import * 
import requests
import os

OUT_PATH = "./original_videos"

def download_mp4(video, url, path):
    response = requests.get(url)
    f = open(path + "/" + video + ".mp4", 'wb')
    for chunk in response.iter_content(chunk_size=255): 
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)

if __name__ == "__main__":
    if not os.path.isdir(OUT_PATH):
        os.mkdir(OUT_PATH)
    video_urls = get_video_urls()
    for video in video_urls.keys():
        url = video_urls[video]
        download_mp4(video, url, OUT_PATH)