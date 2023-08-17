import xlsxwriter
from par_fek import param



def writer(parametr):
    book = xlsxwriter.Workbook("/Users/nikolajhlistko/Desktop/par_fek.xlsx")
    page = book.add_worksheet("fek")
    

    row = 0
    column = 0


    page.set_column("A:A", 50)
    page.set_column("B:B", 50)
    page.set_column("C:C", 50)
    page.set_column("D:D", 50)
    page.set_column("E:E", 50)
    page.set_column("F:F", 50)
    page.set_column("G:G", 50)
    page.set_column("H:H", 50)
    page.set_column("I:I", 50)
    page.set_column("J:J", 200)

    page.write(row, column, "Наименование школы")
    page.write(row, column+1, "Дата регистрациии")
    page.write(row, column+2, "Директор и инн")
    page.write(row, column+3, "Адрес школы")
    page.write(row, column+4, "Тип образования")
    page.write(row, column+5, "Средняя оценка организации")
    page.write(row, column+6, "Кол-во нигативных факторов")
    page.write(row, column+7, "Кол-во положительных факторов")
    page.write(row, column+8, "Кол-во факторов требующих проверки")
    row += 1


    for item in parametr():
        page.write(row, column, item[0])
        page.write(row, column+1, item[1])
        page.write(row, column+2, item[2])
        page.write(row, column+3, item[3])
        page.write(row, column+4, item[4])
        page.write(row, column+5, item[5])
        page.write(row, column+6, item[6])
        page.write(row, column+7, item[7])
        page.write(row, column+8, item[8])
        row += 1

    book.close()

writer(param)


