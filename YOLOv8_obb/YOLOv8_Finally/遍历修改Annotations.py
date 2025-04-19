import os


def rename_files_in_directory(directory, start_number):
    # 获取目录中的所有文件并过滤出 .xml 文件
    files = [f for f in os.listdir(directory) if f.endswith('.xml')]

    # 提取文件名中的数字部分，并将其与文件名一起存储为元组
    file_numbers = []
    for filename in files:
        name, ext = os.path.splitext(filename)
        if name.startswith('photo_'):
            try:
                number = int(name[len('photo_'):])
                file_numbers.append((number, filename))
            except ValueError:
                print(f'Skipping file {filename}: Invalid number format')

    # 按照数字部分进行排序
    file_numbers.sort(key=lambda x: x[0])

    # 根据排序结果重命名文件
    for i, (old_number, filename) in enumerate(file_numbers):
        new_number = start_number + i
        new_filename = f'photo_{new_number:02d}{ext}'

        old_file_path = os.path.join(directory, filename)
        new_file_path = os.path.join(directory, new_filename)

        os.rename(old_file_path, new_file_path)
        print(f'Renamed: {filename} to {new_filename}')


# 使用示例
directory_path = r'.\my_data_1\Annotations'  # 替换为你的目录路径
start_number = 1 # 你希望开始的序号
rename_files_in_directory(directory_path, start_number)