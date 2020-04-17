from ocs.login import login, get_grades
url = "https://sschool.tp.edu.tw/Login.action?schNo=330301"
Account = ''
Password = ''

if __name__ == '__main__':
    get_grades(url, Account, Password)
    