import requests
from bs4 import BeautifulSoup
from time import sleep 

headers_fek = {"User-Agent":
           "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5.1 Safari/605.1.15"}

 
def param():

  url = "https://fek.ru/reestr/7720584916-gbou-shkola-№-2031-8452"

  response = requests.get(url, headers=headers_fek)

  soup = BeautifulSoup(response.text, "lxml")

  data = soup.find_all("div", class_="nrstrMainBlock__cnt")


  for i in data:

    name_school = i.find("div", class_="nrstrMainBlock__leftRowCnt").text
    date_of_registration = i.select('.nrstrMainBlock__leftRowCnt')[1].text
    director = i.select('.nrstrMainBlock__leftRowCnt')[4].text
    legal_address = i.select('.nrstrMainBlock__leftRowCnt')[2].text
    kind_of_activity = i.select('.nrstrMainBlock__leftRowCnt')[6].find("p", style="margin-bottom: 20px;").text
  

    average_rating = i.find("div", class_="mbCircle").text
    negative_factors = i.find("div", class_="mbTotal__count mbTotal__count_negative").find("p").text
    positive_factors = i.find("div", class_="mbTotal__count mbTotal__count_positive").find("p").text
    requiring_attention = i.find("div", class_="mbTotal__count mbTotal__count_warning").find("p").text

    yield name_school, date_of_registration, director, legal_address, kind_of_activity, average_rating, negative_factors, positive_factors, requiring_attention
      


    
    