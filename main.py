from ocs.login import login, get_grades
from dotenv import load_dotenv, find_dotenv
from pathlib import Path
import os

load_dotenv()

url = "https://sschool.tp.edu.tw/Login.action?schNo=330301"
Account = os.getenv("ACCOUNT")
Password = os.getenv("PASSWORD")

def main(request):
    get_grades(url, Account, Password)

main(1)
