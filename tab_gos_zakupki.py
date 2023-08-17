import xlsxwriter
from par_gos_zakupki import get_price_year



def writer(parametr):
    book = xlsxwriter.Workbook("/Users/nikolajhlistko/Desktop/gos_zakupki.xlsx")
    page = book.add_worksheet("Госзакупки")
    

    row = 0
    column = 0


    page.set_column("A:A", 30)
    page.set_column("B:B", 30)
    page.write(row, column, "Сумма закупки")
    page.write(row, column+1, "Дата закупки")
    row += 1


    for item in parametr():
        page.write(row, column, item[0])
        page.write(row, column+1, item[1])
        row += 1

    book.close()


writer(get_price_year)
