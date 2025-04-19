import cv2
import os


def extract_frames(video_path, output_folder, frame_rate):
    # 确保输出文件夹存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 打开视频文件
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    frame_count = 1
    save_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # 每frame_rate帧保存一次图片
        if frame_count % frame_rate == 0:
            filename = os.path.join(output_folder, f"photo_{save_count:02d}.jpg")
            cv2.imwrite(filename, frame)
            print(f"Saved {filename}")
            save_count += 1

        frame_count += 1

    cap.release()
    print("Finished extracting frames.")


# 使用示例
video_path = '123321.mp4'  # 替换为你的视频路径
output_folder = './frames'  # 输出文件夹
frame_rate = 5  # 抽帧频率，每100帧抽取一帧
extract_frames(video_path, output_folder, frame_rate)