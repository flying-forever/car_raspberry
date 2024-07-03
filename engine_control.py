# -*- coding:utf-8 -*-
#导入模块
from config import results
import sys, io, time
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
    '''控制舵机 (舵机模式)'''
    cmd = f'#{id:03d}P{pwm:04d}T{time:04d}!'
    myUart.uart_send_str(cmd)
    return cmd


# ---------------------------------------- 小车控制 ----------------------------------------


class Cmds:

    @staticmethod
    def wheel_mod_cmd(id: int=255, mod: int=1):
        '''左轮(id=3)：7前8后 | 右轮(id=2)：8前7后'''
        return f'#{id:03d}PMOD{mod}!'
    
    @staticmethod
    def wheel_move_cmd(id: int=255, pwm: int=1700, time: int=1):
        return f'#{id:03d}P{pwm:04d}T{time:04d}!'
    
class Car:
    '''pwm:转速, time:时间'''

    leftId = 3
    rightId = 2
    leftForwardMod = 7  # 左轮(id=3)：7前8后 | 右轮(id=2)：8前7后

    @staticmethod
    def mod_reverse(mod: int):
        return 8 if mod == 7 else 7

    @staticmethod
    def move(forward=True, left=True, pwm: int=1700, t: int=1):
        '''一个轮子的一次移动'''

        whell_id = Car.leftId if left else Car.rightId
        mod_id = Car.leftForwardMod 
        if not forward: 
            mod_id += 1
        if not left:
            mod_id = Car.mod_reverse(mod_id)

        cmd1 = Cmds.wheel_mod_cmd(id=whell_id, mod=mod_id)
        cmd2 = Cmds.wheel_move_cmd(id=whell_id, pwm=pwm, time=t)
        myUart.uart_send_str(cmd1)
        time.sleep(0.25)  # 否则可能不转
        myUart.uart_send_str(cmd2)
        return f'{cmd1} {cmd2}'

def app_car():
    '''test: 控制小车'''

    print('[example cmd]: left0 ')
    while True:
        cmd = input('Please input the command by text: ') 
        if cmd == '#': 
            break
        left = 'l' in cmd
        forward = '0' in cmd
        cmd = Car.move(left=left, forward=forward, pwm=1700, t=2)
        print('[run]', cmd)


if __name__ == '__main__':
    # text_cmd_parse()
    # app()

    app_car()
