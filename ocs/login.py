from time import sleep
import json
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.common.action_chains import ActionChains
from .baidu import _request
from urllib.parse import urlencode, quote_plus


def login(url, account, password):
    '''
        login to 第二代校務行政系統 automatically.

        Args:
            url: the site of the school's 第二代校務行政系統 you want to go to
            account: student's 第二代校務行政系統 account
            password: student's 第二代校務行政系統 password

        Returns:
            nothing

    '''
    loggedin = False
    login_tries = 0
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    # options.add_argument("headless")
    browser = webdriver.Chrome(chrome_options=options)
    browser.get(url)
    while not loggedin:
        validate_result = ""
        validate_img = browser.find_element_by_id('validatePic').get_attribute("src")[
                       22:].encode(encoding="utf-8")
        result_json = json.loads(_request(urlencode({'image': validate_img})))
        for words_result in result_json["words_result"]:
            validate_result += words_result["words"]
        validate_result = validate_result.strip()
        browser.find_element_by_id('loginId').send_keys(account)
        browser.find_element_by_id('pas1').send_keys(password)
        browser.find_element_by_id('validateCode').send_keys(validate_result)
        browser.find_element_by_id('login').click()
        time.sleep(0.1)
        loggedin = login_success()
    browser.implicitly_wait(10)


def login_success():
    """
        check if login successful

        Returns:
            return boolean, True if success, otherwise False

    """
    try:
        browser.find_element_by_xpath(
            "//div[@class='ui-dialog-buttonset']/button[1]").click()
    except NoSuchElementException:
        return True
    return False


def get_grades():
    """
        get grades

        Returns:
            print grades

    """
    ActionChains(browser).move_to_element(
        browser.find_element_by_xpath("//li[@name='01各項查詢']/a")).perform()
    browser.find_element_by_name('A0410S').click()
    sleep(0.5)
    browser.find_element_by_id("contents").click()
    semesters = browser.find_elements_by_xpath(
        "//tr[@class='ui-widget-content jqgrow ui-row-ltr']")
    year = []
    for row in semesters:
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
    for sem in semesters:
        sem.click()
        sleep(1)
        tests = list(browser.find_elements_by_xpath(
            "//tr[@class='ui-widget-content jqgrow ui-row-ltr']"))
        rows = len(tests) - 2
        tests = tests[year:year+3]
        for test in tests:
            try:
                test.click()
            except ElementClickInterceptedException:
                browser.find_element_by_xpath(
                    "(//div[@class='ui-dialog-buttonset'])[2]/button").click()
                break
            sleep(1)
            grades = list(browser.find_elements_by_xpath(
                "//tr[@class='ui-widget-content jqgrow ui-row-ltr']"))[rows:-1]
            scores = {}
            for s in grades:
                if s.find_element_by_css_selector("td:nth-child(5)").text[0] not in "0123456789":
                    scores[s.find_element_by_css_selector("td:nth-child(5)").text] = s.find_element_by_css_selector(
                        "td:nth-child(6)").text
            print(scores)
