import os

label_num = {"보행자": 0, "SUV/승합차": 1, "세단": 2}

P_LBL_PATH = r"D:\car_human\Training\bounding_box\Gyeonggi\lbl"
A_LBL_PATH = r"C:\Users\1234\Desktop\Research\file_to_yolo\car_conv"

file_list = os.listdir(P_LBL_PATH)

MINIMUM_BOS_SIZE = 50 # number of pixel
pass_list = ["SUV/승합차", "세단"]

def conv_2_yolo(points, imgsz):

    center_x = (points[0][0] + points[1][0])/2
    center_y = (points[1][1] + points[2][1])/2

    abs_width = abs(points[0][0] - points[1][0])
    abs_hights = abs(points[1][1] - points[2][1])

    if abs_width * abs_hights < MINIMUM_BOS_SIZE:
        return

    x = round(center_x/imgsz[0], 6)
    y = round(center_y/imgsz[1], 6)

    w = round(abs_width/imgsz[0], 6)
    h = round(abs_hights/imgsz[1], 6)

    return x, y, w, h

max_ = len(file_list)

for n, name in enumerate(file_list):

    try:
        with open(fr"{P_LBL_PATH}\{name}", "r", encoding='UTF-8') as f:
            lines = f.readlines()

    except:
        with open(fr"{P_LBL_PATH}/{name}", "r", encoding='UTF-8') as f:
            lines = f.readlines()

    tmp_line = ""
    for num, i in enumerate(lines):
        tmp_line += i.strip("\n")
    try:
        json_raw = eval(tmp_line)
    except:
        continue
    json_info = json_raw["annotations"] # list per each object

    file_name = json_raw["filename"].split(".")[0]
    width = int(json_raw["camera"]["resolution_width"])
    height = int(json_raw["camera"]["resolution_height"])
    img_size = [width, height]
    try:
        with open(f"{A_LBL_PATH}\{file_name}.txt", "w") as f:
            for i in json_info:
                points = i["points"]
                x, y, w, h = conv_2_yolo(points, img_size)
                labels = i["label"]
                if labels == "보행자":
                    f.write(f"%d {x} {y} {w} {h}\n" % label_num[labels])
                    continue

                if label_num[i["attributes"][labels]] in pass_list:
                    f.write(f"%d {x} {y} {w} {h}\n" % label_num[i["attributes"][labels]])
                    continue
    except:
        try:
            with open(f"{A_LBL_PATH}/{file_name}.txt", "w") as f:
                for i in json_info:
                    points = i["points"]
                    x, y, w, h = conv_2_yolo(points, img_size)
                    if labels == "보행자":
                        f.write(f"%d {x} {y} {w} {h}\n" % label_num[labels])
                        continue

                    if label_num[i["attributes"][labels]] in pass_list:
                        f.write(f"%d {x} {y} {w} {h}\n" % label_num[i["attributes"][labels]])
                        continue

        except:
            continue

    print(f"{n+1}/{max_}")