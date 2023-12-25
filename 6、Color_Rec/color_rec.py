import cv2
import os
import numpy as np
from collections import Counter

table = {
    'black': {'hmin': 0, 'hmax': 180, 'smin': 0, 'smax': 255, 'vmin': 0, 'vmax': 80},
    'gray': {'hmin': 0, 'hmax': 180, 'smin': 0, 'smax': 255, 'vmin': 200, 'vmax': 220},
    'white': {'hmin': 0, 'hmax': 180, 'smin': 0, 'smax': 30, 'vmin': 221, 'vmax': 255},
    'pink': {'hmin': 0, 'hmax': 10, 'smin': 43, 'smax': 255, 'vmin': 46, 'vmax': 255},
    'dark red': {'hmin': 156, 'hmax': 180, 'smin': 43, 'smax': 255, 'vmin': 46, 'vmax': 255},
    'orange': {'hmin': 11, 'hmax': 12, 'smin': 43, 'smax': 255, 'vmin': 46, 'vmax': 255},
    'brown': {'hmin': 10, 'hmax': 13, 'smin': 43, 'smax': 255, 'vmin': 46, 'vmax': 255},
    'gold': {'hmin': 15, 'hmax': 22, 'smin': 43, 'smax': 255, 'vmin': 46, 'vmax': 255},
    'yellow': {'hmin': 26, 'hmax': 34, 'smin': 43, 'smax': 255, 'vmin': 46, 'vmax': 255},
    'green': {'hmin': 35, 'hmax': 77, 'smin': 43, 'smax': 255, 'vmin': 46, 'vmax': 255},
    'cyan': {'hmin': 78, 'hmax': 99, 'smin': 43, 'smax': 255, 'vmin': 46, 'vmax': 255},
    'sky blue': {'hmin': 100, 'hmax': 110, 'smin': 43, 'smax': 255, 'vmin': 46, 'vmax': 255},
    'blue': {'hmin': 111, 'hmax': 124, 'smin': 43, 'smax': 255, 'vmin': 46, 'vmax': 255},
    'purple': {'hmin': 125, 'hmax': 155, 'smin': 43, 'smax': 255, 'vmin': 46, 'vmax': 255}
}

def find_most_common_colors(img_path, table,save_path, downsample_rate=4):
    # 创建保存图片的目录（如果它不存在）
    file_name = os.path.basename(img_path)
    # 读取图片
    img = cv2.imread(img_path)

    # 将图片从BGR格式转换为HSV格式
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # 获取图片的高度和宽度
    height, width = hsv_img.shape[:2]
    # 创建一个空的numpy数组，用于存储每个像素的颜色
    color_img = np.empty((height, width), dtype=object)

    # 使用向量化操作替换双重for循环
    for color, values in table.items():
        mask = cv2.inRange(hsv_img, (values['hmin'], values['smin'], values['vmin']), (values['hmax'], values['smax'], values['vmax']))
        # 排除特定的HSV值
        mask &= np.all(hsv_img != [0, 0, 255], axis=-1)
        color_img[mask > 0] = color

    # 下采样
    color_img = color_img[::downsample_rate, ::downsample_rate]

    # 将color_img转换为一维数组
    color_array = color_img.flatten()
    # 过滤掉None值
    color_array = color_array[color_array != None]
    # 使用Counter统计每种颜色的出现次数
    counter = Counter(color_array)
    #转化为百分比
    total = sum(counter.values())

    percentage_table = {}
    color = ""
    for key, value in counter.items():
        percentage = (value / total) * 100
        if percentage > 18:
            percentage_table[key] = round(percentage, 2)
    # 按照百分比大小对键进行排序
    sorted_table = sorted(percentage_table.items(), key=lambda x: x[1], reverse=True)
    for i, key in enumerate(sorted_table):
        if i >= 3:
            break
        color = color + key[0]+" "

        # 在图片上添加文字
    cv2.putText(img, color, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
    file_path = os.path.join(save_path, file_name)
    # 保存修改后的图片
    cv2.imwrite(file_path, img)
    return color

def process_images_in_folder(folder_path,table, save_path):

    os.makedirs(save_path, exist_ok=True)
    # 获取文件夹中的所有文件
    files = os.listdir(folder_path)
    # 过滤出.jpg文件
    img_files = [f for f in files if f.endswith('.jpg')]

    # 对每一张图片进行处理
    for img_file in img_files:
        img_path = os.path.join(folder_path, img_file)
        most_common_colors = find_most_common_colors(img_path=img_path, table=table, save_path=save_path)
        print(f'图片{img_file}鞋子的颜色是：{most_common_colors}')

if __name__ == '__main__':
    folder_path ="./detc_images"
    save_path = "./output"
    process_images_in_folder(folder_path=folder_path, table=table, save_path=save_path)
