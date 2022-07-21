from multiprocessing import Process, Value
import os
import cv2

# -------------------------------image_checker parameter-------------------------------
TARGET_IMGSIZE = (1920, 1080)
DIV_FACTOR = 4900
# -------------------------------image_checker parameter-------------------------------
# -------------------------------lbl_matcher parameter-------------------------------
pass
# -------------------------------lbl_matcher parameter-------------------------------
# -------------------------------converter parameter-------------------------------
EXTEND_FACTOR = 1.1
# -------------------------------converter parameter-------------------------------
# -------------------------------remover parameter-------------------------------

# -------------------------------remover parameter-------------------------------

IMG_PATH = r"E:\val\img"
BEFORE_LBL_PATH = r"E:\val\lbl"
AFTER_LBL_PATH = r"E:\val\res"

if os.path.isdir(IMG_PATH) and os.path.isdir(BEFORE_LBL_PATH) and os.path.isdir(AFTER_LBL_PATH):
    print("Y")
else:
    exit()

class FormatError(Exception):

    def __str__(self):
        print("Another Format detected")

def img_remover(img_list, f_cnt):

    max_ = len(img_list)
    cnt = 1

    for i in img_list:
        print("%d/%d (img_checker) 1/4" % (cnt, max_))
        img = cv2.imread(fr"{IMG_PATH}\{i}")
        IMG_SIZE = img.shape
        if (IMG_SIZE[0] != TARGET_IMGSIZE[1]) or (IMG_SIZE[1] != TARGET_IMGSIZE[0]):
            os.remove(fr"{IMG_PATH}\{i}")
        cnt += 1
    f_cnt.value += 1
    return

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

def lbl_matcher():

    img_list = [i.split(".")[0] for i in os.listdir(IMG_PATH)]
    lbl_list = os.listdir(BEFORE_LBL_PATH)

    max_ = len(lbl_list)
    cnt = 1
    for i in lbl_list:
        f_name = i.split(".")[0]
        if f_name not in img_list:
            os.remove(fr"{BEFORE_LBL_PATH}\%s" % i)
        print("%d/%d (lbl_matcher) 2/4" % (cnt, max_))
        cnt += 1

    lbl_list = os.listdir(BEFORE_LBL_PATH)
    print(f"finished before : {max_} after : {len(lbl_list)}")

def converter():
    file_list = os.listdir(BEFORE_LBL_PATH)

    cnt = 1
    max_ = len(file_list)

    for name in file_list:

        print("%d/%d (converter) 3/4" % (cnt, max_))
        cnt += 1

        with open(fr"{BEFORE_LBL_PATH}\%s" % name, "r") as f:
            lines = f.readlines()
            if len(lines) != 1:
                continue

        main_line = lines[0]
        att_dict = eval(main_line)

        imgsz = att_dict["image"]["imsize"]
        att_list = att_dict["annotation"]

        TL_list = []
        for i in att_list:  # type, light_count, box, attribute, direction, class
            if i["class"] == "traffic_light":
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
                    class_num = 5 * (light_count - 1) + add_num
                    save_str = f"{class_num} {x} {y} {width} {height}"
                    TL_list.append(save_str)

        if len(TL_list) == 0:
            continue

        p_target_name = att_dict["image"]["filename"].split(".")[0]
        target_name = "%s.txt" % p_target_name

        with open(fr"{AFTER_LBL_PATH}\%s" % target_name, "w") as p:
            for j in TL_list:
                p.write("%s\n" % j)

    print("end")

def n_converter():

    file_list = os.listdir(BEFORE_LBL_PATH)

    cnt = 1
    max_ = len(file_list)

    for name in file_list:

        print("%d/%d (converter)" % (cnt, max_))
        cnt += 1

        with open(fr"{BEFORE_LBL_PATH}\%s" % name, "r") as f:
            lines = f.readlines()
            if len(lines) != 1:
                continue

        main_line = lines[0]
        att_dict = eval(main_line)

        imgsz = att_dict["image"]["imsize"]
        att_list = att_dict["annotation"]

        TL_list = []
        stop_iter = False
        for i in att_list:  # type, light_count, box, attribute, direction, class
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
                        class_num = 5 * (light_count - 1) + add_num
                        save_str = f"{class_num} {x} {y} {width} {height}"
                        TL_list.append(save_str)

                else:  # 망할 제작자들
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
                            class_num = 5 * (light_count - 1) + add_num
                            save_str = f"{class_num} {x} {y} {width} {height}"
                            TL_list.append(save_str)
                    else:  # 않이;; traffic_light지만 위치 정보 빼고 아무런 정보를 얻을 수 없을 때
                        stop_iter = True
                        continue
        if stop_iter:
            continue

        if len(TL_list) == 0:
            continue

        p_target_name = att_dict["image"]["filename"].split(".")[0]
        target_name = "%s.txt" % p_target_name

        with open(fr"{AFTER_LBL_PATH}\%s" % target_name, "w") as p:
            for j in TL_list:
                p.write("%s\n" % j)

    print("end")

def remover():
    img_list = os.listdir(IMG_PATH)
    lbl_list = [i.split(".")[0] for i in os.listdir(AFTER_LBL_PATH)]

    max_ = len(img_list)
    cnt = 1

    for i in img_list:
        f_name = i.split(".")[0]
        if f_name not in lbl_list:
            os.remove(fr"{IMG_PATH}\%s" % i)
        print("%d/%d (remover) 4/4" % (cnt, max_))
        cnt += 1

    img_list = os.listdir(IMG_PATH)
    print(f"finished before : {max_} after : {len(img_list)}")

if __name__ == "__main__":

    f_cnt = Value("i", 0)
    img_list = os.listdir(IMG_PATH)
    num_of_process = int(len(img_list) / DIV_FACTOR) + 1
    for i in range(num_of_process):
        if i == num_of_process-1:
            inp_list = img_list[i*DIV_FACTOR:]
        else:
            inp_list = img_list[i*DIV_FACTOR:(i+1)*DIV_FACTOR]

        P = Process(target=img_remover, args=(inp_list, f_cnt))
        P.start()

    while f_cnt.value < num_of_process:
        pass

    lbl_matcher()
    n_converter()
    remover()