from tkinter import *
from serial import *


##### WINDOW #########################################################
root = Tk()
root.title("Whiteboard Plotter")
menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
shapeMenu = Menu(menubar, tearoff=0)
helpmenu = Menu(menubar, tearoff=0)
############################################################

#### SERIAL SEND SETTINGS ##################################
serial_port = '/dev/ttyACM0'
baudRate = 9600
serial_send = Serial(serial_port, baudRate, timeout=0, writeTimeout=0)

############################################################

###### SERIAL SEND #########################################
def clickSend():
    global coordinates
    m_id = coordinates[0].get() 
    tempstring = coordinates[1].get() 
    send_string = "D" + m_id + "B" + tempstring
    entry_index = 2
    tempstring = coordinates[entry_index].get()
    
    while (tempstring and entry_index != len(coordinates)):
        send_string += " "
        send_string += tempstring
        entry_index += 1
        try:
            tempstring = coordinates[entry_index].get()
        except:
            break
    print(send_string)
    send_string += '\n'
    serial_send.write(str.encode(send_string))

############################################################
def close_top():
    global thetop
    thetop.destroy()
##### CLEAR SCREEN #########################################
def forget_frame(shape):

    if (shape=="600"):
        line()
    elif (shape=="601"):
        circle()
    elif (shape=="602"):
        square()
    elif (shape=="603"):
        triangle()
    elif (shape=="604"):
        xy()
############################################################

############## LINE ########################################  
def line(): 
    global coordinates
    global thetop
    thetop = Toplevel(root)
    tLine = Frame(thetop)
    tLine.option_add('*Font', '21')
    title = Label(tLine, relief=GROOVE, padx=10, text="PLOT LINE")
    back = Button(tLine, text="Back", pady=4, bd=2, highlightcolor='grey20', command=close_top)
    coordinates = []
    coordinates.append(Entry(tLine, width=5))
    coordinates.append(Entry(tLine, width=5))
    coordinates.append(Entry(tLine, width=5))
    coordinates.append(Entry(tLine, width=5))
    coordinates.append(Entry(tLine, width=5))
    coordinates.append(Entry(tLine, width=5))
    coordinates.append(Entry(tLine, width=5))
    coordinates.append(Entry(tLine, width=5))
    coordinates.append(Entry(tLine, width=5))
    button = Button(tLine, text="Send", padx=10, bd=2, highlightcolor='grey20', command=clickSend)

    l_id = Label(tLine, text=" mID:")
    l_x0 = Label(tLine, text=" x0:")
    l_y0 = Label(tLine, text=" y0:")
    l_x1 = Label(tLine, text=" x1:")
    l_y1 = Label(tLine, text=" y1:")

    back.place(x=4, y=0)
    title.pack(side=TOP)
    l_id.pack(side=LEFT)
    coordinates[0].pack(side=LEFT)
    l_x0.pack(side=LEFT)
    coordinates[1].pack(side=LEFT)
    coordinates[2].pack(side=LEFT)
    l_y0.pack(side=LEFT)
    coordinates[3].pack(side=LEFT)
    coordinates[4].pack(side=LEFT)
    l_x1.pack(side=LEFT)
    coordinates[5].pack(side=LEFT)
    coordinates[6].pack(side=LEFT)
    l_y1.pack(side=LEFT)
    coordinates[7].pack(side=LEFT)
    coordinates[8].pack(side=LEFT)
    button.pack(side=LEFT)
    tLine.pack()
    thetop.protocol("WM_DELETE_WINDOW", close_top)
    
#######################################################################################

############# CIRCLE ##################################################################
def circle():
    global coordinates
    global thetop
    
    thetop = Toplevel()
    tLine = Frame(thetop)
    tLine.option_add('*Font', '21')
    title = Label(tLine, relief=GROOVE, padx=10, text="PLOT CIRCLE")

    back = Button(tLine, text="Back", pady=4, bd=2, highlightcolor='grey20', command = close_top)
    coordinates = []                                                                  
    coordinates.append(Entry(tLine, width = 4 ))
    coordinates.append(Entry(tLine, width = 4 ))
    coordinates.append(Entry(tLine, width = 4 ))
    coordinates.append(Entry(tLine, width = 4 ))
    coordinates.append(Entry(tLine, width = 4 ))
    coordinates.append(Entry(tLine, width = 4 ))
    coordinates.append(Entry(tLine, width = 4 ))


    send_button = Button(tLine, text = "Send", command = clickSend) 

    c_id = Label(tLine, text=" mID:")
    rad_label = Label(tLine, text = " Radius:")
    x0_label = Label(tLine, text = " x0:")
    y0_label = Label(tLine, text = " y0:")

    back.place(x=4, y=0)
    title.pack(side=TOP)
    c_id.pack(side=LEFT)
    coordinates[0].pack(side=LEFT)
    rad_label.pack(side=LEFT)
    coordinates[1].pack(side=LEFT)   
    coordinates[2].pack(side=LEFT) 
    x0_label.pack(side=LEFT)
    coordinates[3].pack(side=LEFT)
    coordinates[4].pack(side=LEFT)
    y0_label.pack(side=LEFT)
    coordinates[5].pack(side=LEFT)
    coordinates[6].pack(side=LEFT)  

    send_button.pack(side=LEFT, padx=10)
    tLine.pack()
    thetop.protocol("WM_DELETE_WINDOW", close_top)
#######################################################################################

############## SQUARE #################################################################
def square():
    global coordinates 
    global thetop
    
    thetop = Toplevel()
    tLine = Frame(thetop)
    tLine.option_add('*Font', '21')
    title = Label(tLine, relief=GROOVE, padx=10, text="PLOT SQUARE")

    back = Button(tLine, text="Back", pady=4, bd=2, highlightcolor='grey20', command=close_top)
    coordinates = []                                                                     
    coordinates.append(Entry(tLine, width = 4 ))
    coordinates.append(Entry(tLine, width = 4 ))
    coordinates.append(Entry(tLine, width = 4 ))
    coordinates.append(Entry(tLine, width = 4 ))
    coordinates.append(Entry(tLine, width = 4 ))
    coordinates.append(Entry(tLine, width = 4 ))
    coordinates.append(Entry(tLine, width = 4 ))
    send_button = Button(tLine, text = "Send", command = clickSend)
    
    s_id = Label(tLine, text=" mID:")
    x0_label = Label(tLine, text = " x center:")
    y0_label = Label(tLine, text = " y center:")
    length_label = Label(tLine, text = " length:")

    back.place(x=4, y=0)
    title.pack(side=TOP)

    s_id.pack(side=LEFT)
    coordinates[0].pack(side=LEFT)

    x0_label.pack(side=LEFT)   
    coordinates[1].pack(side=LEFT)
    coordinates[2].pack(side=LEFT)
    y0_label.pack(side=LEFT)   
    coordinates[3].pack(side=LEFT)
    coordinates[4].pack(side=LEFT)

    length_label.pack(side=LEFT)     
    coordinates[5].pack(side=LEFT)   
    coordinates[6].pack(side=LEFT)

    send_button.pack(side=LEFT)
    tLine.pack()

    thetop.protocol("WM_DELETE_WINDOW", close_top)
#######################################################################################

######################### TRIANGLE ####################################################
def triangle():
    global coordinates
    global thetop
    
    thetop = Toplevel()
    tLine = Frame(thetop)
    tLine.option_add('*Font', '21')
    title = Label(tLine, relief=GROOVE, padx=10, text="PLOT TRIANGLE")

    back = Button(tLine, text="Back", pady=4, bd=2, highlightcolor='grey20', command=close_top)
    coordinates = []                                                                 
    coordinates.append(Entry(tLine, width = 4 ))
    coordinates.append(Entry(tLine, width = 4 ))
    coordinates.append(Entry(tLine, width = 4 ))
    coordinates.append(Entry(tLine, width = 4 ))
    coordinates.append(Entry(tLine, width = 4 ))
    coordinates.append(Entry(tLine, width = 4 ))
    coordinates.append(Entry(tLine, width = 4 ))
    send_button = Button(tLine, text = "Send", command = clickSend)

    tr_id = Label(tLine, text=" mID:")
    p1_label = Label(tLine, text = " point1:")
    p2_label = Label(tLine, text = " point2:")
    p3_label = Label(tLine, text = " point3:")

    back.place(x=4, y=0)
    title.pack(side=TOP)

    tr_id.pack(side=LEFT)
    coordinates[0].pack(side=LEFT)

    p1_label.pack(side=LEFT)   
    coordinates[1].pack(side=LEFT)
    coordinates[2].pack(side=LEFT)

    p2_label.pack(side=LEFT)     
    coordinates[3].pack(side=LEFT)
    coordinates[4].pack(side=LEFT)

    p3_label.pack(side=LEFT)     
    coordinates[5].pack(side=LEFT)
    coordinates[6].pack(side=LEFT)

    send_button.pack(side=LEFT)
    tLine.pack()
#######################################################################################

############ XY AXIS ##################################################################
def xy():
    global coordinates
    global thetop
    
    thetop = Toplevel()
    tLine = Frame(thetop)
    tLine.option_add('*Font', '21')
    title = Label(tLine, relief=GROOVE, padx=10, pady=2, text="PLOT XY-DIAGRAM")

    back = Button(tLine, text="Back", pady=4, bd=2, highlightcolor='grey20', command=close_top)
    coordinates = []
    coordinates.append(Entry(tLine, width = 4))
    coordinates.append(Entry(tLine, width = 4))
    coordinates.append(Entry(tLine, width = 4))
    coordinates.append(Entry(tLine, width = 4))
    coordinates.append(Entry(tLine, width = 4))

    send_button = Button(tLine, text = "Send", command = clickSend)

    xy_id = Label(tLine, text=" mID:")
    x_label = Label(tLine, text = " x:")
    y_label = Label(tLine, text = " y:")

    back.place(x=4, y=0)
    title.pack(side=TOP)

    xy_id.pack(side=LEFT)
    coordinates[0].pack(side=LEFT)

    x_label.pack(side=LEFT)
    coordinates[1].pack(side=LEFT)
    coordinates[2].pack(side=LEFT)

    y_label.pack(side=LEFT)
    coordinates[3].pack(side=LEFT)
    coordinates[4].pack(side=LEFT)

    send_button.pack(side=LEFT)
    tLine.pack()

    thetop.protocol("WM_DELETE_WINDOW", close_top)

#####################################################################################

############ SHAPE ##################################################################    
#shapeMenu = Menu(menubar, tearoff=0)
lineb = Button(root, text="Line", width=7, height=2, padx=10, pady=10, bd=2, command=line)
circb = Button(root, text="Circle", width=7, height=2, padx=10, pady=10, bd=2, command=circle)
sqb = Button(root, text="Square", width=7, height=2, padx=10, pady=10, bd=2, command=square)
trib = Button(root, text="Triangle", width=7, height=2, padx=10, pady=10, bd=2, command=triangle)
xyb = Button(root, text="xy-Axis", width=7, height=2, padx=10, pady=10, bd=2, command=xy)
lineb.pack(side=LEFT)
circb.pack(side=LEFT)
sqb.pack(side=LEFT)
trib.pack(side=LEFT)
xyb.pack(side=LEFT)
#shapeMenu.add_command(label = "Line", command=open_linetop)
#shapeMenu.add_command(label = "Circle", command = lambda : forget_frame("601"))
#shapeMenu.add_command(label = "Square", command = lambda : forget_frame("602"))
#shapeMenu.add_command(label = "Triangle", command = lambda : forget_frame("603"))
#shapeMenu.add_command(label = "XY-axis", command = lambda : forget_frame("604"))
#menubar.add_cascade(label = "Shapes", menu = shapeMenu)
#####################################################################################

########### HELP ####################################################################    
#helpmenu.add_command(label = "Help Index", command = donothing)
#helpmenu.add_command(label = "About...", command = donothing)
#menubar.add_cascade(label = "Help", menu = helpmenu)
#####################################################################################  

root.mainloop()

