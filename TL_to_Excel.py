import xml.etree.ElementTree as ET

tree = ET.parse('testsuites_all.xml')
root = tree.getroot()

impact_level = ['Smoke','Low','Med','High']

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
        # Same as above but checks for AA folder (numerous features seem to have this typo)
        for testcase in feature.findall(f".//*[@name='AA']/*[@name='{impact}']/testcase"):
            test_name = testcase.get('name')
            print(test_name)