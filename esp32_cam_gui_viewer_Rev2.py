# 참고 https://www.digikey.kr/ko/maker/projects/esp32-cam-python-stream-opencv-example/840608badd0f4a5eb21b1be25ecb42cb

import cv2
import tkinter as tk
from tkinter import Label, Button
from PIL import Image, ImageTk

# ESP32-CAM 스트리밍 주소
stream_url = 'http://192.168.0.6:81/stream'

# 비디오 캡처 객체 생성
video = cv2.VideoCapture(stream_url)

# 스트리밍 성공 여부 확인
if not video.isOpened():
    print("스트림을 열 수 없습니다.")
    exit()

# Tkinter 윈도우 생성
window = tk.Tk()
window.title("ESP32-CAM Viewer")

# 프레임을 표시할 라벨 생성
label = Label(window)
label.pack()

# 종료 플래그 설정
running = True

def update_frame():
    if running:
        ret, frame = video.read()
        if ret:
            # OpenCV 프레임을 PIL 이미지로 변환
            cv_img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(cv_img)
            imgtk = ImageTk.PhotoImage(image=img)
            
            # 라벨 업데이트
            label.imgtk = imgtk
            label.config(image=imgtk)
        
        # 10ms 후에 update_frame 함수 호출
        window.after(10, update_frame)

# 해상도 설정
video.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # 가로 해상도
video.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)  # 세로 해상도

# 프레임 업데이트 시작
update_frame()

def release_video():
    global running
    # 종료 플래그 설정
    running = False
    # 비디오 캡처 객체 해제
    video.release()
    cv2.destroyAllWindows()
    # Tkinter 창 종료
    window.destroy()

# 해제 버튼 추가
release_button = Button(window, text="해제", command=release_video)
release_button.pack()

# Tkinter 이벤트 루프 시작
window.mainloop()
