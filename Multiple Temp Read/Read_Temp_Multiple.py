import os
import glob
import time
import sys
import csv

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
#device_folder1 = glob.glob(base_dir + '28*')[1]
#device_file1 = device_folder1 + '/w1_slave'
#cel = 0.0
#far = 0.0

def read_temp_raw():
    lines = [None] * loop_value
    for i in range(0, loop_value):
        f = open(device_file[i], 'r')
        lines[i] = f.readlines()
        f.close()
    return lines

def read_temp():
    lines = read_temp_raw()
    temp_c = [None] * loop_value
    for i in range(0, loop_value):
        while lines[i][0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines[i] = read_temp_raw[i]()
        equals_pos = lines[i][1].find('t=')
        if equals_pos != -1:
            temp_string = lines[i][1][equals_pos+2:]
            temp_c[i] = float(temp_string) / 1000.0
            #temp_f = temp_c * 9.0 / 5.0 + 32.0
    return temp_c

#temp_list = pd.DataFrame(
#    {'Celsius': cel,
#     'Fahrenheit': far,
#    })

print(str(loop_value) + " thermometers detected.")

start_time = time.time()
last_time = start_time
csvfile = open('temp_data_multiple.csv', 'w', newline='')
writer = csv.writer(csvfile)
writer.writerow(["Time"] + row_labels)
while True:
    temp_array = read_temp()
    writer.writerow([int(last_time-start_time)] + temp_array)
    #print(read_temp())
    #[cel, far] = read_temp()
    #print(cel, far)
    #s = pd.Series([cel, far], index = ['Celsius', 'Fahrenheit'])
    #temp_list.to_csv('temp_data.csv', mode='a', header=False, index=True)
    print('row written')
    #print(temp_array)
    #print(time.time()-start_time)
    time_dif = time.time()-last_time
    if time_dif <= float(loop_value):
        time.sleep(float(loop_value)-time_dif)
    last_time = time.time()
