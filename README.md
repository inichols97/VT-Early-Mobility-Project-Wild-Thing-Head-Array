# VT-Early-Mobility-Project-Wild-Thing-Head-Array
Code needed to run the Head Array control system for the Vermont Early Mobility Project's Wild Thing

The code used in this project enables the raspberry pi to operate the sensors, process sensor input, and issue control commands to the motor controllers to let the user operate the wild thing. The code is broken into two files in the current working version: constants,py which stores all constants and optionally adjustable values, and app.py which is the main script that performs the above functions.

## constants.py
Although short, constants.py was added to the overall design more modular, which helps to make edits to adjustable values such as the default control set (labelled defaultControlSet) far easier for technicians, and potentially parents to make changes as needed. 

## app.py
The primary functionality of the Head Array is carried out by app.py which sets up all input and output GPIO pins connecting to the ultrasonic sensors, then the rf sensor. The control scheme is set based on the default control set set in constants.py or selected by the user. The control system waits for a signal from the rf received, if it is received then all function stops. If the restart signal comes next, then operation begins again, if the stop signal is entered again then function ends. While waiting for a signal from the kill switch, input comes from the ultrasonic sensors. This input is processed, and depending on what direction the user inputs and what control set is actively running, the control unit sends commands to the motor controllers.
