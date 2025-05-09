import subprocess
import glob
import time
import statistics
import sys
#import csv

#it doesn't seem like there is a way to control the precise temperature of the heaters
#we can regulate the temperature of the room by simply turning them on and off, assuming that they are at a higher temperature than the goal
#I feel it is a safe assumption since we can guarantee what the heater temperature is by simply never messing with actual temperature control

class PID:
    def __init__(self, goal, kp, ki, kd, max):
        self.goal = goal
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.max = max
        self.previous_error = 0
        self.integral = 0
    def get_output(self, measurement):
        error = self.goal - measurement
        self.integral = self.integral + error
        derivative = error - self.previous_error
        output = self.kp*error + self.ki*self.integral + self.kd*derivative
        output = max(output, -self.max)
        output = min(output, self.max)
        self.previous_error=error
        return output

state = False

subprocess.run(['modprobe', 'w1-gpio'])
subprocess.run(['modprobe', 'w1-therm'])

base_dir = '/sys/bus/w1/devices/'
loop_value = len(glob.glob(base_dir + '28*'))
device_folder = [None] * loop_value
device_file = [None] * loop_value
#row_labels = [None] * loop_value
for i in range(0, loop_value):
    device_folder[i] = glob.glob(base_dir + '28*')[i]
    device_file[i] = device_folder[i] + '/w1_slave'
    #row_labels[i] = "Temp " + str(i)

def read_temp_raw(thermo):
    f = open(device_file[thermo], 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp(thermo):
    lines = read_temp_raw(thermo)
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

def main():
    try:
        '''
        target = float(input("What is the target temperature? (Celsius)\n"))
        hq = input("Are the chicken coop heaters currently on? (y/n)\n")
        state = True if hq == 'y' else False
        '''
        target = float(sys.argv[1])
        state = bool(int(sys.argv[2]))
        print("Target is "+str(target)+" and state is "+str(state))

        control = PID(target, 0.5, 1.0, 0.0, 0.2)

        print(str(loop_value) + " thermometers detected.")

        start_time = time.time()
        last_time = start_time

        temp_array = [0.0] * loop_value
        while True:
            for i in range(0, loop_value):
                temp = read_temp(i)
                if temp != 0.0:
                    temp_array[i] = temp
            print(temp_array)
            temp_controller_output = control.get_output(statistics.fmean(temp_array))
            print(temp_controller_output)
            if (state and temp_controller_output <= 0.0) or (not state and temp_controller_output >= 0.0):
                subprocess.run(["irsend", "SEND_ONCE", "chicken", "pwr"])
                state = not state
            time_dif = time.time()-last_time
            if time_dif <= float(loop_value):
                time.sleep(float(loop_value)-time_dif)
            last_time = time.time()

    finally:
        print("Exiting.")
        if state:
            subprocess.run(["irsend", "SEND_ONCE", "chicken", "pwr"])
            print("Turning off heaters.")

main()
