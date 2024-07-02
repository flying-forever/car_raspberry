# -*- coding: utf-8 -*-
from flask import Flask, render_template, jsonify, request
from spark import zl_http
from config import results, INPI
import sys, io
import re

if INPI:
    from text_control import text_cmd_parse


# 设置默认编码为 utf-8
# 备注：加上后，spark.py的输入在重载后才会一次性显示
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
# sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


def re(text: str, results: list):
    '''输入文本text，是否包含results中某条指令'''

    for result in results:
        if result in text:
            return result
    return None


def send_result(cmd):
    '''控制机械臂 | 向网页返回识别结果'''
    if INPI:
        text_cmd_parse(cmd=cmd)
    return jsonify(cmd)
    

@app.route('/text2cmd', methods=['POST'])
def text2cmd():
    
    data = request.json  ;print(data)
    text = data['content']

    # 1 机械文本匹配
    r = re(text=text, results=results)
    if r:
        return send_result(r)

    # 2 使用大模型语义比对
    r = zl_http(content=data['content'], model='generalv3', results=results)  ;print(r)
    return send_result(r)


app.run(debug=True, host="0.0.0.0", port=5000)
