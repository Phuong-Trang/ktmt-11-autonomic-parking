import subprocess
import json


def detect_image(source_path):
    weights_path = "pretrain/yolov7.pt"
    command = f"python detect.py --weights {weights_path} --source {source_path}"
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output = process.communicate()

    with open('result_arr.txt', 'r') as f:
        result_str = f.read()  # đọc toàn bộ nội dung tệp vào biến result_str
        result = eval(result_str)  # chuyển đổi chuỗi thành mảng
    for item in result:
        if item in ['bicycle', 'car', 'motorcycle', 'truck']:
            print(item)


detect_image("test_images/test.jpeg")  # Với đầu vào là source ảnh
