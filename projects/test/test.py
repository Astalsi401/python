import openpyxl

pwd = 'd:/Documents/python/projects/schedule'


timeslot = openpyxl.load_workbook(f"{pwd}/test.xlsx")
sh = timeslot['Sheet1']

availability = []
for rows in sh.iter_rows():
    row_cells = []
    for cell in rows:
        row_cells.append(cell.value)
    availability.append(tuple(row_cells))

print(len(availability[0]))
