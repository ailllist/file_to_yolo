import os

IMG_PATH = r"E:\val\img"
BEFORE_LBL_PATH = r"E:\val\lbl"
AFTER_LBL_PATH = r"E:\val\res"
LBL_PATH = r"E:\0315_new_data\Training\train\labels"

file_list = os.listdir(LBL_PATH)

max = 0
cnt = 1
total = len(file_list)
error_list = []

for i in file_list:
    try:
        with open(rf"{LBL_PATH}\%s" % i) as f:
            lines = [j.strip("\n") for j in f.readlines()]
            for j in lines:
                if int(j.split(" ")[0]) > max:
                    max = int(j.split(" ")[0])
                if int(j.split(" ")[0]) > 29:
                    error_list.append(i)
        print("%d/%d" % (cnt, total))
    except:
        pass
    cnt += 1

print("max classes : ", max)
print(error_list)