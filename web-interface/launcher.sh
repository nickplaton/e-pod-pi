#!/bin/sh
cd /
cd home/e-pod-pi/Desktop/web-interface
sudo /etc/init.d/apache2 stop
sudo python3 app.py
cd /
