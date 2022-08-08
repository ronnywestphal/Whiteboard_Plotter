# Whiteboard Plotter
A plotter that is mounted on a whiteboard using magnets. It is capable of drawing shapes in different sizes.

This is a school project at the end of the first year in the Electrical Engineering program at KTH Royal Institute of Technology. 
The objective was to use a GD32VF103 RISC-V MCU and it's CAN2.0B interface to create a device that could complete a task. 

Components:
Two GD32VF103 RISC-V MCU's: One that controls the plotter and one that is used as a CAN-module.
Raspberry PI 4: For the GUI.

The GUI is written in Python's GUI package Tkinter. The user can select a shape and what size by manually entering the coordinates or by using the library. The coordinates are then sent to the CAN-module which allows the MCU on the plotter to receive the coordinates with it's CAN interface. The coordinates only consist of start/end/center/radius etc. to limit the amount of data sent to the plotter. So the functions that constructs the shapes are handled by the MCU on the plotter. 

The project on the plotter MCU is written in C using the PlatformIO development platform. 
