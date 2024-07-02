import requests
# URL = 'http://127.0.0.1:9977/api'
URL = 'http://192.168.43.166:9977/api'


# ------------------------------------  stt语音识别  ------------------------------------


def mp2text(model_name='base', dir='C:\\Users\\ThinkPad\\Desktop', filename='向左转.mp3',) -> str:
    '''mp3语音文件 -> stt语音识别'''
    print('[mp2text]...')

    fpath = f"{dir}/{filename}"
    with open(fpath, "rb") as fp:
        files = {"file": fp}
        data={"language":"zh","model":model_name,"response_format":"text"}  # response_format:text|json|srt
        response = requests.request("POST", URL, timeout=600, data=data, files=files)
    json = response.json()
    print(f'[mp2text]: {json}')
    return json['data']

