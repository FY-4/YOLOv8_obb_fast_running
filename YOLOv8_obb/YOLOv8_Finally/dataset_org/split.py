# 该脚本将YOLO目标检测的样本图片和标注数据按比例切分为三部分：训练集、验证集和测试集
import shutil
import random
import os
import collections

# 修改你的项目路径、原始图像数据和标签路径
cur_path = "F:/YOLO/YOLOv8_Finally/YOLOv8_Finally/YOLOv8_Finally/dataset_org/"
image_original_path = cur_path + "images/"
label_original_path = cur_path + "labels/"
image_format = '.jpg'  # 样本照片的格式后缀 .jpg .png .bmp等等

# 标签拆分比例
train_percent = 0.8
val_percent = 0.1
test_percent = 0.1

# 训练集路径
train_image_path = os.path.join(cur_path, "datasets/train/images/")
train_label_path = os.path.join(cur_path, "datasets/train/labels/")

# 验证集路径
val_image_path = os.path.join(cur_path, "datasets/val/images/")
val_label_path = os.path.join(cur_path, "datasets/val/labels/")

# 测试集路径
test_image_path = os.path.join(cur_path, "datasets/test/images/")
test_label_path = os.path.join(cur_path, "datasets/test/labels/")

# 训练集目录
list_train = os.path.join(cur_path, "datasets/train.txt")
list_val = os.path.join(cur_path, "datasets/val.txt")
list_test = os.path.join(cur_path, "datasets/test.txt")


def del_file(path):
    for i in os.listdir(path):
        file_data = path + "\\" + i
        os.remove(file_data)


def mkdir():
    if not os.path.exists(train_image_path):
        os.makedirs(train_image_path)
    else:
        del_file(train_image_path)
    if not os.path.exists(train_label_path):
        os.makedirs(train_label_path)
    else:
        del_file(train_label_path)

    if not os.path.exists(val_image_path):
        os.makedirs(val_image_path)
    else:
        del_file(val_image_path)
    if not os.path.exists(val_label_path):
        os.makedirs(val_label_path)
    else:
        del_file(val_label_path)

    if not os.path.exists(test_image_path):
        os.makedirs(test_image_path)
    else:
        del_file(test_image_path)
    if not os.path.exists(test_label_path):
        os.makedirs(test_label_path)
    else:
        del_file(test_label_path)


def clearfile():
    if os.path.exists(list_train):
        os.remove(list_train)
    if os.path.exists(list_val):
        os.remove(list_val)
    if os.path.exists(list_test):
        os.remove(list_test)


def get_main_class(label_path):
    """
    读取YOLO格式标签文件，返回出现频率最高的类别ID
    如果标签为空或出错，返回-1
    """
    try:
        with open(label_path, 'r') as f:
            lines = f.readlines()
            if not lines:
                return -1

            # 统计每个类别出现的次数
            class_counts = collections.Counter()
            for line in lines:
                parts = line.strip().split()
                if len(parts) >= 5:  # YOLO格式: class x y w h
                    class_id = int(parts[0])
                    class_counts[class_id] += 1

            # 返回出现频率最高的类别ID
            return class_counts.most_common(1)[0][0]
    except:
        return -1


def main():
    mkdir()
    clearfile()

    file_train = open(list_train, 'w')
    file_val = open(list_val, 'w')
    file_test = open(list_test, 'w')

    total_txt = os.listdir(label_original_path)

    # 按类别分组
    class_images = collections.defaultdict(list)

    print("正在分析标签文件中的类别信息...")
    for i, txt_name in enumerate(total_txt):
        name = txt_name[:-4]
        label_path = os.path.join(label_original_path, txt_name)

        # 获取图片的主要类别
        main_class = get_main_class(label_path)
        if main_class >= 0:  # 有效的类别ID
            class_images[main_class].append((i, name))

    # 打印每个类别的图片数量
    print("数据集类别分布情况:")
    for class_id, images in class_images.items():
        print(f"类别 {class_id}: {len(images)} 张图片")

    # 按类别进行分层抽样
    train_indices = []
    val_indices = []
    test_indices = []

    # 创建计数器跟踪每个集合中各类别的图片数量
    train_class_counts = collections.Counter()
    val_class_counts = collections.Counter()
    test_class_counts = collections.Counter()

    for class_id, images in class_images.items():
        num_images = len(images)
        indices = list(range(num_images))
        random.shuffle(indices)

        num_train = int(num_images * train_percent)
        num_val = int(num_images * val_percent)

        # 为每个类别分配训练/验证/测试集索引
        train_idx = indices[:num_train]
        val_idx = indices[num_train:num_train + num_val]
        test_idx = indices[num_train + num_val:]

        # 更新每个集合中各类别的计数
        train_class_counts[class_id] = len(train_idx)
        val_class_counts[class_id] = len(val_idx)
        test_class_counts[class_id] = len(test_idx)

        # 将索引转换为原始图片索引
        train_indices.extend([images[idx][0] for idx in train_idx])
        val_indices.extend([images[idx][0] for idx in val_idx])
        test_indices.extend([images[idx][0] for idx in test_idx])

    print(f"\n训练集总数：{len(train_indices)}, 验证集总数：{len(val_indices)}, 测试集总数：{len(test_indices)}")

    # 打印每个数据集中各类别的分布情况
    print("\n训练集类别分布:")
    for class_id, count in sorted(train_class_counts.items()):
        print(f"类别 {class_id}: {count} 张图片")

    print("\n验证集类别分布:")
    for class_id, count in sorted(val_class_counts.items()):
        print(f"类别 {class_id}: {count} 张图片")

    print("\n测试集类别分布:")
    for class_id, count in sorted(test_class_counts.items()):
        print(f"类别 {class_id}: {count} 张图片")

    # 处理每个图片
    for i, txt_name in enumerate(total_txt):
        name = txt_name[:-4]

        srcImage = image_original_path + name + image_format
        srcLabel = label_original_path + name + ".txt"

        if i in train_indices:
            dst_train_Image = train_image_path + name + image_format
            dst_train_Label = train_label_path + name + '.txt'
            shutil.copyfile(srcImage, dst_train_Image)
            shutil.copyfile(srcLabel, dst_train_Label)
            file_train.write(dst_train_Image + '\n')
        elif i in val_indices:
            dst_val_Image = val_image_path + name + image_format
            dst_val_Label = val_label_path + name + '.txt'
            shutil.copyfile(srcImage, dst_val_Image)
            shutil.copyfile(srcLabel, dst_val_Label)
            file_val.write(dst_val_Image + '\n')
        elif i in test_indices:
            dst_test_Image = test_image_path + name + image_format
            dst_test_Label = test_label_path + name + '.txt'
            shutil.copyfile(srcImage, dst_test_Image)
            shutil.copyfile(srcLabel, dst_test_Label)
            file_test.write(dst_test_Image + '\n')

    file_train.close()
    file_val.close()
    file_test.close()


if __name__ == "__main__":
    main()
