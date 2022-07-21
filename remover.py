import os

IMG_PATH = r"/media/autonav/새 볼륨/0718_deliv/images"
LBL_PATH = r"/media/autonav/새 볼륨/0718_deliv/labels"

img_list = os.listdir(IMG_PATH)
lbl_list = [i.split(".")[0] for i in os.listdir(LBL_PATH)]

max_ = len(img_list)
cnt = 1

for i in img_list:
    f_name = i.split(".")[0]
    if f_name not in lbl_list:
        os.remove(fr"{IMG_PATH}/%s" % i)
    print("%d/%d" % (cnt, max_))
    cnt += 1

img_list = os.listdir(IMG_PATH)
print(f"finished before : {max_} after : {len(img_list)}")