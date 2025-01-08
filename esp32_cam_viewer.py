import cv2
import time

# ESP32-CAM 스트리밍 주소
# stream_url = 'http://192.168.0.6:81/stream'
stream_url = 'http://192.168.0.4:8080/video'

# 비디오 캡처 객체 생성
video = cv2.VideoCapture(stream_url)

# 스트리밍 성공 여부 확인
if not video.isOpened():
    print("스트림을 열 수 없습니다.")
    exit()

print("스트리밍 시작...")

while True:
    ret, frame = video.read()
    if not ret:
        print("프레임 읽기 실패")
        break
    
    # 프레임 표시
    cv2.imshow('ESP32-CAM Viewer', frame)
    
    # 'Esc' 키 또는 'q' 키를 누르면 종료
    key = cv2.waitKey(1) & 0xFF
    if key == 27 or key == ord('q'):
        break

# 비디오 캡처 객체 해제
video.release()
cv2.destroyAllWindows()
