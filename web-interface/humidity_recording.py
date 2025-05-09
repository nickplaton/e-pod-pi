import time
import adafruit_dht
import board
import csv
from datetime import datetime

dht_device0 = adafruit_dht.DHT22(board.D17)
#dht_device1 = adafruit_dht.DHT22(board.D27)
while True:
    stime = time.time()
    try:
        print("Temperature: " + str(dht_device0.temperature) + ", Humidity: " + str(dht_device0.humidity))
        with open('humidity_data.csv', 'a', newline='') as csvfile:
            csv.writer(csvfile).writerow([datetime.now().strftime("%H:%M:%S"),str(dht_device0.humidity)])
    except Exception as e:
        print("Failed to read from Sensor 0: " + str(e))
    time.sleep(2.0-(time.time()-stime))
