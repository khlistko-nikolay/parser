from xlsxwriter import Workbook
from bs4 import BeautifulSoup
from lxml import html, etree
from requests import session
from json import loads

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5.1 Safari/605.1.15"


def getInfo(inn):
    client = session()
    client.headers.update({ "User-Agent": USER_AGENT })

    # Получаем csrf токен
    responseData = client.get("https://fek.ru").text
    soup = BeautifulSoup(responseData, "lxml")
    client.headers.update({"X-CSRF-TOKEN": soup.select_one("meta[name=\"csrf-token\"]").get("content")})

    # Выполняем запрос, с поиском компании
    companyData = loads(client.post("https://fek.ru/search-company", data={
        "query": inn
    }, headers={
        "Accept-Language": "ru,en;q=0.9",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
    }).text)

    # Парсим сайт с результатами
    companyUri = companyData.get("suggestions")[0].get("data").get("uri")
    companyResultpageContent = client.get(f"https://fek.ru/reestr/{companyUri}").content
    pageTree = html.fromstring(companyResultpageContent)

    # Парсим реестр проверок прокуратуры, если он имеется
    inspections = []

    if ("По данным генеральной прокуратуры РФ для данного ИНН найдены следующие записи о проверках:" in pageTree.xpath("/html/body/div[3]/div[5]/div[2]/p/text()")[0]):
        reestrData = etree.tostring(pageTree.xpath("/html/body/div[3]/div[5]/div[2]")[0])
        soup = BeautifulSoup(reestrData, "lxml")

        for entry in soup.find_all(class_="nrstrBlock__row"):
            inspectionTextList = entry.get_text().split()

            inspections.append({
                "year": "{} {}".format(inspectionTextList[0], inspectionTextList[1]),
                "inspections": "{} {}".format(inspectionTextList[2], inspectionTextList[3]),
                "violations": "{} {}".format(inspectionTextList[4], inspectionTextList[5]).replace("(", "").replace(")", ""),
            })

    return {
        "inn": inn,
        "name": pageTree.xpath("/html/body/div[3]/div[5]/div[1]/div/div[1]/div[1]/div[2]/text()")[0],
        "regDate": pageTree.xpath("/html/body/div[3]/div[5]/div[1]/div/div[1]/div[2]/div[2]/text()")[0],
        "director": pageTree.xpath("/html/body/div[3]/div[5]/div[1]/div/div[1]/div[5]/div[2]/p/text()")[0],
        "legal_address": pageTree.xpath("/html/body/div[3]/div[5]/div[1]/div/div[1]/div[3]/div[2]/text()")[0],
        "kind_of_activity": pageTree.xpath("/html/body/div[3]/div[5]/div[1]/div/div[1]/div[6]/div[2]/p[1]/text()")[0],
        "average_rating": pageTree.xpath("/html/body/div[3]/div[5]/div[1]/div/div[2]/div[1]/div[1]/span[1]/text()")[0],
        "negative_factors": pageTree.xpath("/html/body/div[3]/div[5]/div[1]/div/div[2]/div[1]/div[2]/div[1]/p[1]/span/text()")[0],
        "positive_factors": pageTree.xpath("/html/body/div[3]/div[5]/div[1]/div/div[2]/div[1]/div[2]/div[2]/p[1]/text()")[0],
        "requiring_attention": pageTree.xpath("/html/body/div[3]/div[5]/div[1]/div/div[2]/div[1]/div[2]/div[3]/p[1]/span/text()")[0],
        "inspections": inspections
    }

def createTable(data):
    workbook = Workbook("/Users/nikolajhlistko/Desktop/fek_test.xlsx")
    worksheet = workbook.add_worksheet()

    worksheet.set_column(0, 0, 50)
    worksheet.set_column(0, 1, 50)
    worksheet.set_column(0, 2, 50)
    worksheet.set_column(0, 3, 50)
    worksheet.set_column(0, 4, 50)
    worksheet.set_column(0, 5, 50)
    worksheet.set_column(0, 6, 50)
    worksheet.set_column(0, 7, 50)
    worksheet.set_column(0, 8, 50)
    worksheet.set_column(0, 8, 50)
    worksheet.set_column(0, 8, 50)
    worksheet.set_column(0, 8, 50)

    worksheet.write(0, 0, "Наименование")
    worksheet.write(0, 1, data.get("name"))

    worksheet.write(1, 0, "Дата регистрации")
    worksheet.write(1, 1, data.get("regDate"))

    worksheet.write(2, 0, "ИНН")
    worksheet.write(2, 1, data.get("inn"))

    worksheet.write(3, 0, "Директор")
    worksheet.write(3, 1, data.get("director"))

    worksheet.write(4, 0, "Адрес")
    worksheet.write(4, 1, data.get("legal_address"))

    worksheet.write(5, 0, "Вид деятельности")
    worksheet.write(5, 1, data.get("kind_of_activity"))

    worksheet.write(6, 0, "Рейтинг")
    worksheet.write(6, 1, data.get("average_rating"))

    worksheet.write(7, 0, "Негативные факторы")
    worksheet.write(7, 1, data.get("negative_factors"))

    worksheet.write(8, 0, "Положительные факторы")
    worksheet.write(8, 1, data.get("positive_factors"))

    worksheet.write(9, 0, "Факторы требующие внимани]")
    worksheet.write(9, 1, data.get("requiring_attention"))

    worksheet.write(10, 0, "Данные о проверках:")

    worksheet.write(11, 0, "Год")
    worksheet.write(11, 1, "Количество инспекций")
    worksheet.write(11, 2, "Нарушения")

    row = 12
    for inspection in data.get("inspections"):
        worksheet.write(row, 0, inspection.get("year"))
        worksheet.write(row, 1, inspection.get("inspections"))
        worksheet.write(row, 2, inspection.get("violations"))
        row += 1

    workbook.close()

if __name__ == "__main__":
    inn = 7720567460
    createTable(getInfo(inn))

