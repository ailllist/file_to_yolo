import random
import shutil
import os

IMG_PATH = r"/home/autonav-linux/Documents/0718_deliv/images"
LBL_PATH = r"/home/autonav-linux/Documents/0718_deliv/labels"
val_TARGET_IMG = r"/home/autonav-linux/Documents/n_0718/val/images"
val_TARGET_LBL = r"/home/autonav-linux/Documents/n_0718/val/labels"
train_TARGET_IMG = r"/home/autonav-linux/Documents/n_0718/train/images"
train_TARGET_LBL = r"/home/autonav-linux/Documents/n_0718/train/labels"

VAL_ratio = 20  # %

lbl_list = os.listdir(LBL_PATH)
img_list = os.listdir(IMG_PATH)
name_list = [i.split(".")[0] for i in img_list]
# shutil.copy("./test1/test1.txt", "./test3.txt")
for num, i in enumerate(name_list):

    if random.randint(1, 100) <= VAL_ratio:  # VAL_ratio 보다 작은 수를 뽑은 경우
        shutil.copy(fr"{IMG_PATH}/{i}.jpg", fr"{val_TARGET_IMG}/{i}.jpg")
        shutil.copy(fr"{LBL_PATH}/{i}.txt", fr"{val_TARGET_LBL}/{i}.txt")

    else:
        shutil.copy(fr"{IMG_PATH}/{i}.jpg", fr"{train_TARGET_IMG}/{i}.jpg")
        shutil.copy(fr"{LBL_PATH}/{i}.txt", fr"{train_TARGET_LBL}/{i}.txt")

    print(f"{num}/{len(name_list)}")