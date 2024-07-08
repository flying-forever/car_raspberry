# -*- coding: utf-8 -*-
import requests, timeit
from config import SPARKAI_URL, SPARKAI_APP_ID, SPARKAI_API_SECRET, SPARKAI_API_KEY, SPARKAI_DOMAIN


def zl_http(content='别站个歪的！', results=['向左转', '向右转', '立正'], model='general'):
    '''向spark模型发起文本转指令的请求'''
    
    prompt = f"\
        1. 你是一个自然语言转文本指令的助手，有如下文本指令：{results}。\
        2. 你的职责是根据用户说的话，从上述文本指令中选择和用户的话最相似的一个。\
        3. 你的输出应当仅仅是一个文本指令，不要说多余的话。\
        4. 输出必须是完全一致的文本指令，不能包含任何额外的解释或说明。\
        下面我说：{content}"
    
    url = SPARKAI_URL
    data = {
            "model": model, # 指定请求的模型
            "temperature": 0.01, # 生成的文本的随机程度
            "max_tokens": 10, # 生成的文本的最大长度
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }
    header = {
        "Authorization": f"Bearer {SPARKAI_API_KEY}:{SPARKAI_API_SECRET}" # 注意此处替换自己的key和secret
    }
    response = requests.post(url, headers=header, json=data)
    print(response.text)
    print('[zl_http]')
    r = response.json()['choices'][0]['message']['content']
    # print(r)
    return r


if __name__ == '__main__':
    t1 = timeit.timeit(lambda: zl_http(model='generalv3'), number=1)
    t2 = timeit.timeit(zl_http, number=1)
    # t1 = timeit.timeit(zl, number=1)
    print(f'[test]t1={t1}s, t2={t2}s')
