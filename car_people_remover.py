import os
import shutil

LBL_PATH = r"C:\Users\1234\Desktop\Research\file_to_yolo\car_conv"
A_IMG_PATH = r"C:\Users\1234\Desktop\Research\file_to_yolo\conv_img"
B_IMG_PATH = r"D:\car_human\Training\bounding_box\Gyeonggi\img"


lbl_file_list = os.listdir(LBL_PATH)
lbl_file_list = [i.split(".")[0] for i in lbl_file_list]
img_file_list = os.listdir(B_IMG_PATH)

max_ = len(img_file_list)

for num, i in enumerate(img_file_list):
    # print(i.split(".")[0])
    # print(lbl_file_list)
    print(fr"{B_IMG_PATH}\{i}")
    # breakpoint()
    if i.split(".")[0] in lbl_file_list:
        # print("gh")
        # print(fr"{B_IMG_PATH}\{i}")
        shutil.copy(fr"{B_IMG_PATH}\{i}", fr"{A_IMG_PATH}\{i}")

    print(f"{num}/{max_}")