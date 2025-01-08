import cv2
import numpy as np
import requests
import time

URL = "http://192.168.0.6"  # ESP32-CAM URL로 변경
FACE_CASCADE_PATH = 'haarcascade_frontalface_alt.xml' # haarcascade 파일 경로를 명시적으로 지정
AWB = True

try:
    face_classifier = cv2.CascadeClassifier(FACE_CASCADE_PATH)
except Exception as e:
    print(f"Error loading face cascade: {e}")
    exit()

def set_control(url: str, var: str, val):
    try:
        requests.get(f"{url}/control?var={var}&val={val}", timeout=1)  # timeout 추가
    except requests.exceptions.RequestException as e:
        print(f"Error setting {var}: {e}")

def set_resolution(url: str, index: int):
    resolutions = {
        10: "UXGA(1600x1200)", 9: "SXGA(1280x1024)", 8: "XGA(1024x768)",
        7: "SVGA(800x600)", 6: "VGA(640x480)", 5: "CIF(400x296)",
        4: "QVGA(320x240)", 3: "HQVGA(240x176)", 0: "QQVGA(160x120)"
    }
    if index in resolutions:
        set_control(url, "framesize", index)
        print(f"Setting resolution to: {resolutions[index]}")
    else:
        print("Invalid resolution index.")

def set_quality(url: str, value: int):
    if 10 <= value <= 63:
        set_control(url, "quality", value)
        print(f"Setting quality to: {value}")
    else:
        print("Quality value must be between 10 and 63.")

def toggle_awb(url: str):
    global AWB
    AWB = not AWB
    set_control(url, "awb", 1 if AWB else 0)
    print(f"AWB toggled to: {AWB}")

if __name__ == '__main__':
    cap = cv2.VideoCapture(f"{URL}:81/stream")
    if not cap.isOpened():
        print(f"Error opening stream from {URL}:81/stream")
        exit()

    set_resolution(URL, 8) # 기본 해상도 설정

    prev_frame_time = 0
    new_frame_time = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error reading frame.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)

        faces = face_classifier.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5) # scaleFactor 및 minNeighbors 조정

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 0), 2) # 두께를 줄임

        new_frame_time = time.time()
        fps = 1/(new_frame_time-prev_frame_time)
        prev_frame_time = new_frame_time
        fps = int(fps)
        fps = str(fps)
        cv2.putText(frame, fps, (7, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (100, 255, 0), 3, cv2.LINE_AA) # FPS 표시

        cv2.imshow("frame", frame)

        key = cv2.waitKey(1)
        if key == ord('r'):
            try:
                idx = int(input("Select resolution index: "))
                set_resolution(URL, idx)
            except ValueError:
                print("Invalid input. Please enter an integer.")
        elif key == ord('q'):
            try:
                val = int(input("Set quality (10 - 63): "))
                set_quality(URL, val)
            except ValueError:
                print("Invalid input. Please enter an integer.")
        elif key == ord('a'):
            toggle_awb(URL)
        elif key == 27:
            break

    cap.release()
    cv2.destroyAllWindows()