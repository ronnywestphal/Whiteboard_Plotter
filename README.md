# Whiteboard Plotter
A plotter that is mounted on a whiteboard using magnets. It is capable of drawing shapes in different sizes.

This is a school project at the end of the first year in the Electrical Engineering program at KTH Royal Institute of Technology. 
The course objective was to use a GD32VF103 RISC-V MCU and it's CAN2.0B interface to create a device that could complete a task. 

<p align="center">
 <img src="https://user-images.githubusercontent.com/84048902/184477814-aded21fe-4947-4625-af45-166133167624.png" width="450" height="350" />
</p>

## Hardware
- Two GD32VF103 with RISC-V   
- Raspberry PI 4
- Nema 17 RS PRO Hybrid Stepper Motors
- TOWER PRO SERVO MOTOR SG90

## GD32VF103 RISC-V | Main Project
The project is written in C using the PlatformIO development platform in Visual Studio Code. The MCU receives coordinates on it's CAN interface and stores them in a FIFO buffer where it can store a number of messages. Each CAN message contains all the necessary information for the plotter to draw one shape. 

## GD32VF103 RISC-V | USB to CAN Converter and Transceiver
This is necessary to receive the serial data from the Raspberry PI then transmit it as a CAN message to the transceiver so the plotter can receive the message on it's CAN interface. 

## Raspberry PI 4
The GUI is written in Python's GUI package Tkinter. The user can select a shape and what size by manually entering the ID of the shape along with the coordinates or by using the library. The ID and coordinates are stored in a byte string along with identifiers. 

## Drawing a line example: 
<p align="center">
  <img src="https://user-images.githubusercontent.com/84048902/184476230-2786d1f2-d88a-4804-bfd7-e4dad85331c7.png" width="600" />
</p>

User input = [1122, 3344, 5566, 7788] gets converted to b'D600B11 22 33 44 55 66 77 88\n' and sent via serial port 'ttyACM0'.

'D' indicates the start of the ID (600 = Line) and 'B' indicates the start of the coordinates (start and end of line).

The plotter reads the ID and proceeds to draw the line using the coordinates and Bresenham's Line Algorithm.






