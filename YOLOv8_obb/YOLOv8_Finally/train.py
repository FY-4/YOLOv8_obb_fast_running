from ultralytics import YOLO

model = YOLO("yolov8n.pt")

results = model.train(data="1.yaml", imgsz=640, epochs=200, batch= 16,device=0)#自己电脑上训练 加上workers=0