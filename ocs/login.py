url = "https://sschool.tp.edu.tw/Login.action?schNo=330301"
Account = "710918"
Password = "ray131184845"


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
