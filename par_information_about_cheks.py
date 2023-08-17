import requests
from bs4 import BeautifulSoup
from time import sleep 
import re

headers_fek = {"User-Agent":
           "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5.1 Safari/605.1.15"}

def check():

    url = "https://fek.ru/reestr/7720584916-gbou-shkola-№-2031-8452"

    response = requests.get(url, headers=headers_fek)

    soup = BeautifulSoup(response.text, "lxml")

    information_about_checks = soup.find("div", id="inspections", class_="nrstrBlock nrstrBlock_half").find_all("div", class_="nrstrBlock__row")

    for i in information_about_checks:
        a = i.text
        a = re.sub("^\s+|\n|\r|\s+$", ' ', a)
        yield a