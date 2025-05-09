import os
import glob
import time
#import pandas as pd
import csv

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'
#cel = 0.0
#far = 0.0

def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c, temp_f

#temp_list = pd.DataFrame(
#    {'Celsius': cel,
#     'Fahrenheit': far,
#    })

start_time = time.time()
last_time = start_time
while True:
    temp_array = read_temp()
    with open('temp_data.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([int(last_time-start_time), temp_array[0], temp_array[1]])
    #print(read_temp())
    #[cel, far] = read_temp()
    #print(cel, far)
    #s = pd.Series([cel, far], index = ['Celsius', 'Fahrenheit'])
    #temp_list.to_csv('temp_data.csv', mode='a', header=False, index=True)
    #print('row written')
    time_dif = time.time()-last_time
    if time_dif <= 1.0:
        time.sleep(1.0-time_dif)
    last_time = time.time()
