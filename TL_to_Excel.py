import xml.etree.ElementTree as ET
import xlwt

def write_row(sheet, row, data):
    r = sheet.row(row)
    for index, col in enumerate(data):
        r.write(index, col)
    return row + 1

tree = ET.parse('testsuites_all.xml')
root = tree.getroot()

impact_level = ['Smoke', 'Low', 'Med', 'High']

book = xlwt.Workbook()
sheet1 = book.add_sheet('PySheet1')
cols = ['Feature', 'Impact Level', 'Test Case']
row = write_row(sheet1, 0, cols)

print(root.get('name'))

for feature in root.findall('./*[@name]'):
    feature_name = feature.get('name')
    print(f'--------------------- {feature_name} ---------------------')
    for impact in impact_level:
        print(f'--> {impact} <--')
        # Find all testcases in <Feature>/AAs/<impact>/ folders
        for testcase in feature.findall(f".//*[@name='AAs']/*[@name='{impact}']/testcase"):
            test_name = testcase.get('name')
            print(test_name)
            row = write_row(sheet1, row, [feature_name, impact, test_name])
        # Same as above but checks for AA folder (numerous features seem to have this typo)
        for testcase in feature.findall(f".//*[@name='AA']/*[@name='{impact}']/testcase"):
            test_name = testcase.get('name')
            print(test_name)
            row = write_row(sheet1, row, [feature_name, impact, test_name])

book.save('test.xls')
