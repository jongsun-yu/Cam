# MicroPython 펌웨어를 플래시(flash)
# http://192.168.0.6:81/stream

import network
import socket
import camera
import time

# Wi-Fi 설정
ssid = 'iptime1004'
password = 'kiss1004'

sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect(ssid, password)
while not sta_if.isconnected():
    time.sleep(1)
print("Connected to WiFi")

# 카메라 초기화
camera.init()
print("Camera initialized")

# HTML 페이지
html = """<html>
<head>
    <title>ESP32-CAM</title>
</head>
<body>
    <h1>ESP32-CAM Live Stream</h1>
    <img src="stream.mjpg" width="640" height="480">
</body>
</html>
"""

# 스트리밍 함수
def stream_handler(client):
    client.send("HTTP/1.1 200 OK\r\nContent-Type: multipart/x-mixed-replace; boundary=frame\r\n\r\n")
    while True:
        frame = camera.capture()
        if not frame:
            break
        client.send("--frame\r\n")
        client.send("Content-Type: image/jpeg\r\n\r\n")
        client.send(frame)
        client.send("\r\n")
        time.sleep(0.1)

# 서버 설정
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('192.168.0.6', 81))
server_socket.listen(1)
print("Server started at 192.168.0.6:81")

while True:
    client, addr = server_socket.accept()
    print('Got connection from', addr)
    request = client.recv(1024)
    if b'GET /stream.mjpg' in request:
        stream_handler(client)
    else:
        client.send("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n")
        client.send(html)
    client.close()
