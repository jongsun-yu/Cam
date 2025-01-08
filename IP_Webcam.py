# https://rahites.tistory.com/202

from urllib.request import urlopen
import cv2
import numpy as np
import time

url = "http://192.168.0.4:8080/video"

cam = cv2.VideoCapture(url)

# FHD로 녹화
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('ipWebCam.avi', fourcc, 30.0, (1920, 1080))

while True:
    check, img = cam.read()

    # 녹화 시작
    out.write(img)

    cv2.imshow('Camera', img)
    height, width, channels = img.shape
    if cv2.waitKey(1) == ord("q"):
        break

# 녹화 종료
cam.release()
out.release()
cv2.destroyAllWindows()