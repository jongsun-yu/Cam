import machine
import time
import network
import camera

ssid = 'YourWiFiSSID'
password = 'YourWiFiPassword'

sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect(ssid, password)
while not sta_if.isconnected():
    machine.idle()

camera.init()
time.sleep(2)

camera.capture('/tmp/camera.jpg')



'''
import machine
import time
import network
import camera

# Wi-Fi 설정
ssid = 'YourWiFiSSID'
password = 'YourWiFiPassword'

sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect(ssid, password)
while not sta_if.isconnected():
    machine.idle()
print("Connected to Wi-Fi")

# 카메라 초기화 및 해상도 설정
camera.init()
camera.framesize(camera.FRAME_QVGA)  # QVGA (320x240) 해상도
# 다른 해상도를 설정하려면 아래와 같이 변경하세요:
# camera.FRAME_96X96, camera.FRAME_QQVGA, camera.FRAME_HQVGA, camera.FRAME_VGA, camera.FRAME_SVGA,
# camera.FRAME_XGA, camera.FRAME_HD, camera.FRAME_SXGA, camera.FRAME_UXGA

print("Camera initialized with resolution:", camera.FRAME_QVGA)
time.sleep(2)

# 이미지 촬영
camera.capture('/tmp/camera.jpg')
print("Image captured and saved to /tmp/camera.jpg")

# 카메라 종료
camera.deinit()
print("Camera deinitialized")



해상도 조절
ESP32-CAM의 해상도를 조절

해상도 옵션
camera.FRAME_96X96: 96x96
camera.FRAME_QQVGA: 160x120
camera.FRAME_QVGA: 320x240
camera.FRAME_VGA: 640x480
camera.FRAME_SVGA: 800x600
camera.FRAME_XGA: 1024x768
camera.FRAME_HD: 1280x720
camera.FRAME_SXGA: 1280x1024
camera.FRAME_UXGA: 1600x1200

'''