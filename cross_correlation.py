import cv2
import os
import numpy as np
import screenshot_utilities as ssutil
from crop_images import OUT_PATH

VIDEO_PATH = "./original_videos"

def get_frame(name, n):
    cap = cv2.VideoCapture(VIDEO_PATH + '/' + name + '.mp4')
    frame_num = 1
    while (cap.isOpened()):
        ret, frame = cap.read()
        if not ret:
            break
        if frame_num == n:
            cap.release()
            return frame
        frame_num += 1
    cap.release()
    return frame_num

video1 = '201503142019170006Card-30fps'

def get_frames_near(name, n, near = 2):
    frames = {}
    for x in range(n - near, n + near + 1):
        f = get_frame(name, x)
        frames[x] = f
    return frames

def read_screenshot(video, rater, name): 
    path = OUT_PATH + "/" + video + "/" + rater + '/' + name + "_cropped.png"
    ss =  cv2.imread(path)
    return ss
    
def cross_correlate(ss_name):
    video_name = ssutil.get_video_name(ss_name)[:-4]
    rater_name = ssutil.get_rater_id(ss_name)
    frame_num = int(ssutil.get_frame(ss_name))
    
    frame_ss = read_screenshot(video_name, rater_name, ss_name)
    frame_ss.astype(np.float32) 
    dims = (frame_ss.shape[1], frame_ss.shape[0])

    frames_original = get_frames_near(video_name, frame_num)
    
    max_coeff = 0
    max_frame = -1
    for original_frame_num in frames_original.keys():
        frame_original = frames_original[original_frame_num]
        frame_original.astype(np.float32)
        frame_original = cv2.resize(frame_original, dims)

        method = cv2.TM_CCOEFF_NORMED
        result = cv2.matchTemplate(frame_ss, frame_original, method)

        idx = (np.unravel_index(result.argmax(), result.shape))
        corr_coeff = result[idx[0], idx[1]]

        if corr_coeff > max_coeff:
            max_coeff = corr_coeff
            max_frame = original_frame_num
        print (result[idx[0], idx[1]])

    #show match
    cv2.imshow("Frame " + str(max_frame), frames_original[max_frame])
    cv2.imshow("Screenshot", frame_ss)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    print ("**************************************")
    return max_frame, frames_original[max_frame]

        
def find_original_frames(start, end):
    frame_original_nums = {}
    for num in range(start, end + 1):
        name = "ss" + str(num)
        frame_num, frame = cross_correlate(name)
        frame_original_nums[name] = (frame_num, frame)
    return frame_original_nums

def find_and_save_original_frames():
    total_num = ssutil.count()
    frame_original_nums = find_original_frames(1, total_num)
    print (frame_original_nums["ss1300"])


if __name__ == "__main__":
    find_and_save_original_frames()


# frames = get_frames_near(video1, 142)
# for f in frames.keys():
#     cv2.imshow("Frame " + str(f), frames[f])
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()


#cv2.imwrite(path , cropped)
# def show_frames(name, start, end):
#     for x in range(start, end + 1):
#         f = get_frame(name, x)
#         cv2.imshow("Frame " + str(x), f)
#         cv2.waitKey(0)
#         cv2.destroyAllWindows()
