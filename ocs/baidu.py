import json
from urllib.request import urlopen, Request
from urllib.error import URLError
from urllib.parse import urlencode, quote_plus


# account info
API_KEY = 'qPO9LT4d030sY00t6KL8Gsqx'
SECRET_KEY = 'nf8Z3vuN2KFIVzgvAa3odLVZcK0dklQy'
OCR_URL = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic?access_token="
TOKEN_URL = 'https://aip.baidubce.com/oauth/2.0/token'
image = '/9j/4AAQSkZJRgABAgAAAQABAAD/2wBDAAgGBgcGBQgHBwcJCQgKDBQNDAsLDBkSEw8UHRofHh0aHBwgJC4nICIsIxwcKDcpLDAxNDQ0Hyc5PTgyPC4zNDL/2wBDAQkJCQwLDBgNDRgyIRwhMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjL/wAARCAAWAEIDASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9oADAMBAAIRAxEAPwDrfD/h/wAJt4A0O5uPDmjs39l281xcPYRs7HylLEnbknqSepp8Ok+A5bB78aHo/wBkicJJJ/ZqcHjtsz3HatDwZ/yI3h//ALBtt/6KWsqV5rOO68OQAqJrhY4G25KwyZZsKeWC4YE579RiohJ3ua15uhFWtZp9Lvmtp16mnc6X8P4dFGqjw9ojWjZCMNNjDSMCRtUFQc5B/n05pmm6N4K1K4a1/wCEQ0+1ulQyeRdaTGjFMgbh8uMZOOvY1q6lpQ1DSLe0spfss9myS2pPzKGQYUHOcjH+T0OHHdajd+NtPW8nsp5LOOVpEsz8kQIK8knO7OAVxwAPU45Z1aiqJLZ2X37/AHHG41VJRluO1a2+G+gXiWup6JokMzxiQJ/ZStlSSM5VCOoNXNL0j4ea1ps1/ZaFoT2kLMssr6bHGEIAJzuQcAEHPSq3xEdn8EaiWP8Azz/9GrW3qk8UGhak1xD58AtZTJFvK7xsOVyOmRxmvUeHXIn1PRnhlChzq/N66aW8jkopvh3NLCW8H21vZTSmGLUJtIiW2Y5IHzEdDg9Rx3xg46d/A3hVMZ8M6Kc/9OEX/wATXA3VtqVv8PNMvb7Xo73ShJEzaYDs8xN3+rEo+Ykd1/h2nH3BXrs7ZfHpWeKpQgk4ea+45MLUlN2kfFfi+CK28a69b28SRQxajcJHHGoVUUSMAABwAB2oqTxt/wAj74i/7Cdz/wCjWorNbFPc9b8P/Gvw3pXhvS9OnstVaa0tIoJGSKMqWVApIzIOMip5PjT4Mk1GK/fS9YN1EuxH8uPgc9vNx3NFFZ2OpvmST1E1D40eC9UgWC80rWJY1beB5aLzgjtKPU0th8afBOmRGOz0fVYVPUiGIluvUmTJ6nrRRVUoRVTmS1C+vN1KWq/FP4e63dLc6joeszTKgjDYVcKCTjCyjuTVrSvjH4H0S1a207SNZhhZzIV2I2WIAzlpT2Aoors9pK1rlutUa5b6Fez+J/wzs79L+Lw5qq3SOZFYRoVVvUKZdox2444xW837QXhMnP8AZ+tf9+Yv/jlFFc1WTm/edzhilCp7uh8/+ItQi1bxNqupW6usN3eTTxrIAGCu5YA4JGcH1ooooQ3uf//Z'


def fetch_token():
    """Fetch token from baidu API

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


def _request(data):
    """Convert validate image to strings through Baidu API

        Args:
            data (str): encoded validate image's url

        Returns:
            return validate code if true, print err otherwise

    """
    url = OCR_URL + fetch_token()
    req = Request(url, data.encode('utf-8'))
    try:
        f = urlopen(req)
        result_str = f.read().decode()
        return result_str
    except URLError as err:
        print(err)


if __name__ == "__main__":
    result_json = json.loads(_request(urlencode({'image': image})))
    print(result_json)
