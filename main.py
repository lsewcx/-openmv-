from machine import Pin
import sensor, image, time
import pyb
from pyb import UART
import math

# 初始化摄像头
sensor.reset()
sensor.set_pixformat(sensor.RGB565)  # 设置图像色彩格式为RGB565格式
sensor.set_framesize(sensor.QQVGA)  # 设置图像大小为160*120
sensor.set_auto_whitebal(True)  # 设置自动白平衡
sensor.set_brightness(3000)  # 设置亮度为3000hjl;'k
sensor.skip_frames(time=20)  # 跳过帧

clock = time.clock()
num = 0
uart = UART(3, 115200)


def fill(string, width):  # 没到一定位数自动补零
    if len(string) == width:
        if string > str(sensor.width()):
            return str(sensor.width())
        else:
            return string
    else:
        padding = "0" * (width - len(string))
        return padding + string


while True:
    clock.tick()
    img = sensor.snapshot().lens_corr(1.8)

    # -----矩形框部分-----
    # 在图像中寻找矩形
    for r in img.find_rects(threshold=10000):
        # 判断矩形边长是否符合要求
        if 65 > r.w() > 20 and 65 > r.h() > 20:
            # 在屏幕上框出矩形
            img.draw_rectangle(r.rect(), color=(255, 0, 0), scale=4)
            # 获取矩形角点位置
            corner = r.corners()
            # 在屏幕上圈出矩形角点
            img.draw_circle(corner[0][0], corner[0][1], 5, color=(0, 0, 255), thickness=2, fill=False)
            img.draw_circle(corner[1][0], corner[1][1], 5, color=(0, 0, 255), thickness=2, fill=False)
            img.draw_circle(corner[2][0], corner[2][1], 5, color=(0, 0, 255), thickness=2, fill=False)
            img.draw_circle(corner[3][0], corner[3][1], 5, color=(0, 0, 255), thickness=2, fill=False)
            x_values = [corner[0][0], corner[1][0], corner[2][0], corner[3][0]]
            y_values = [corner[0][1], corner[1][1], corner[2][1], corner[3][1]]
            center_x = sum(x_values) / len(x_values)
            center_y = sum(y_values) / len(y_values)
            angles = []
            for x, y in zip(x_values, y_values):
                angle = math.atan2(y - center_y, x - center_x)  # 计算角度
                angles.append(angle)
            sorted_coordinates = [coord for _, coord in sorted(zip(angles, zip(x_values, y_values)))]  # 按照顺时针排序
            str_1 = fill(str(sorted_coordinates[0][0]), 3)
            str_2 = fill(str(sorted_coordinates[0][1]), 3)
            str_3 = fill(str(sorted_coordinates[1][0]), 3)
            str_4 = fill(str(sorted_coordinates[1][1]), 3)
            str_5 = fill(str(sorted_coordinates[2][0]), 3)
            str_6 = fill(str(sorted_coordinates[2][1]), 3)
            str_7 = fill(str(sorted_coordinates[3][0]), 3)
            str_8 = fill(str(sorted_coordinates[3][1]), 3)
            # 所有四个角点的x和y通信
            uart.write(str_1)
            uart.write(str_2)
            uart.write(str_3)
            uart.write(str_4)
            uart.write(str_5)
            uart.write(str_6)
            uart.write(str_7)
            uart.write(str_8)
