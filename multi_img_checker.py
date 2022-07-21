from multiprocessing import Process
import os
import cv2

TARGET_IMGSIZE = (1920, 1080)
DIV_FACTOR = 5000

IMG_PATH = r"E:\0324_only_traffic\Val\img"

def img_remover(img_list):
    max_ = len(img_list)
    cnt = 1

    for i in img_list:
        print("%d/%d" % (cnt, max_))
        img = cv2.imread(fr"{IMG_PATH}\{i}")
        IMG_SIZE = img.shape
        if (IMG_SIZE[0] != TARGET_IMGSIZE[1]) or (IMG_SIZE[1] != TARGET_IMGSIZE[0]):
            os.remove(fr"{IMG_PATH}\{i}")
        cnt += 1

if __name__ == "__main__":

    img_list = os.listdir(IMG_PATH)
    num_of_process = int(len(img_list) / DIV_FACTOR) + 1
    for i in range(num_of_process):
        if i == num_of_process-1:
            inp_list = img_list[i*DIV_FACTOR:]
        else:
            inp_list = img_list[i*DIV_FACTOR:(i+1)*DIV_FACTOR]

        P = Process(target=img_remover, args=(inp_list, ))
        P.start()
