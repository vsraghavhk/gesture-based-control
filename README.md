# Controlling UAV camera using gestures with Leap Motion Controller

This project was an extension to CSCE 635 AI Robotics with Dr. Robin Murphy at Texas A&M. 
Project developed by [Raghav Hari Krishna](https://github.com/vsraghavhk) and [Leslie Kim](), developed during Fall of 2020. 

The final report for this project which explains the prohject in detail, is available [here]. 

## Requirements
This project requires the following softwares and SDKs for the corresponding hardware. 

### [Leap Motion Controller](https://www.ultraleap.com/product/leap-motion-controller/): 
  - [Leap Motion SDK Version 3.2](https://developer.leapmotion.com/releases/leap-motion-orion-321)
  - [Python 2.7](https://www.python.org/download/releases/2.7/)
  
  The documentation to use the Leap Motion SDK with Python 2.7 can be found [here](https://developer-archive.leapmotion.com/documentation/python/index.html#). 

The Leap Motion SDK does not officially support Python 3 and above. But there are a few wrappers made by the community, but they do not tend to work. 
Let me know if you come across a working one. 
  
### [Parrot Anafi Thermal drone](https://www.parrot.com/us/drones/anafi-thermal)
  - [PyParrot API](https://github.com/amymcgovern/pyparrot) by [amymcgovern](https://github.com/amymcgovern)
  - [Python 3.9](https://www.python.org/downloads/release/python-390/)
  

## Installation

Install the two python versions (2.7 and 3.9). 

It is suggested to create two [virtual environments](https://docs.python.org/3/tutorial/venv.html) for the 2 python versions. 

To run the leap motion controller code
  - Make sure the Leap Motion Controller control panel shows the LMC as connected. 
  - In the Leap Motion Control Panel go to General tab, and uncheck both "robust mdoe tracking" and "Auto-orient tracking". 
  - The code in the leap folder is to obtain the gestures using the leap motion controller. 
  - Install leap-requirements.txt in the leap folder within the Python 2.7 environment.
  - The leap folder has all the code and the relevant SDK files needed to run the code which handles the gestures. 
  - The read_gesture.py in the leap folder is the program to run within the python 2.7 environment.
  
The read_gesture_extended.py is the same code as read_gesture.py but has more comments and extra bits of code which can be used to add more gestures or implement different gestures. 


To run the parrot drone code:
  - The code in the pyparrot folder is to send commands to the drone based on the gesture inputs from LMC. 
  - Install drone-requirements.txt in the pyparrot folder with Python 3.9.
  - The PyParrot folder has all the SDK files form the PyParrot API necessary to run the code for the drone control. 
  - The Anafi-gesture.py in the pyparrot folder is the program to run within the python 3.9 environement. 

Before running this program, open the anafi-gesture.py in an editor and check the debug_mode parameter. If this is set to true, the program does not actually connect to anything but instead simply prints the commands recieved from the read_gesture.py program. If set to False, it will attempt to connect to the Parrot Anafi drone and send the commands to it. 


#### Both the read_gesture.py and Anafi-gesture.py must be run at the same time. 

### Possible Python 3 implementations of Leap Motion SDK (For the sake of posterity)
The LMC py3 support folder inside the leap folder has the Leap SDK files which should ideally work with python 3. It is from this [resource section of CSSE 120 class at Rose-Hulman Institute of Technology](https://www.rose-hulman.edu/class/cs/csse120/Resources/LeapMotion/)


Another option to try is [repo](https://github.com/brunodigiorgi/leapMotionController) by [brunodigiorgi](https://github.com/brunodigiorgi). 
