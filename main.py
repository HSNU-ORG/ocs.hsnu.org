from ocs.login import login, get_grades
url = "https://sschool.tp.edu.tw/Login.action?schNo=330301"

if __name__ == '__main__':
    Account = input('enter account: ')
    Password = input('enter password: ')
    login(url, Account, Password)
    get_grades()
