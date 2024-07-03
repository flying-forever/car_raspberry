# -*- coding: utf-8 -*-

# 自定义的开机自启程序
from engine_control import Car
import time


if __name__ == '__main__':
    Car.stop()
    Car.move(forward=True, left=True, pwm=1700, t=2)
    Car.move(forward=True, right=True, pwm=1700, t=2)
    time.sleep(3)
    Car.stop()
    