import cv2
import os

# 创建一个用于保存图片的目录，如果不存在的话
output_dir = 'zhibei8'
os.makedirs(output_dir, exist_ok=True)

# 打开摄像头
cap = cv2.VideoCapture(1)

if not cap.isOpened():
    print("无法打开摄像头！")
    exit()

photo_counter = 4511  # 初始化计数器
while True:
    # 捕获视频帧
    ret, frame = cap.read()
    if not ret:
        print("无法获取视频帧！")
        break

    # 显示视频帧
    cv2.imshow('Press Q to take a photo', frame)

    # 检测按键输入
    if cv2.waitKey(1) & 0xFF == ord('q'):
        # 格式化图片名称，例如：01.png, 02.png, ..., 100.png
        img_name = f"{output_dir}/photo_{photo_counter:02d}.jpg"

        # 保存图片
        cv2.imwrite(img_name, frame)
        print(f"图片已保存为 {img_name}")

        photo_counter += 1  # 增加计数器

        # 如果达到100张照片，则退出循环
        if photo_counter > 4530 :
            print("已拍摄30张照片，程序结束。")
            break

# 释放摄像头资源并关闭所有窗口
cap.release()
cv2.destroyAllWindows()