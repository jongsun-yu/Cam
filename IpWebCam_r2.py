# https://pcseob.tistory.com/25
# https://tydud.tistory.com/entry/python-openCV%EB%A1%9C-%EC%99%B8%EB%B6%80-IP-cam-%EC%98%81%EC%83%81-%EC%A0%9C%EC%96%B4onvif

import cv2
import datetime
import os


def writeVideo():
    #현재시간 가져오기
    currentTime = datetime.datetime.now()
    
    #RTSP를 불러오는 곳
    # video_capture = cv2.VideoCapture('rtsp://admin:admin@192.168.0.2:554')
    video_capture = cv2.VideoCapture('http://192.168.0.4:8080/video')
    

    # 웹캠 설정
    video_capture.set(3, 800)  # 영상 가로길이 설정
    video_capture.set(4, 600)  # 영상 세로길이 설정
    fps = 20
    # 가로 길이 가져오기
    streaming_window_width = int(video_capture.get(3))
    # 세로 길이 가져오기
    streaming_window_height = int(video_capture.get(4))  
    
    #현재 시간을 '년도 달 일 시간 분 초'로 가져와서 문자열로 생성
    fileName = str(currentTime.strftime('%Y %m %d %H %M %S'))

    # TODO: 관련 파일저장 위치 변경요망....
    #파일 저장하기 위한 변수 선언
    path = f'D:/cctv/cctv/python/{fileName}.avi'
    
    # DIVX 코덱 적용 # 코덱 종류 # DIVX, XVID, MJPG, X264, WMV1, WMV2
    # 무료 라이선스의 이점이 있는 XVID를 사용
    fourcc = cv2.VideoWriter_fourcc('X', 'V', 'I', 'D')
    
    # 비디오 저장
    # cv2.VideoWriter(저장 위치, 코덱, 프레임, (가로, 세로))
    out = cv2.VideoWriter(path, fourcc, fps, (streaming_window_width, streaming_window_height))

    while True:
        ret, frame = video_capture.read()
        # 촬영되는 영상보여준다. 프로그램 상태바 이름은 'streaming video' 로 뜬다.
        cv2.imshow('streaming video', frame)
        
        # 영상을 저장한다.
        out.write(frame)
        
        # 1ms뒤에 뒤에 코드 실행해준다.
        k = cv2.waitKey(1) & 0xff
        #키보드 esc 누르면 종료된다.
        if k == 27:
            break
    video_capture.release()  # cap 객체 해제
    out.release()  # out 객체 해제
    cv2.destroyAllWindows()

if __name__ == "__main__":
    writeVideo()