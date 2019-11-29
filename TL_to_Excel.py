import xml.etree.ElementTree as ET
import xlsxwriter

def create_doc():
    book = xlsxwriter.Workbook('test.xls')
    sheet1 = book.add_worksheet('PySheet1')
    header_format = book.add_format({
        'align': 'left',
        'valign': 'vcenter',
        'bold': True,
        'font_size': 14
    })
    feature_format = book.add_format({
        'align': 'left',
        'valign': 'vcenter',
        'text_wrap': True
    })
    impact_format = book.add_format({
        'align': 'center',
        'valign': 'vcenter',
    })
    testcase_format = book.add_format({
        'align': 'left',
        'text_wrap': True
    })
    sheet1.set_column('A:A', 20, feature_format)
    sheet1.set_column('B:B', 10, impact_format)
    sheet1.set_column('C:C', 75, testcase_format)
    sheet1.set_column('D:D', 15)
    cols = ['Feature', 'Impact', 'Test Case', 'Testing']
    sheet1.write_row('A1', cols, header_format)
    return (book, sheet1)

tree = ET.parse('testsuites_all.xml')
root = tree.getroot()

impact_level = ['Smoke', 'Low', 'Med', 'High']

book, sheet = create_doc()
row = 1

for feature in root.findall('./*[@name]'):
    feature_name = feature.get('name')
    feature_row_start = row
    print(f'--------------------- {feature_name} ---------------------')
    for impact in impact_level:
        impact_row_start = row
        print(f'--> {impact} <--')
        # Find all testcases in <Feature>/AAs/<impact>/ folders
        for testcase in feature.findall(f".//*[@name='AAs']/*[@name='{impact}']/testcase"):
            test_name = testcase.get('name')
            print(test_name)
            sheet.write_row(row, 0, (feature_name, impact, test_name))
            row += 1
        # Same as above but checks for AA folder (numerous features seem to have this typo)
        for testcase in feature.findall(f".//*[@name='AA']/*[@name='{impact}']/testcase"):
            test_name = testcase.get('name')
            print(test_name)
            sheet.write_row(row, 0, (feature_name, impact, test_name))
            row += 1
        if impact_row_start != row: sheet.merge_range(impact_row_start, 1, row-1, 1, impact)
    if feature_row_start != row: sheet.merge_range(feature_row_start, 0, row-1, 0, feature_name)

book.close()
