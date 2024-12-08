import cv2
import requests
import json
from hyperlpr import HyperLPR_plate_recognition
import time

# 读取配置文件
def load_camera_config(config_file):
    with open(config_file, 'r') as file:
        config = json.load(file)
    return config['cameras']


# 主函数
def main():
    # 加载摄像头配置
    cameras = load_camera_config('camera_config.json')
    
    # 循环处理每个摄像头
    for camera in cameras:
        camera_id = camera['id']
        camera_index = camera['index']
        
        # 创建视频捕获对象
        cap = cv2.VideoCapture(camera_index)
        
        if not cap.isOpened():
            print(f"无法打开摄像头 {camera_id}")
            continue
        
        while True:
            # 读取一帧
            ret, frame = cap.read()
            if not ret:
                break
            
            # 车牌识别
            result = HyperLPR_plate_recognition(frame)
            
            # 检查是否识别到车牌
            if result:
                license_plate = result[0].plate
            else:
                license_plate = ''
            
            # 发送HTTP请求
            url = f"https://api.xingbiao.com/chepai?id={camera_id}&chepai={license_plate}"
            response = requests.get(url)
            if response.status_code == 200:
                print(f"车牌信息已发送到服务器：{url}")
            else:
                print(f"发送失败：{response.text}")
        
        # 释放摄像头资源
        cap.release()
        time.sleep(5)  # 等待5秒后处理下一个摄像头

if __name__ == "__main__":
    main()