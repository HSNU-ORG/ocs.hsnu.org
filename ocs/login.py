import json
from time import sleep
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.common.action_chains import ActionChains
from urllib.parse import urlencode, quote_plus
from .baidu import get_validate_code


def login(url, account, password):
    '''Login to 第二代校務行政系統 automatically.
    
        Args:
            url: the site of the school's 第二代校務行政系統 you want to go to
            account: student's 第二代校務行政系統 account
            password: student's 第二代校務行政系統 password
        Returns:
            nothing
    '''

    loggedin = False

    # browser configuration
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    # options.add_argument("headless")
    global browser
    browser = webdriver.Chrome(chrome_options=options)
    browser.get(url)

    # try to log in
    while not loggedin:
        # get img and turn into validate_code
        validate_img = browser.find_element_by_id(
            'validatePic').get_attribute("src")[22:]
        validate_code = get_validate_code(validate_img)

        # fill in the info
        browser.find_element_by_id('loginId').send_keys(account)
        browser.find_element_by_id('pas1').send_keys(password)
        browser.find_element_by_id('validateCode').send_keys(validate_code)
        browser.find_element_by_id('login').click()
        sleep(0.1)
        login_stat = login_success(password)
        if login_stat == 1:
            account = input("帳號不存在,請重新輸入：")
            global Account
            Account = account
        elif login_stat == 2:
            password = input("帳號或密碼錯誤,請重新輸入：")
            global Password
            Password = password
        elif login_stat == 0:
            loggedin = True
    browser.implicitly_wait(10)


def login_success(password):
    """Check if login successful.

        Args:
            password: password to the account logging in
        Returns:
            return integer, 0 if success, 1 if account does not exist, 2 if password wrong, 3 if validate code wrong
    """

    try:
        err_text = browser.find_element_by_xpath(
            "//div[@id='ui-id-6']/p[1]").text
        browser.find_element_by_xpath(
            "//div[@class='ui-dialog-buttonset']/button[1]").click()
        if err_text == "無此帳號！":
            return 1
        elif err_text == "密碼錯誤！":
            return 2
        else:
            return 3
    except NoSuchElementException:
        sleep(1)
        try:
            browser.find_element_by_id("oldpd").send_keys(password)
            newpd = password + '1'
            browser.find_element_by_id("newpd").send_keys(newpd)
            browser.find_element_by_id("agnpd").send_keys(newpd)
            browser.find_element_by_id("btnSubmit").click()
        except NoSuchElementException:
            return 0
        return 0


def get_grades(url, account, password):
    """Get grades from 第二代校務行政系統.

        Args:
            url: the site of the school's 第二代校務行政系統 you want to go to
            account: student's 第二代校務行政系統 account
            password: student's 第二代校務行政系統 password
        Returns:
            test scores in .json format
    """
    allscores = []
    login(url, account, password)
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
    for sem in semesters:
        yr = sem.find_element_by_css_selector("td:nth-child(2)").get_attribute('textContent')  #year
        smt = sem.find_element_by_css_selector("td:nth-child(3)").get_attribute('textContent') #semester
        grd = sem.find_element_by_css_selector("td:nth-child(14)").get_attribute('textContent') #grade
        sem.click()
        sleep(0.7)
        tests = list(browser.find_elements_by_xpath(
            "//tr[@class='ui-widget-content jqgrow ui-row-ltr']"))
        rows = len(tests) - 2
        tests = tests[year:year+3]
        count = 0
        for test in tests:
            count += 1
            testID = yr + smt + grd + str(count) #[year][semester][grade][test] ex.[108][1][2][3]
            scores = {}
            scores["testID"] = testID
            try:
                test.click()
            except ElementClickInterceptedException:
                browser.find_element_by_xpath(
                    "(//div[@class='ui-dialog-buttonset'])[2]/button").click()
                break
            sleep(0.7)
            grades = list(browser.find_elements_by_xpath(
                "//tr[@class='ui-widget-content jqgrow ui-row-ltr']"))[rows:-1]
            for s in grades:
                if s.find_element_by_css_selector("td:nth-child(5)").text[0] not in "0123456789":
                    scores[s.find_element_by_css_selector("td:nth-child(5)").text] = int(s.find_element_by_css_selector(
                        "td:nth-child(6)").text)
            allscores.append(scores)
    return json.dumps(allscores, ensure_ascii=False, indent=4)
