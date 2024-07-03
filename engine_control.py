# -*- coding:utf-8 -*-
#导入模块
import sys, io, time
# sys.path.append('/home/pi/Desktop/ZL-PI/factory_code/')
sys.path.append('/home/pi/Desktop/sound/')
import ZL_SDK.ActionGroupControl as AGC
import ZL_SDK.Z_UartServer as myUart

# 设置默认编码为 utf-8
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
# sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')


#读取动作组文件。输入参数：动作组文件位置   
# AGC.Group_read('/home/pi/Desktop/ZL-PI/factory_code/Jibot3_Group/jia_zi.ini')
myUart.setup_uart(115200)


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
    
    @staticmethod
    def stop(id: int=255):
        return f'#{id:03d}PDST!'
    

class Car:
    '''提供小车基本动作的封装。'''

    leftId = 3
    rightId = 1
    leftForwardMod = 7  # 左轮(id=3)：7前8后 | 右轮(id=2)：8前7后

    @staticmethod
    def mod_reverse(mod: int):
        return 8 if mod == 7 else 7

    @staticmethod
    def move(forward=True, left=True, pwm: int=1700, t: int=1, excute=True):
        '''一个轮子的一次移动
        @excute: False则不执行，仅仅返回命令'''

        whell_id = Car.leftId if left else Car.rightId
        mod_id = Car.leftForwardMod 
        if not forward: 
            mod_id += 1
        if not left:
            mod_id = Car.mod_reverse(mod_id)

        cmd1 = Cmds.wheel_mod_cmd(id=whell_id, mod=mod_id)
        cmd2 = Cmds.wheel_move_cmd(id=whell_id, pwm=pwm, time=t)
        if excute:
            # 否则仅仅返回命令
            myUart.uart_send_str(cmd1)
            time.sleep(0.4)  # 否则可能不转
            myUart.uart_send_str(cmd2)
        return f'{cmd1} {cmd2}'
    
    @staticmethod
    def stop(id: int=255):
        cmd = Cmds.stop(id=id)
        myUart.uart_send_str(cmd)
        return cmd

    @staticmethod
    def move_double(forward=True, pwml: int=1700, pwmr: int=1700, t: int=1, turn_left: bool=None):
        '''两只轮子一起动，使用动作组。（可以差速转弯）'''
        
        # 单向运动 | 原地转圈
        if turn_left is None:
            fl = fr = forward
        elif turn_left:
            fl, fr = False, True
        else:
            fl, fr = True, False

        cmdl = Car.move(forward=fl, left=True, pwm=pwml, t=t, excute=False).split()
        cmdr = Car.move(forward=fr, left=False, pwm=pwmr, t=t,  excute=False).split()
        
        group_mod = '{' + cmdl[0] + cmdr[0] + '}'
        group_move = '{' + cmdl[1] + cmdr[1] + '}'

        myUart.uart_send_str(group_mod)
        time.sleep(0.4)
        myUart.uart_send_str(group_move)
        
        return f'{group_mod} {group_move}'



def app_car():
    '''test: 控制小车'''

    print('[example cmd]: left0 ')
    while True:
        cmd = input('Please input the command by text: ') 
        if cmd == '#': 
            break
        if 'g' in cmd:
            # 动作组
            forward = '1' not in cmd
            cmd = Car.move_double(forward=forward, pwml=1800, pwmr=1700, t=2)
            print('[run group]', cmd)
            continue
        left = 'l' in cmd
        forward = '0' in cmd
        cmd = Car.move(left=left, forward=forward, pwm=1800, t=2)
        print('[run]', cmd)


if __name__ == '__main__':
    # text_cmd_parse()
    # app()

    app_car()
