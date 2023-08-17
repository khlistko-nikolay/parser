import xlsxwriter
from par_information_about_cheks import check



def writer(parametr):
    book = xlsxwriter.Workbook("/Users/nikolajhlistko/Desktop/par_inf_checks.xlsx")
    page = book.add_worksheet("checks")
    

    row = 0
    column = 0


    page.set_column("A:A", 150)

    page.write(row, column, "Информация о проверках")
   
    row += 1


    for item in parametr():
        page.write(row, column, item)
        row += 1

    book.close()

writer(check)


