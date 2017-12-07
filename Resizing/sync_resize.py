# coding=utf-8

"""
Labeling_Tool
Resize pic to defined size.

__author__ = 'JNingWei'
"""

import os
import cv2


def dst_check(dst):
    import shutil
    try:
        shutil.rmtree(dst)
    except OSError:
        pass
    os.makedirs(dst)

def resize_location(x, scale, min, max):
    # 类型检查
    x = int(x)
    # 尺寸缩放
    x = int(round(float(x) * scale))
    # 边界溢出检查
    x = min if x < min else x
    x = max if x > max else x
    return x


def get_path_lists(src):
    check_suffix = lambda x : True if os.path.splitext(x)[1] in [".jpg", ".JPG", ".png", ".PNG"] else False
    src_image_paths = [os.path.join(src, name) for name in os.listdir(src) if check_suffix(name)]
    assert len(src_image_paths)
    src_image_paths.sort()
    src_label_paths = [path.replace(os.path.splitext(path)[1], ".txt") for path in src_image_paths]
    dst_image_paths = [path.replace("Origin", "Resized").replace(os.path.splitext(path)[1], os.path.splitext(path)[1].lower()) for path in src_image_paths]
    dst_label_paths = [path.replace("Origin", "Resized").replace(os.path.splitext(path)[1], ".txt") for path in src_image_paths]
    return src_image_paths, src_label_paths, dst_image_paths, dst_label_paths


def get_src_label_size(image_path):
    image = cv2.imread(image_path)
    h, w = image.shape[:2]
    return h, w

def resize_image(src_image_path, dst_image_path, origin_size, new_size, idx):
    src_image = cv2.imread(src_image_path)
    dst_image = cv2.resize(src_image, new_size)
    cv2.imwrite(dst_image_path, dst_image)

def resize_label(src_label_path, dst_label_path, origin_size, new_size, idx):
    origin_h, origin_w = origin_size
    new_h, new_w = new_size
    scale_h, scale_w = new_h / origin_h, new_w / origin_w
    r_file = open(src_label_path, "r")
    w_file = open(dst_label_path, "w")
    lines = r_file.readlines()
    _, messages = lines[0], lines[1:]
    w_file.writelines(lines[0])
    for mess in messages:
        if mess.split():
            i, y1, x1, y2, x2 = mess.split()
            y1_new = resize_location(y1, scale_h, min=0, max=new_h-1)
            x1_new = resize_location(x1, scale_w, min=0, max=new_w-1)
            y2_new = resize_location(y2, scale_h, min=0, max=new_h-1)
            x2_new = resize_location(x2, scale_w, min=0, max=new_w-1)
            new_mess = "{0} {1} {2} {3} {4}\n".format(i, y1_new, x1_new, y2_new, x2_new)
            w_file.writelines(new_mess)
    r_file.close()
    w_file.close()


def main(src, dst, new_size):
    dst_check(dst)
    idx = 0
    src_image_paths, src_label_paths, dst_image_paths, dst_label_paths = get_path_lists(src)
    for (src_image_path, src_label_path, dst_image_path, dst_label_path) in zip(src_image_paths, src_label_paths, dst_image_paths, dst_label_paths):
        resize_image(src_image_path, dst_image_path, None, new_size, idx)
        resize_label(src_label_path, dst_label_path, get_src_label_size(src_image_path), new_size, idx)
        idx += 1


if __name__ == "__main__":
    SRC = './Origin'    # dir for origin pics
    DST = './Resized'    # dir for resized pics
    NEW_SIZE = (1024, 1024)   # new size
    main(SRC, DST, NEW_SIZE)
