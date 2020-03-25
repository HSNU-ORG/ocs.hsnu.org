import sys
import json
import base64
from urllib.request import urlopen
from urllib.request import Request
from urllib.error import URLError
from urllib.parse import urlencode
from urllib.parse import quote_plus
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

API_KEY = 'qPO9LT4d030sY00t6KL8Gsqx'

SECRET_KEY = 'nf8Z3vuN2KFIVzgvAa3odLVZcK0dklQy'


OCR_URL = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic"


"""  TOKEN start """
TOKEN_URL = 'https://aip.baidubce.com/oauth/2.0/token'


"""
    获取token
"""
def fetch_token():
    params = {'grant_type': 'client_credentials',
              'client_id': API_KEY,
              'client_secret': SECRET_KEY}
    post_data = urlencode(params)
    post_data = post_data.encode('utf-8')
    req = Request(TOKEN_URL, post_data)
    try:
        f = urlopen(req, timeout=5)
        result_str = f.read()
    except URLError as err:
        print(err)
    result_str = result_str.decode()
    result = json.loads(result_str)

    if ('access_token' in result.keys() and 'scope' in result.keys()):
        if not 'brain_all_scope' in result['scope'].split(' '):
            print ('please ensure has check the  ability')
            exit()
        return result['access_token']
    else:
        print ('please overwrite the correct API_KEY and SECRET_KEY')
        exit()

"""
    读取文件
"""
def read_file(image_path):
    f = None
    try:
        f = open(image_path, 'rb')
        return f.read()
    except:
        print('read image file fail')
        return None
    finally:
        if f:
            f.close()


"""
    调用远程服务
"""
def _request(url, data):
    req = Request(url, data.encode('utf-8'))
    has_error = False
    try:
        f = urlopen(req)
        result_str = f.read().decode()
        return result_str
    except  URLError as err:
        print(err)

if __name__ == '__main__':

    token = fetch_token()

    image_url = OCR_URL + "?access_token=" + token

    text = ""

    result = _request(image_url, urlencode({'image': img}))

    result_json = json.loads(result)
    for words_result in result_json["words_result"]:
        text = text + words_result["words"]
    print(text)