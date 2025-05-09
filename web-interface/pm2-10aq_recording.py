import serial
import time
from datetime import datetime
import csv

ser = serial.Serial('/dev/ttyUSB0')

while True:
    data = []
    for i in range(0, 10):
        datum = ser.read()
        data.append(datum)
    pmtwofive = int.from_bytes(b''.join(data[2:4]), byteorder='little') / 10
    pmten = int.from_bytes(b''.join(data[4:6]), byteorder='little') / 10
    print(pmtwofive)
    print(pmten)
    with open('airquality_pm2-10.csv', 'a', newline='') as csvfile:
        csv.writer(csvfile).writerow([datetime.now().strftime("%H:%M:%S"),str(pmtwofive),str(pmten)])
    time.sleep(2)