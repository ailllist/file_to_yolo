import os

EXTEND_FACTOR = 1.1

class FormatError(Exception):

    def __str__(self):
        print("Another Format detected")


def conv_2_yolo(att, imgsz):
    center_x = (att[0] + att[2])/2
    center_y = (att[1] + att[3])/2

    abs_width = abs(att[0] - att[2])
    abs_height = abs(att[1] - att[3])

    x = round(center_x/imgsz[0], 6)
    y = round(center_y/imgsz[1], 6)

    width = round(abs_width/imgsz[0] * EXTEND_FACTOR, 6)
    height = round(abs_height/imgsz[1] * EXTEND_FACTOR, 6)

    return x, y, width, height

def status_analysisor(TL_status):

    add_number = 99

    if len(TL_status) == 1:
        if "red" in TL_status:
            add_number = 0
        elif"yellow" in TL_status:
            add_number = 1
        elif "green" in TL_status:
            add_number = 4

    elif len(TL_status) == 2:
        if "left_arrow" in TL_status:
            if "red" in TL_status:
                add_number = 2
            elif "green" in TL_status:
                add_number = 3

    return add_number

# file_list = os.listdir(r"D:\file_to_yolo\convert")
file_list = os.listdir(r"E:\0315_new_data\Training\lbl")


cnt = 1
max_ = len(file_list)


for name in file_list:

    print("%d/%d (converter)" % (cnt, max_))
    cnt += 1

    with open(r"E:\0315_new_data\Training\lbl\%s" % name, "r") as f:
        lines = f.readlines()
        if len(lines) != 1:
            continue

    main_line = lines[0]
    att_dict = eval(main_line)

    imgsz = att_dict["image"]["imsize"]
    att_list = att_dict["annotation"]

    TL_list = []
    stop_iter = False
    for i in att_list: # type, light_count, box, attribute, direction, class
        if i["class"] == "traffic_light":
            key_list = list(i.keys())
            if "type" in key_list and "direction" in key_list:
                if i["type"] == "car" and i["direction"] == "horizontal":
                    pos = i["box"]
                    try:
                        light_count = int(i["light_count"])
                    except:
                        break
                    x, y, width, height = conv_2_yolo(pos, imgsz)
                    att_type = i["attribute"][0]
                    TL_status = []
                    for j in list(att_type.keys()):
                        if att_type[j] == "on":
                            TL_status.append(j)

                    add_num = status_analysisor(TL_status)
                    if add_num == 99:
                        break
                    mul_num = light_count
                    class_num = 5 * (light_count-1) + add_num
                    save_str = f"{class_num} {x} {y} {width} {height}"
                    TL_list.append(save_str)

            else: # 망할 제작자들
                if "light_count" in key_list:
                    light_count = int(i["light_count"])
                    if light_count >= 3:
                        x, y, width, height = conv_2_yolo(pos, imgsz)
                        att_type = i["attribute"][0]
                        TL_status = []
                        for j in list(att_type.keys()):
                            if att_type[j] == "on":
                                TL_status.append(j)

                        add_num = status_analysisor(TL_status)
                        if add_num == 99:
                            break
                        mul_num = light_count
                        class_num = 5 * (light_count - 1) + add_num
                        save_str = f"{class_num} {x} {y} {width} {height}"
                        TL_list.append(save_str)
                else: # 않이;; traffic_light지만 위치 정보 빼고 아무런 정보를 얻을 수 없을 때
                    stop_iter = True
                    continue
    if stop_iter:
        continue

    if len(TL_list) == 0:
        continue

    p_target_name = att_dict["image"]["filename"].split(".")[0]
    target_name = "%s.txt" % p_target_name

    with open(r"E:\0315_new_data\Training\res\%s" % target_name, "w") as p:
        for j in TL_list:
            p.write("%s\n" % j)

p_max = max_

print("end")


img_list = os.listdir(r"E:\0315_new_data\Training\img")
lbl_list = [i.split(".")[0] for i in os.listdir(r"E:\0315_new_data\Training\res")]

max_ = len(img_list)
cnt = 1

for i in img_list:
    f_name = i.split(".")[0]
    if f_name not in lbl_list:
        os.remove(r"E:\0315_new_data\Training\img\%s" % i)
    print("%d/%d (remover)" % (cnt, max_))
    cnt += 1

img_list = os.listdir(r"E:\0315_new_data\Training\img")
print(f"finished before : {max_} after : {len(img_list)}")
print(f"total finished before : {p_max} after : {len(img_list)}")