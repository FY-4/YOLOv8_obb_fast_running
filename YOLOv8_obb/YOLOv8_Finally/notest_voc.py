import xml.etree.ElementTree as ET
import os

sets = ['train', 'val']  # 只保留训练集和验证集
classes = ['CYLJ', 'KHSLJ', 'QTLJ', 'YHLJ']

def convert(size, box):
    dw = 1. / size[0]
    dh = 1. / size[1]
    x = (box[0] + box[1]) / 2.0 - 1
    y = (box[2] + box[3]) / 2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return x, y, w, h

def convert_annotation(image_set, image_id):
    in_file = open(f'my_data_1/Annotations/{image_id}.xml', encoding='UTF-8')
    out_file = open(f'my_data_1/labels/{image_id}.txt', 'w')
    tree = ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)
    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult) == 1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text),
             float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
        bb = convert((w, h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')

for image_set in sets:
    if not os.path.exists('my_data_1/labels/'):
        os.makedirs('my_data_1/labels/')
    with open(f'my_data_1/ImageSets/{image_set}.txt') as f:
        image_ids = f.read().strip().split()
    list_file = open(f'my_data_1/{image_set}.txt', 'w')
    for image_id in image_ids:
        list_file.write(os.getcwd() + '/my_data_1/images/' + image_id + '.jpg\n')
        convert_annotation(image_set, image_id)
    list_file.close()