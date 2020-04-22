from ocs.login import get_grades
from dotenv import load_dotenv
import os

load_dotenv()

url = "https://sschool.tp.edu.tw/Login.action?schNo=330301"
Account = os.getenv("ACCOUNT")
Password = os.getenv("PASSWORD")


def main():
    f = open("result.json", "w")
    f.write(get_grades(url, Account, Password))
    f.close


main()
