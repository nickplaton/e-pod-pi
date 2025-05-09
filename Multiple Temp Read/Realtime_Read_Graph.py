import os
import glob
import time
#import sys
#import csv
import matplotlib.pyplot as plt

x = []
y = []
plt.ion()
figure, ax = plt.subplots(figsize=(8, 6))
(line1,) = ax.plot(x, y)

plt.title("Realtime Temperature Data", fontsize=25)

plt.xlabel("Time", fontsize=18)
plt.ylabel("Temperature (C)", fontsize=18)

#loop_value = int(sys.argv[1])

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
loop_value = len(glob.glob(base_dir + '28*'))
device_folder = [None] * loop_value
device_file = [None] * loop_value
row_labels = [None] * loop_value #unrelated to these, but I don't wanna duplicate a for loop
for i in range(0, loop_value):
    device_folder[i] = glob.glob(base_dir + '28*')[i]
    device_file[i] = device_folder[i] + '/w1_slave'
    row_labels[i] = "Temp " + str(i)

def read_temp_raw(thermo):
    f = open(device_file[thermo], 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp(thermo):
    lines = read_temp_raw(thermo)
    '''while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw(thermo)'''
    try:
        equals_pos = lines[1].find('t=')
    except Exception as e:
        print(e)
        return 0.0
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c
    else:
        return 0.0

print(str(loop_value) + " thermometers detected.")

start_time = time.time()
last_time = start_time
'''with open('temp_data_multiple.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Time"] + row_labels)'''
temp_array = [0.0] * loop_value
while True:
    for i in range(0, loop_value):
        temp = read_temp(i)
        if temp != 0.0:
            temp_array[i] = temp
    print(temp_array)
    '''with open('temp_data_multiple.csv', 'a', newline='') as csvfile:
        csv.writer(csvfile).writerow([int(last_time-start_time)] + temp_array)'''
    print('row written')
    
    x.append(int(last_time-start_time))
    y.append(temp_array)
    
    line1.set_xdata(x)
    line1.set_ydata(y)

    figure.canvas.draw()

    figure.canvas.flush_events()
    
    time_dif = time.time()-last_time
    if time_dif <= float(loop_value):
        time.sleep(float(loop_value)-time_dif)
    last_time = time.time()
