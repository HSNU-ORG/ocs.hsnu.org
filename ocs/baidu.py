import json
import os
from urllib.request import urlopen, Request
from urllib.error import URLError
from urllib.parse import urlencode, quote_plus
from dotenv import load_dotenv

load_dotenv()

# account info
API_KEY = os.getenv("API_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")
OCR_URL = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic?access_token="
TOKEN_URL = 'https://aip.baidubce.com/oauth/2.0/token'


def fetch_token():
    """Fetch token from baidu API.

        Returns:
            token on success
    """

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
            print('please ensure has check the  ability')
            exit()
        return result['access_token']
    else:
        print('please overwrite the correct API_KEY and SECRET_KEY')
        exit()


def get_validate_code(data):
    """Convert validate image to strings through Baidu API.

        Args:
            data (str): unencoded validate image's url

        Returns:
            return stripped validate_code(str) if true, print err otherwise

    """
    url = OCR_URL + fetch_token()
    img = urlencode({'image': data})
    req = Request(url, img.encode('utf-8'))
    try:
        f = urlopen(req)
        result_str = f.read().decode()
        validate_code = json.loads(result_str)[
            "words_result"][0]["words"].strip()
        return validate_code
    except URLError as err:
        print(err)
