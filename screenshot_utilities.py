import os
import json

path = './screenshots/screenshot_data.json'
data = {}

def set_path(p):
    global path
    path = p

def init_file(p = path):
    global data
    set_path(p)
    try:
        with open(path) as json_file:
            data = json.load(json_file)
    except:
        data['count'] = 0
        data['ss'] = {}
    with open(path, 'w') as data_file:
        json.dump(data, data_file)
        
def add_screenshot(video, rater, frame = 0):
    global data
    data['count'] += 1
    ss_data = data['ss']
    ss_data['ss'+ str(data['count'])] = {
        'video': video,
        'rater': rater,
        'frame': frame
    }
    return 'ss' + str(data['count'])

def count():
    global data
    if data == {}:
        with open(path) as json_file:
            data = json.load(json_file)
            return data['count']

def save_data():
    global data
    with open(path, 'w') as data_file:
        json.dump(data, data_file)

def get_attr(ss_name, attr):
    global data
    if len(ss_name.split("_")) == 2:
        ss_name = ss_name.split("_")[0]
    with open(path) as json_file:
        if data == {}:
            data = json.load(json_file)
        return data['ss'][ss_name][attr]

def get_video_name(ss_name):
    return get_attr(ss_name, "video")

def get_rater_id(ss_name):
    return get_attr(ss_name, "rater")

def get_frame(ss_name):
    return get_attr(ss_name, "frame")

if __name__ == "__main__":
    set_path('screenshots/screenshot_data.json')
    print(get_frame("ss1_cropped"))