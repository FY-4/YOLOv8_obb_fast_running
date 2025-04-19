import argparse
import cv2
from ultralytics import YOLO
import os

def main(args):
    # 加载模型
    model = YOLO(args.model_path)

    # 创建保存目录
    save_dir = 'runs/train/predict'
    os.makedirs(save_dir, exist_ok=True)
    output_video_path = os.path.join(save_dir, 'output_detected.mp4')

    # 读取视频
    cap = cv2.VideoCapture(args.source)

    # 获取视频属性
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    # 定义视频编码器
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (frame_width, frame_height))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # 进行推理
        results = model(frame)

        # 绘制结果
        annotated_frame = results[0].plot()

        # 写入输出视频
        out.write(annotated_frame)

    # 释放资源
    cap.release()
    out.release()
    cv2.destroyAllWindows()

    print(f"推理视频已保存到 {output_video_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="YOLOv8 Prediction Script")
    parser.add_argument('--model_path', type=str, default='runs/detect/train5/weights/best.pt', help='Path to the model file')
    parser.add_argument('--source', type=str, default='output.mp4', help='Source video path')
    parser.add_argument('--conf', type=float, default=0.25, help='Confidence threshold')
    parser.add_argument('--iou', type=float, default=0.45, help='IOU threshold')
    parser.add_argument('--imgsz', type=int, default=640, help='Image size')

    args = parser.parse_args()
    main(args)