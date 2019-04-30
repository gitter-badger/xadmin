import xlrd
def fileload(filename = 'Template.xls'):
  dataset = []
  workbook = xlrd.open_workbook(filename)
  table = workbook.sheets()[0]
  for row in range(table.nrows):
    dataset.append(table.row_values(row))
  return dataset
print(fileload())