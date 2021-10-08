import requests
import json

ALL_VIDEO_INFO = None

def get_all_video_info():
    ##################get password from file##################
    passfile = open("login_info.txt", "r")
    login_info_lines = passfile.read().split('\n')
    USERNAME = login_info_lines[0]
    PASSWORD = login_info_lines[1]

    ##################login, get token##################

    login_url = "https://us-central1-bubblelocatorapi.cloudfunctions.net/api/login"
    payload = json.dumps({
    "email": USERNAME,
    "password": PASSWORD
    })
    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", login_url, headers=headers, data=payload)
    token = response.json()['token']

    all_videos_url = "https://us-central1-bubblelocatorapi.cloudfunctions.net/api/get-all-completed-videos"

    payload={}
    headers = {
    'token': token
    }

    all_video_info = requests.request("GET", all_videos_url, headers=headers, data=payload)
    return all_video_info.json()

def get_video_urls():
    global ALL_VIDEO_INFO
    if ALL_VIDEO_INFO == None:
        ALL_VIDEO_INFO = get_all_video_info()
    
    video_urls = {}
    for video in ALL_VIDEO_INFO:
        video_urls[video['title'][:-4]] = video['url']
    return video_urls
    
if __name__ == "__main__":
    urls = get_video_urls()
    print (urls)