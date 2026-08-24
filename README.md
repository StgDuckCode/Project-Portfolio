# Project-Portfolio
Portfolio of my work for job applications.

## Robot avoidance algorithm

The [robot_avoider.bash](https://github.com/StgDuckCode/Project-Portfolio/blob/main/Robot_avoidance/robot_avoider.bash) code is a robot avoidance algorithm I designed.  The robot can turn left or right or go forward. The robot decides based on scan data from sensors at different positions on the robot. The code has been verified in RViz simulation. This project was part of [TheconstructAI's](https://www.theconstruct.ai/) Linux Basics Real Robot Project. 

The "robot_interface.py" used to declare the parameters was designed by TheconstructAI, so I have not included it in the repo. The [robot_functions.bash](https://github.com/StgDuckCode/Project-Portfolio/blob/main/Robot_avoidance/robot_functions.bash), however, was designed by me and is used to define the functions.

## ESP-32 HomeAssistant-controlled kettle
Work in progress - see [Kettle Project](https://github.com/StgDuckCode/Kettle-Project) for details.

## 6DoF Robot Arm controller in Python
Project Aim: Investigate whether [LewanSoul Xarm1](https://xarm-lewansoul-ros.readthedocs.io/en/latest/index.html) can pick and place Petri dishes for inoculation during the minimum inhibitory concentration (MIC) process. Master's uni project.
Task of the code: read the joint trajectory from the robot simulation, output the trajectory, and then record the actual robot trajectory.

see [Video](https://youtube.com/shorts/f9CUZDWoMhA?feature=share) for results.

Uses source code for: 
- [HID communication](https://github.com/libusb/hidapi.git)
- [controller methods](https://github.com/adeguet1/lewansoul-xarm.git)
