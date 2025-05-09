from flask import Flask, render_template, redirect, url_for, request
import subprocess
import threading
import signal

app = Flask(__name__)

data_collection_process = None
def run_data_collection():
    global data_collection_process
    data_collection_process = subprocess.Popen(['python3', 'opt-Read_Temp_Multiple.py'])

temp_set_process = None
temperature_goal = 25.0
chicken_on = False
def run_temp_set():
    global temp_set_process
    global temperature_goal
    global chicken_on
    print("From run_temp_set: "+str(temperature_goal)+str(chicken_on))
    temp_set_process = subprocess.Popen(['python3', 'Temp_Control.py', str(temperature_goal), str(int(chicken_on))])

temp_set_collection_process = None
def run_temp_set_collection():
    global temp_set_collection_process
    global temperature_goal
    global chicken_on
    temp_set_collection_process = subprocess.Popen(['python3', 'Temp_Control_and_Collection.py', str(temperature_goal), str(int(chicken_on))])

@app.route('/')
def index():
    return render_template('index.html', data_collection_running=data_collection_process is not None, temp_set_running=temp_set_process is not None, temp_set_collection_running=temp_set_collection_process is not None)

@app.route('/start')
def start_data_collection():
    global data_collection_process
    global temp_set_process
    global chicken_on
    if temp_set_process:
        temp_set_process.send_signal(signal.SIGINT)
        temp_set_process = None
        chicken_on = False
        threading.Thread(target=run_temp_set_collection).start()
    elif data_collection_process is None and temp_set_collection_process is None:
        threading.Thread(target=run_data_collection).start()
    return redirect(url_for('index'))

@app.route('/stop')
def stop_data_collection():
    global data_collection_process
    global temp_set_collection_process
    if temp_set_collection_process:
        temp_set_collection_process.send_signal(signal.SIGINT)
        temp_set_collection_process = None
        chicken_on = False
        threading.Thread(target=run_temp_set).start()
    elif data_collection_process:
        data_collection_process.terminate()
        data_collection_process = None
    return redirect(url_for('index'))

@app.route('/start_temp', methods=['GET','POST'])
def start_temp_set():
    global temp_set_process
    global data_collection_process
    global chicken_on
    global temperature_goal
    if data_collection_process:
        data_collection_process.terminate()
        data_collection_process = None
        if request.form.get('heater-state'):
            print("check!")
            chicken_on = True
        else:
            print("neck!")
            chicken_on = False
        temperature_goal = request.form.get('temp-goal')
        threading.Thread(target=run_temp_set_collection).start()
    elif temp_set_process is None and temp_set_collection_process is None:
        if request.form.get('heater-state'):
            print("check!")
            chicken_on = True
        else:
            print("neck!")
            chicken_on = False
        print(request.form.get('temp-goal'))
        temperature_goal = request.form.get('temp-goal')
        threading.Thread(target=run_temp_set).start()
    return redirect(url_for('index'))

@app.route('/stop_temp')
def stop_temp_set():
    global temp_set_process
    global temp_set_collection_process
    if temp_set_collection_process:
        temp_set_collection_process.send_signal(signal.SIGINT)
        temp_set_collection_process = None
        chicken_on = False
        threading.Thread(target=run_data_collection).start()
    elif temp_set_process:
        temp_set_process.send_signal(signal.SIGINT)
        temp_set_process = None
    return redirect(url_for('index'))

@app.route('/start_temp_data', methods=['GET','POST'])
def start_temp_set_collection():
    global temp_set_collection_process
    global chicken_on
    if temp_set_collection_process is None:
        if request.form.get('heater-state'):
            print("check!")
            chicken_on = True
        else:
            print("neck!")
            chicken_on = False
        temperature_goal = request.form.get('temp-goal')
        threading.Thread(target=run_temp_set_collection).start()
    return redirect(url_for('index'))

@app.route('/stop_temp_data')
def stop_temp_set_collection():
    global temp_set_collection_process
    if temp_set_collection_process:
        temp_set_collection_process.send_signal(signal.SIGINT)
        temp_set_collection_process = None
    return redirect(url_for('index'))

@app.route('/stop_all')
def stop_all_processes():
    global data_collection_process
    if data_collection_process:
        data_collection_process.terminate()
        data_collection_process = None
    global temp_set_process
    if temp_set_process:
        temp_set_process.send_signal(signal.SIGINT)
        temp_set_process = None
    global temp_set_collection_process
    if temp_set_collection_process:
        temp_set_collection_process.send_signal(signal.SIGINT)
        temp_set_collection_process = None
    return redirect(url_for('index'))

@app.route('/plot')
def plot_data():
    import pandas as pd
    import matplotlib
    matplotlib.use('Agg')
    from matplotlib import pyplot as plt

    data = pd.read_csv('temp_data_multiple.csv')
    data.plot(x="Time")
    plt.title('Temperature Data')
    plt.savefig('static/plot.png')
    plt.close()

    return redirect('static/plot.png')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80) # needs sudo / admin permission
    #app.run(host='0.0.0.0', port=5000)

'''
, methods=['POST']
print("not cool")
if request.form.get('match-with-pairs'):
    print("cool")

        <input type="checkbox" name="match-with-pairs">who am i</input>
    
'''
