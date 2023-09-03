try:
    import usocket as socket
except:
    import socket

from dht import DHT11
from machine import Pin

dhtSensor = DHT11(Pin(8))
dhtSensor.measure()
temp = dhtSensor.temperature()

def w_server():
    html = "<HTML>Temp = " + temp + " °C</HTML>"
    print("T={:02d} °C".format(temp))
    return html

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

while True:
    conn, addr = s.accept()
    print("Incoming connection from: ", str(addr))
    request = conn.recv(1024)
    request = str(request)
    print("Content: ", request)
    response = w_server()
    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type: text/html\n')
    conn.send('Connection: close\n\n')
    conn.sendall(response)
    conn.close()
