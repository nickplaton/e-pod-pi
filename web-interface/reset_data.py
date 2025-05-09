import glob
import time
import csv
import subprocess

subprocess.run(['cp','temp_data_multiple.csv','backups/'+str(time.time())+'_temp_data_mutltiple.csv'])


base_dir = '/sys/bus/w1/devices/'
loop_value = len(glob.glob(base_dir + '28*'))
row_labels = [None] * loop_value
for i in range(0, loop_value):
    row_labels[i] = "Temp " + str(i)

print(str(loop_value) + " thermometers detected.")

with open('temp_data_multiple.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Time"] + row_labels)