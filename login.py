import base64, requests, sys, json, ssl, time, json, pymongo
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.common.action_chains import ActionChains
from urllib.request import urlopen, Request
from urllib.error import URLError
from urllib.parse import urlencode, quote_plus
from time import sleep
from pymongo import MongoClient

con = MongoClient(host='localhost', port=27017)
db = con.HSNUorg
collection = db.test

url = "https://sschool.tp.edu.tw/Login.action?schNo=330301"
Account = "710918"
Password = "ray131184845"
API_KEY = 'qPO9LT4d030sY00t6KL8Gsqx'

SECRET_KEY = 'nf8Z3vuN2KFIVzgvAa3odLVZcK0dklQy'
OCR_URL = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic"
TOKEN_URL = 'https://aip.baidubce.com/oauth/2.0/token'

# 拿API token
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
            print ('please ensure has check the  ability')
            exit()
        return result['access_token']
    else:
        print ('please overwrite the correct API_KEY and SECRET_KEY')
        exit()

def _request(url, data):
    req = Request(url, data.encode('utf-8'))
    has_error = False
    try:
        f = urlopen(req)
        result_str = f.read().decode()
        return result_str
    except URLError as err:
        print(err)

# 檢查登入是否成功
def login_success():
    # 確認是否有登入錯誤的關閉按鈕
    try:
        browser.find_element_by_xpath("//div[@class='ui-dialog-buttonset']/button[1]").click()
    except NoSuchElementException:
        return True
    return False

# 獲取成績
def get_grades():

    ActionChains(browser).move_to_element(browser.find_element_by_xpath("//li[@name='01各項查詢']/a")).perform()  # 進入各項查詢項目
    browser.find_element_by_name('A0410S').click()  # 點擊查詢個人成績
    sleep(0.5)
    browser.find_element_by_id("contents").click()
    semesters = browser.find_elements_by_xpath("//tr[@class='ui-widget-content jqgrow ui-row-ltr']")
    year = []
    for row in semesters:  # 確認學期數
        year.append(row.find_element_by_css_selector("td:nth-child(2)").text)
    if len(year) <= 2:
        semesters = semesters[0]
    elif year[2] == year[0]:
        semesters = semesters[:2]
    else:
        for i in range(len(year)):
            if int(year[i]) > int(year[i+1]):
                semesters = semesters[:i+1]
                break
    year = len(year) - 2
    done = False
    for sem in semesters:  # 迭代學期
        sem.click()
        sleep(1)
        tests = list(browser.find_elements_by_xpath("//tr[@class='ui-widget-content jqgrow ui-row-ltr']"))
        rows = len(tests) - 2
        tests = tests[year:year+3]
        for test in tests:  # 迭代考試
            try:
                test.click()
            except ElementClickInterceptedException:
                browser.find_element_by_xpath("(//div[@class='ui-dialog-buttonset'])[2]/button").click()
                break
            sleep(1)
            grades = list(browser.find_elements_by_xpath("//tr[@class='ui-widget-content jqgrow ui-row-ltr']"))[rows:-1]
            scores = {}
            for s in grades:
                if s.find_element_by_css_selector("td:nth-child(5)").text[0] not in "0123456789":
                    scores[s.find_element_by_css_selector("td:nth-child(5)").text] = s.find_element_by_css_selector(
                        "td:nth-child(6)").text
            print(scores)  # 印出成績
loggedin = False
login_tries = 0
token = fetch_token()
image_url = OCR_URL + "?access_token=" + token
validate_result = ""
options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
#options.add_argument("headless")
browser = webdriver.Chrome(chrome_options=options)
browser.get(url)
while not loggedin:  # 循環登入程序直到成功
    validate_result = ""
    validate_img = browser.find_element_by_id('validatePic').get_attribute("src")[22:].encode(encoding="utf-8")
    result_json = json.loads(_request(image_url, urlencode({'image': validate_img})))
    for words_result in result_json["words_result"]:
        validate_result += words_result["words"]
    validate_result = validate_result.strip()
    browser.find_element_by_id('loginId').send_keys(Account)    # 輸入帳號
    browser.find_element_by_id('pas1').send_keys(Password)  # 輸入密碼
    browser.find_element_by_id('validateCode').send_keys(validate_result)   # 輸入驗證碼
    browser.find_element_by_id('login').click() # 點擊登入鍵
    time.sleep(0.1)
    loggedin = login_success()  # 確認是否登入成功
browser.implicitly_wait(10)

get_grades()   # 獲取成績