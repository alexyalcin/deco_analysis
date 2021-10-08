import os
import cv2
import numpy as np
import take_screenshots

IN_PATH = "./screenshots"
OUT_PATH = "./sc_cropped"

SC = "./screenshots/9a04631c-e7a8-469c-b669-2c4ef2c18681/3wlj21KAF5ZHOdD50qAJLAupxMz1/9a04631c-e7a8-469c-b669-2c4ef2c18681.mp4_3wlj21KAF5ZHOdD50qAJLAupxMz1_4.png"

NEIGHBOR_OFFSETS = [[0,1], [0, -1], [1,0], [-1,0]]
def add_offsets(pixel, offsets):
    next_pixels = []
    for offset in offsets:
        next_pixels.append([pixel[0] + offset[0], pixel[1] + offset[1]])
    return next_pixels

def find_pixels(img):
    almost_black = []
    for y in range(img.shape[0]):
        for x in range(img.shape[1]):
            if sum(list(img[y, x])) <= 15:
                almost_black.append([y,x])
    print (len(almost_black))
    three_blue = []
    for pixel in almost_black:
        neighbors = add_offsets(pixel, NEIGHBOR_OFFSETS)
        bg_neighbors = 0
        for neighbor in neighbors:
            if list(img[neighbor[0], neighbor[1]]) == [220, 220, 220]:
                bg_neighbors+=1
        if bg_neighbors >1:
            three_blue.append(pixel)

    print (len(three_blue))
    print (three_blue)
    return three_blue

def get_crop_coordinates(corners):
    y = set([])
    x = set([])
    for vertex in corners:
        y.add(vertex[0])
        x.add(vertex[1])
    y = list(y)
    x = list(x)
    y.sort()
    x.sort()
    return y, x 

def find_red_cross(sc, cropy, cropx):
    x = cropx[0] #left pixel
    b, g, r = cv2.split(sc)
    for y in range(cropy[0], 0, -1):
        if r[y, x] == 255:
            cropy.insert(0, y)
            print('appended')
            return cropy, cropx
    return cropy, cropx


def crop_image(path, cropy = None, cropx = None):
    original_sc = cv2.imread(path)

    if cropy == None:
        corner_pixels = find_pixels(original_sc)
        cropy, cropx = get_crop_coordinates(corner_pixels)
    print (cropy, cropx)
    if len(cropy) == 1 and len(cropx) == 2:
        cropy, cropx = find_red_cross(original_sc, cropy, cropx)
    if len(cropy) < 2 or len(cropx) < 2:    
        print("FAILED TO CROP AUTOMATICALLY")
        cv2.imshow('Failed crop', original_sc)
        cv2.waitKey(1000)
        cv2.destroyAllWindows()
        return None, False, cropy, cropx
    cropped = original_sc[cropy[0]:cropy[1], cropx[0]:cropx[1]]
    return cropped, True, cropy, cropx

if __name__ == "__main__":
    for video in os.listdir(IN_PATH):
        next_video = False
        cropy = []
        cropx = []
        try:
            os.mkdir(f"{OUT_PATH}/{video}")
        except:
            pass
        if not os.path.isdir(f'{OUT_PATH}/{video}'):
            continue
        for rater in os.listdir(IN_PATH +'/' + video):
            if (next_video):
                break
            try:
                os.mkdir(f"{OUT_PATH}/{video}/{rater}")
            except:
                pass
            for screenshot in os.listdir(IN_PATH + '/' + video + '/' + rater):
                if (next_video):
                    break
                sc_path = f"{IN_PATH}/{video}/{rater}/{screenshot}"
                print (sc_path)
                if len(cropy) == 0 and len(cropx) == 0:
                    cropped, success, cropy, cropx = crop_image(sc_path)
                else:
                    cropped, success, cropy, cropx = crop_image(sc_path, cropy, cropx)
                if not success:
                    next_video = True
                else:
                    cropped_path = f"{OUT_PATH}/{video}/{rater}"
                    cv2.imwrite(os.path.join(cropped_path, f"{screenshot[0:-4]}_cropped.png"), cropped)
            
    #crop_image(SC)