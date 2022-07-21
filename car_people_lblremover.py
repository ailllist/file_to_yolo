import os
import shutil

LBL_PATH = r"C:\Users\1234\Desktop\Research\file_to_yolo\car_conv"
A_LBL_PATH = r"D:\comp_anlysis_car_people\train\lalels"
A_IMG_PATH = r"C:\Users\1234\Desktop\Research\file_to_yolo\conv_img"
B_IMG_PATH = r"D:\car_human\Training\bounding_box\Gyeonggi\img"


lbl_file_list = os.listdir(LBL_PATH)
# lbl_file_list = [i.split(".")[0] for i in lbl_file_list]
img_file_list = os.listdir(A_IMG_PATH)
img_file_list = [i.split(".")[0] for i in img_file_list]

max_ = len(lbl_file_list)

for num, i in enumerate(lbl_file_list):
    # print(i.split(".")[0])
    # print(lbl_file_list)
    # print(fr"{B_IMG_PATH}\{i}")
    # breakpoint()
    if i.split(".")[0] in img_file_list:
        # print("gh")
        # print(fr"{B_IMG_PATH}\{i}")
        shutil.copy(fr"{LBL_PATH}\{i}", fr"{A_LBL_PATH}\{i}")

    print(f"{num}/{max_}")