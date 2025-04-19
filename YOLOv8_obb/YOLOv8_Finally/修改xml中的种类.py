import os
import xml.etree.ElementTree as ET


def update_xml_files(directory):
    # 遍历指定目录下的所有文件和子目录
    for root_dir, _, files in os.walk(directory):
        for file_name in files:
            if file_name.endswith('.xml'):
                file_path = os.path.join(root_dir, file_name)

                # 解析XML文件
                tree = ET.parse(file_path)
                root = tree.getroot()

                # 查找并更新<truncated>标签的值
                for truncated in root.iter('truncated'):
                    if truncated.text == '3':
                        truncated.text = '1'

                # 保存修改后的XML文件
                tree.write(file_path, encoding='utf-8', xml_declaration=True)
                print(f"Updated: {file_path}")


# 调用函数并传入你的XML文件所在目录路径
directory_path = r"F:\YOLO\A垃圾数据集\KHSLJ"
update_xml_files(directory_path)