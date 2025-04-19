import os
import shutil


def copy_xml_files(src_folder, dest_folder):
    # 如果目标文件夹不存在，则创建
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

    # 遍历源文件夹
    for foldername, subfolders, filenames in os.walk(src_folder):
        for filename in filenames:
            if filename.endswith('.jpg'):
                # 构建完整的源文件路径和目标文件路径
                src_file = os.path.join(foldername, filename)
                dest_file = os.path.join(dest_folder, filename)

                # 复制文件
                shutil.copy(src_file, dest_file)
                print(f"Copied {src_file} to {dest_file}")


# 源文件夹路径和目标文件夹路径
source_folder = r'F:\YOLO\A垃圾数据集\YHLJ'  # 替换为你的源文件夹路径
destination_folder = r'F:\YOLO\A垃圾数据集\1'  # 替换为你想要保存XML文件的目标文件夹路径

copy_xml_files(source_folder, destination_folder)