import cv2

# 定义保存视频的文件名和编码格式
output_file = "output.mp4"
fourcc = cv2.VideoWriter_fourcc(*'mp4v')

# 创建VideoWriter对象
out = cv2.VideoWriter(output_file, fourcc, 30.0, (640, 480))

cap = cv2.VideoCapture(0)

while True:
    # 捕获帧
    ret, frame = cap.read()
    if not ret:
        print("无法接收数据流")
        break

    # 写入当前帧
    out.write(frame)

    # 显示结果
    cv2.imshow('Recording...', frame)

    # 按q键退出
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 完成后释放一切
cap.release()
out.release()
cv2.destroyAllWindows()