import cv2
import os

TARGET_IMGSIZE = (1920, 1080)

img_list = os.listdir(r"D:\file_to_yolo\imgs")
max_ = len(img_list)
cnt = 1

for i in img_list:
    print("%d/%d" % (cnt, max_))
    img = cv2.imread(fr"D:\file_to_yolo\imgs\{i}")
    IMG_SIZE = img.shape
    if (IMG_SIZE[0] != TARGET_IMGSIZE[1]) or (IMG_SIZE[1] != TARGET_IMGSIZE[0]):
        os.remove(fr"D:\file_to_yolo\imgs\{i}")
    cnt += 1