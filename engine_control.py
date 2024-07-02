# -*- coding:utf-8 -*-
#导入模块
from config import results
import sys, io
# sys.path.append('/home/pi/Desktop/ZL-PI/factory_code/')
sys.path.append('/home/pi/Desktop/sound/')
import ZL_SDK.ActionGroupControl as AGC
import ZL_SDK.Z_UartServer as myUart

# 设置默认编码为 utf-8
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
# sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')


#读取动作组文件。输入参数：动作组文件位置   
AGC.Group_read('/home/pi/Desktop/ZL-PI/factory_code/Jibot3_Group/jia_zi.ini')
myUart.setup_uart(115200)


def move(ops="$DGT:1-2,1!", n=1):
    '''调用SDK执行动作组'''

    n = 1  # 动作循环次数
    while 1:
        #判断动作组是否执行完成
        if AGC.group_ok:
            if n <= 0: break  # 应该放在parse前，否则可能第二次会执行两遍。
            AGC.groups_parse_cmd(ops)
            n -= 1
            print(f'n:{n}')
        ##循环发送动作组指令   
        AGC.loop_group()  # （每次应该只会执行一个动作）


def text_cmd_parse(cmd='松开'):
    d = {
        '松开': '$DGT:1-1,1!',
        '夹住': '$DGT:2-2,1!',
        '发起进攻': '$DGT:3-7,1!',
    }
    move(ops=d[cmd], n=1)


def app():
    '''test：在终端输入文本指令，控制动作'''
    while True:
        cmd = input('Please input the command by text: ')  # 中文显示异常
        if cmd == '#': break
        text_cmd_parse(cmd=cmd)


def engine_control(id: int=255, pwm: int=1500, time: int=1000):
    '''控制舵机'''
    cmd = f'#{id:03d}P{pwm:04d}T{time:04d}!'
    myUart.uart_send_str(cmd)
    return cmd


if __name__ == '__main__':
    text_cmd_parse()
    app()
