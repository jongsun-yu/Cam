import cv2
import time
import datetime

# ESP32-CAM 스트리밍 주소
stream_url = 'http://192.168.0.4:8080/video'

# 비디오 캡처 객체 생성
video = cv2.VideoCapture(stream_url)

# 스트리밍 성공 여부 확인
if not video.isOpened():
    print("스트림을 열 수 없습니다.")
    exit()

print("스트리밍 시작...")

# 마지막 이미지 저장 시간을 기록하기 위한 변수
last_saved_time = time.time()

while True:
    ret, frame = video.read()
    if not ret:
        print("프레임 읽기 실패")
        break
    
    # 현재 시간 텍스트 추가
    timestamp = datetime.datetime.now().strftime('%Y.%m.%d %H:%M:%S')
    text_size = cv2.getTextSize(timestamp, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0]
    text_x = (frame.shape[1] - text_size[0]) // 2
    text_y = frame.shape[0] - 10
    cv2.putText(frame, timestamp, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
    
    # 프레임 표시
    cv2.imshow('ESP32-CAM Viewer', frame)
    
    # 현재 시간
    current_time = time.time()

    # 30초마다 이미지 저장
    if current_time - last_saved_time >= 30:
        # 현재 시간을 기반으로 파일 이름 생성
        timestamp_file = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'frame_{timestamp_file}.jpg'
        cv2.imwrite(filename, frame)
        print(f'이미지 저장: {filename}')
        
        # 마지막 저장 시간 업데이트
        last_saved_time = current_time
    
    # 'Esc' 키 또는 'q' 키를 누르면 종료
    key = cv2.waitKey(1) & 0xFF
    if key == 27 or key == ord('q'):
        break

# 비디오 캡처 객체 해제
video.release()
cv2.destroyAllWindows()
