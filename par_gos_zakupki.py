import requests
from bs4 import BeautifulSoup
from time import sleep 

headers_gos_zakupki = {"User-Agent":
           "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5.1 Safari/605.1.15"}



def get_price_year():
    inn = 7720584916
    for count in range(1,8):
    
        url = "https://zakupki.gov.ru/epz/order/extendedsearch/results.html?searchString={inn}}&morphology=on&search-filter=Дате+размещения&pageNumber={count}&sortDirection=false&recordsPerPage=_50&showLotsInfoHidden=false&sortBy=UPDATE_DATE&fz44=on&fz223=on&af=on&ca=on&pc=on&pa=on&currencyIdGeneral=-1"

        response = requests.get(url, headers=headers_gos_zakupki)

        soup = BeautifulSoup(response.text, "lxml")

        data = soup.find_all("div", class_="row no-gutters registry-entry__form mr-0")

        for i in data:
            price = i.find("div", class_="price-block__value").text
            year = i.find("div", class_="data-block__value").text
            yield price, year
