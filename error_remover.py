import os

IMG_PATH = r"/media/autonav/새 볼륨/0718_deliv/images"
LBL_PATH = r"/media/autonav/새 볼륨/0718_deliv/labels"

file_list = os.listdir(LBL_PATH)

MAX_CLASS_NUM = 14
max = 0
cnt = 1
total = len(file_list)
error_list = []

for i in file_list:
    try:
        with open(rf"{LBL_PATH}/%s" % i) as f:
            lines = [j.strip("\n") for j in f.readlines()]
            for j in lines:
                if int(j.split(" ")[0]) > max:
                    max = int(j.split(" ")[0])
                if int(j.split(" ")[0]) > MAX_CLASS_NUM:
                    error_list.append(i)
        print("%d/%d" % (cnt, total))
    except:
        pass
    cnt += 1

for i in error_list:
    name = i.split(".")[0]
    try:
        os.remove(rf"{IMG_PATH}/%s.jpg" % name)
    except:
        print("no Img file", name)

    try:
        os.remove(rf"{LBL_PATH}/%s.txt" % name)
    except:
        print("no lbl file", name)

print("max classes : ", max)
print(error_list)