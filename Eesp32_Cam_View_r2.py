import cv2
import numpy as np
import requests
import time
import os

# 설정 변수
ESP32_URL = "http://192.168.0.6"  # ESP32-CAM의 IP 주소로 변경 (예: "http://http://192.168.0.7")
STREAM_URL = f"{ESP32_URL}:81/stream"  # 스트리밍 URL
HAARCASCADE_XML = "haarcascade_frontalface_alt.xml" # haarcascade 파일 이름
AWB = True  # 자동 화이트 밸런스 설정

# haarcascade 파일 경로 설정 (스크립트와 같은 폴더에 있는 경우)
HAARCASCADE_PATH = os.path.join(os.path.dirname(__file__), HAARCASCADE_XML)

# 얼굴 감지기 로드 (예외 처리 포함)
try:
    face_cascade = cv2.CascadeClassifier(HAARCASCADE_PATH)
    if face_cascade.empty():  # 파일 로드 실패 시 확인
        raise IOError(f"Could not load face cascade classifier at: {HAARCASCADE_PATH}")
except IOError as e:
    print(f"Error: {e}")
    exit()
except Exception as e:
    print(f"Error loading face cascade: {e}")
    exit()

# ESP32-CAM 제어 함수 (해상도, 품질, AWB)
def set_esp32_control(var, val):
    try:
        requests.get(f"{ESP32_URL}/control?var={var}&val={val}", timeout=1)
    except requests.exceptions.RequestException as e:
        print(f"Error setting {var}: {e}")

def set_resolution(index):
    resolutions = {  # 해상도 딕셔너리
        10: "UXGA(1600x1200)", 9: "SXGA(1280x1024)", 8: "XGA(1024x768)",
        7: "SVGA(800x600)", 6: "VGA(640x480)", 5: "CIF(400x296)",
        4: "QVGA(320x240)", 3: "HQVGA(240x176)", 0: "QQVGA(160x120)"
    }
    if index in resolutions:
        set_esp32_control("framesize", index)
        print(f"Resolution set to: {resolutions[index]}")
    else:
        print("Invalid resolution index.")

def set_quality(value):
    if 10 <= value <= 63:
        set_esp32_control("quality", value)
        print(f"Quality set to: {value}")
    else:
        print("Quality must be between 10 and 63.")

def toggle_awb():
    global AWB
    AWB = not AWB
    set_esp32_control("awb", 1 if AWB else 0)
    print(f"AWB toggled to: {AWB}")

# 메인 함수
if __name__ == "__main__":
    cap = cv2.VideoCapture(STREAM_URL)  # 비디오 캡처 객체 생성
    if not cap.isOpened():
        print(f"Error opening stream: {STREAM_URL}")
        exit()

    set_resolution(8)  # 기본 해상도 설정 (XGA)

    prev_frame_time = 0  # 이전 프레임 시간
    new_frame_time = 0  # 현재 프레임 시간

    while True:
        ret, frame = cap.read()  # 프레임 읽기
        if not ret:
            print("Error reading frame. Check stream or connection.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # 흑백 변환
        gray = cv2.equalizeHist(gray)  # 히스토그램 평활화 (대비 향상)

        # 얼굴 감지 (파라미터 조정 가능)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 0), 2)  # 얼굴 영역에 사각형 그리기

        # FPS 계산 및 표시
        new_frame_time = time.time()
        fps = 1 / (new_frame_time - prev_frame_time)
        prev_frame_time = new_frame_time
        fps = int(fps)
        fps = str(fps)
        cv2.putText(frame, "FPS: " + fps, (7, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (100, 255, 0), 2, cv2.LINE_AA)

        cv2.imshow("ESP32-CAM Face Detection", frame)  # 창 제목 변경

        key = cv2.waitKey(1)  # 키 입력 대기
        if key == ord('r'):  # 해상도 변경
            try:
                idx = int(input("Enter resolution index: "))
                set_resolution(idx)
            except ValueError:
                print("Invalid input. Please enter an integer.")
        elif key == ord('q'):  # 품질 변경
            try:
                val = int(input("Enter quality (10-63): "))
                set_quality(val)
            except ValueError:
                print("Invalid input. Please enter an integer.")
        elif key == ord('a'):  # AWB 토글
            toggle_awb()
        elif key == 27:  # ESC 키 종료
            break

    cap.release()
    cv2.destroyAllWindows()