# -*- coding: utf8 -*-
import cv2
import socket
import numpy as np
 
print("opencv-version:", cv2.__version__)
print("numpy-version:", np.__version__)

# TCP 사용
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server ip, port
s.connect(('172.19.23.166', 3000))

try:
    # webcam 이미지 capture
    cam = cv2.VideoCapture("/dev/video0")
    if not cam.isOpened():
        raise ValueError("카메라를 여는 데 실패했습니다. '/dev/video0' 경로를 확인하세요.")
except Exception as e:
    print("카메라 초기화 중 오류 발생:", e)
    exit(1)

# 이미지 속성 변경 3 = width, 4 = height
cam.set(3, 320)
cam.set(4, 240)

# 0~100에서 90의 이미지 품질로 설정 (default = 95)
encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

while True:
    # 비디오의 한 프레임씩 읽는다.
    ret, frame = cam.read()
    if not ret:
        print("프레임을 읽는 데 실패했습니다.")
        break

    try:
        # cv2.imencode(ext, img [, params])
        result, frame = cv2.imencode('.jpg', frame, encode_param)
        if not result:
            raise ValueError("이미지 인코딩 실패")
    except Exception as e:
        print("이미지 인코딩 중 오류 발생:", e)
        break

    # frame을 String 형태로 변환
    data = np.array(frame)
    stringData = data.tobytes()

    # 서버에 데이터 전송
    s.sendall(str(len(stringData)).encode().ljust(16) + stringData)

cam.release()
