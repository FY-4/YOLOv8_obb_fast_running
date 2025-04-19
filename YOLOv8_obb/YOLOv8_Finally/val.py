from ultralytics import YOLO
if __name__ == '__main__':
    model = YOLO('runs/detect/train5/weights/best.pt') 
    model.val(data='wheat.yaml',
              # split='val',
              source = "output.mp4",
              imgsz=648,
              batch=3,
              save_json=False, # if you need to cal coco metrice
              project='runs/val',
              name='exp',
              )