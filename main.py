import base64
import requests
import sys
import json
import ssl
import time
import json
import pymongo
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.common.action_chains import ActionChains
from urllib.request import urlopen, Request
from urllib.error import URLError
from urllib.parse import urlencode, quote_plus
from time import sleep
import ocs.login as ocs

loggedin = False
login_tries = 0
image_url = OCR_URL + "?access_token=" + ocs.fetch_token()
validate_result = ""
options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
# options.add_argument("headless")
browser = webdriver.Chrome(chrome_options=options)
browser.get(url)
while not loggedin:
    validate_result = ""
    validate_img = browser.find_element_by_id('validatePic').get_attribute("src")[
        22:].encode(encoding="utf-8")
    result_json = json.loads(ocs._request(
        image_url, urlencode({'image': validate_img})))
    for words_result in result_json["words_result"]:
        validate_result += words_result["words"]
    validate_result = validate_result.strip()
    browser.find_element_by_id('loginId').send_keys(Account)
    browser.find_element_by_id('pas1').send_keys(Password)
    browser.find_element_by_id('validateCode').send_keys(validate_result)
    browser.find_element_by_id('login').click()
    time.sleep(0.1)
    loggedin = ocs.login_success()
browser.implicitly_wait(10)

ocs.get_grades()
