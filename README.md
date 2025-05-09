# e-pod-pi  
## web-interface  
This is where the actual stuff is  
*backups* holds backups of temperature measurements from the study.  
*static* is a folder where the current generated plot goes.  
*templates* holds the webpage html.  
### Explanation of the several html files  
*index_default.html* is an older version that includes automatic temperature control (set and forget, or something trying to be close to that)  
*index_humiditypm210TVOC.html* is the newest iteration of the purely manual page, adding humidity and air quality measurement  
*index.html* is the version used for the study, containing only manual control and temperature measurement  
*index1.html* is an older version of the page for the study and serves no purpose  
*index2.html* is similar to *index_default.html* but is missing manual fan and heater control  
### Why are there three different app.py versions?  
*app.py* was used for the study and contains the same features seen in *index.html*  
*app_backup.py* exists for some reason, but serves no purpose  
*app_humiditypm210TVOC.py* matches the html file with a similar name, adding those measurements  