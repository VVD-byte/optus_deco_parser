import xml.etree.ElementTree as ET


class XmlWriter:
    def __init__(self, data):
        self.tree = ET.ElementTree()
        self.data = data

    def main(self):
        a = {}
        root = ET.Element('data')
        for i in self.data:
            if i['Бренд'] in a.keys():
                a[i['Бренд']].append(i)
            else:
                a[i['Бренд']] = [i]
        for i in a:
            sub_root = ET.Element('Брэнд', name=i)
            for j in range(len(a[i])):
                sub_sub_root = ET.Element('Товар')
                ET.SubElement(sub_sub_root, 'Артикул').text = a[i][j]['Артикул']
                ET.SubElement(sub_sub_root, 'Наличие').text = a[i][j]['Наличие']
                sub_root.append(sub_sub_root)
            root.append(sub_root)
        handle = ET.tostring(root, encoding='utf-8', xml_declaration=True).decode("utf-8")
        print(handle)
        print(root)
        with open('text.xml', 'w') as t:
            t.writelines(handle)
