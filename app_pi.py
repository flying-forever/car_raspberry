# -*- coding: utf-8 -*-
import os
import time
from flask import Flask, render_template, jsonify, request
from spark import zl_http
from stt import mp2text
from config import results, INPI, UPLOAD_FOLDER
import re


if INPI:
    from text_control import text_cmd_parse
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


app = Flask(__name__)



# ------------------------------------  工具函数  ------------------------------------


def test_time(func, func_name='func', *args, **kwargs):
    '''测试函数执行时间，返回原函数的返回值'''
    
    start = time.time()
    r = func(*args, **kwargs)
    end = time.time()
    print(f'[test_time] {func_name} cost {end-start} s')
    return r


def re(text: str, results: list):
    '''输入文本text，是否包含results中某条指令'''

    for result in results:
        if result in text:
            return result
    return None


def send_cmd(cmd):
    '''控制机械臂 | 向网页返回识别结果'''
    if INPI:
        text_cmd_parse(cmd=cmd)
    return jsonify(cmd)
    

# ------------------------------------  路由  ------------------------------------


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/text2cmd', methods=['POST'])
def text2cmd():
    
    data = request.json  ;print(data)
    text = data['content']

    # 1 机械文本匹配
    r = re(text=text, results=results)
    if r:
        return send_cmd(r)

    # 2 使用大模型语义比对
    r = zl_http(content=data['content'], model='generalv3', results=results)  ;print(r)
    return send_cmd(r)


@app.route('/sttapi', methods=['POST'])
def sttAPI():
    '''mp3语音文件 -> 文本转指令'''

    # 1 保存文件
    if 'audio' not in request.files:
        print('[save_audio] No audio file in request')    
    file = request.files['audio']  # ‘audio’表单字段名在前端指定
    if file.filename == '':
        print('[save_audio] No selected file')    
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    # 2 识别
    text = mp2text(filename=file.filename, dir=UPLOAD_FOLDER)
    return jsonify(text)
    

app.run(debug=True, host="0.0.0.0", port=5000)
