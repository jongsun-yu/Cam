설명
스크립트는 ESP32-CAM 스트림에서 프레임을 캡처하고, 각 프레임에 현재 시간을 오버레이하여 30초마다 이미지를 저장합니다.

코드가 하는 일은 다음과 같습니다:
  1. OpenCV (cv2.VideoCapture)를 사용하여 ESP32-CAM에서 비디오 스트림을 캡처합니다.
  2. 비디오 스트림이 성공적으로 열렸는지 확인하고, 열리지 않으면 오류 메시지를 출력합니다.
  3. 원하는 프레임 크기를 설정하고, 루프 내에서 프레임을 읽습니다.
  4. 각 프레임을 지정된 크기로 조정합니다.
  5. 각 프레임에 현재 시간을 타임스탬프로 오버레이합니다.
  6. 각 프레임을 이메일 주소(아마도 당신의 이메일 주소로 추정)로 타이틀이 있는 창에 표시합니다.
  7. 30초마다 프레임을 이미지 파일로 저장합니다.
  8. 'Esc' 키 또는 'q' 키를 사용하여 스크립트를 종료할 수 있습니다.


코드
import cv2
import time
import datetime

# ESP32-CAM 스트리밍 주소
stream_url = 'http://192.168.0.4:8080/video'
stream_url = 'http://192.168.0.6:81/stream'

# 비디오 캡처 객체 생성
video = cv2.VideoCapture(stream_url)

# 스트리밍 성공 여부 확인
if not video.isOpened():
    print("스트림을 열 수 없습니다.")
    exit()

print("스트리밍 시작...")

# 마지막 이미지 저장 시간을 기록하기 위한 변수
last_saved_time = time.time()

# 원하는 크기 설정 (예: 640x480)
desired_width  = 640
desired_height = 480

while True:
    ret, frame = video.read()
    if not ret:
        print("프레임 읽기 실패")
        break
    
    # 프레임 크기 조정
    resized_frame = cv2.resize(frame, (desired_width, desired_height))

    # 현재 시간 텍스트 추가
    timestamp = datetime.datetime.now().strftime('%Y.%m.%d %H:%M:%S')
    text_size = cv2.getTextSize(timestamp, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0]
    text_x = resized_frame.shape[1] - text_size[0] - 10  # 오른쪽 여백 10 픽셀
    text_y = resized_frame.shape[0] - 10  # 하단 여백 10 픽셀

    # 검은색 음영 텍스트
    cv2.putText(resized_frame, timestamp, (text_x + 2, text_y + 2), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)
    # 흰색 텍스트
    cv2.putText(resized_frame, timestamp, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
    
    # 프레임 표시
    cv2.imshow('jongsun.yu@gmail.com', resized_frame)
    
    # 현재 시간
    current_time = time.time()

    # 30초마다 이미지 저장
    if current_time - last_saved_time >= 30:
        # 현재 시간을 기반으로 파일 이름 생성
        timestamp_file = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'frame_{timestamp_file}.jpg'
        cv2.imwrite(filename, resized_frame)
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
