from mq import *
import sys, time, csv
from datetime import datetime

try:
    print("Press CTRL+C to abort.")
    
    mq = MQ();
    while True:
        perc = mq.MQPercentage()
        '''sys.stdout.write("\r")
        sys.stdout.write("\033[K")
        sys.stdout.write("LPG: %g ppm, CO: %g ppm, Smoke: %g ppm" % (perc["GAS_LPG"], perc["CO"], perc["SMOKE"]))
        sys.stdout.flush()'''
        with open('airquality_TVOC.csv', 'a', newline='') as csvfile:
            csv.writer(csvfile).writerow([datetime.now().strftime("%H:%M:%S.%f"),str(perc["GAS_LPG"]),str(perc["CO"]),str(perc["SMOKE"])])
        time.sleep(0.1)

except Exception as e:
    print(e)
    print("\nAbort by user")
