import urequests as requests
import ujson as json
from machine import Pin
import network

# WiFi 연결 설정
wifi_ssid = 'iptime1004'
wifi_password = 'kiss1004'

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(wifi_ssid, wifi_password)
    while not wlan.isconnected():
        pass
    print('WiFi connected:', wlan.ifconfig())

connect_wifi()

# IP 카메라 URL (카메라에 따라 URL 형식이 다를 수 있습니다)
# url = 'http://<아이피주소>:<포트>/video'
url = 'http://http://192.168.0.6/'

def get_camera_stream(url):
    response = requests.get(url)
    return response.content

while True:
    stream = get_camera_stream(url)
    # 스트림 데이터 처리 코드 추가
    # 예: 화면에 표시하거나 파일에 저장
