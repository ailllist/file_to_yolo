import os

IMG_PATH = r"/media/autonav/새 볼륨/0718_deliv/images"
LBL_PATH = r"/media/autonav/새 볼륨/0718_deliv/labels"

lbl_list = os.listdir(LBL_PATH)
img_list = [i.split(".")[0] for i in os.listdir(IMG_PATH)]


max_ = len(lbl_list)
cnt = 1
for i in lbl_list:
    f_name = i.split(".")[0]
    if f_name not in img_list:
        os.remove(fr"{LBL_PATH}/%s" % i)

    print("%d/%d" % (cnt, max_))
    cnt += 1

lbl_list = os.listdir(LBL_PATH)
print(f"finished before : {max_} after : {len(lbl_list)}")