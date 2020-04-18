import openpyxl

wb = openpyxl.load_workbook('example.xlsx')

sheet = wb['Sheet1']

#Cell = sheet['B1']
#print(type(Cell))
#print(Cell.value)
#print(Cell.row)
#print(Cell.column)
#print(Cell.coordinate)
print(sheet.cell(row=3, column=2).value)


#print (sheet['A1':'C3'])