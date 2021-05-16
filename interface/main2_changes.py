from tkinter import *
from serial import *

#Lagt till fler fönster med Toplevel()
#Huvudmenyn göms utan att stänga av programmet med .withdraw() sen .deiconify()
#Några exempel figurer hårdkodade
#Övriga menyer ligger i planet menu2 
#Alla librarysidor ligger i planet library_top
#Alla Entrysidor ligger i planet input_top
#Varje gång en ny sida öppnas töms föregående sida med metoden .destroy(), främst för att frigöra utrymmet då flera gränssnitt delar på planet, men även för att undvika att flera fönster är öppna samtidigt.
#command=lambda : funktion(parameter) används för att kunna skicka parametrar via tkinters funktioner.

##### WINDOW ###############################################
root = Tk()
root.title("Whiteboard Plotter")
root.option_add('*Font', '21')

############################################################

#### SERIAL SEND SETTINGS ##################################
serial_port = '/dev/ttyACM0'
#baudRate = 9600
#serial_send = Serial(serial_port, timeout=0, writeTimeout=0)

############################################################

###### SERIAL SEND #########################################
def clickSend(m_id):
    global coordinates 
    tempstring = coordinates[0].get() 
    send_string = "D" + m_id + "B" + tempstring
    entry_index = 1
    tempstring = coordinates[entry_index].get()
    
    while (tempstring and entry_index != len(coordinates)):
        send_string += " "
        send_string += tempstring
        entry_index += 1
        try:
            tempstring = coordinates[entry_index].get()
        except:
            break
    print(str.encode(send_string + '\n'))
    
    #serial_send.write(str.encode(send_string + '\n'))

###### CLOSE WINDOW #########################################
def close_top(top, shape):
    global root,input_top,library_top,menu2
    if (top=='main'):
        root.withdraw()
    elif (top=='top'):
        input_top.destroy()
    elif (top=='library'):
        library_top.destroy()
    else: 
        menu2.destroy()
        root.deiconify()
        
    if (top != 'menu2'):        
        if (shape=='line'):
            lineMenu()
        elif (shape=='circle'):
            circleMenu()
        elif (shape=='square'):
            squareMenu()
        else:
            root.deiconify()       
        
# CLOSE SECOND MENU WINDOW 
def close_top2(top,lib): # (which window, library/user input)
    global menu2
    menu2.destroy()
    
    if (top=='line'):
        if (lib):
            libLines()
        else: 
            line()
    elif (top=='circle'): 
        if(lib):
            libCircles()
        else: 
            circle()
    elif (top=='square'):
        if(lib): 
            libSquares()
        else: 
            square()
    
#############################################################

##### SEND STRING FROM LIBRARY ##############################
def libSend_line(send):
    print(str.encode(send))
    #serial_send.write(str.encode(send))
def libSend_circle(send):
    print(str.encode(" "))
def libSend_square(send):
    print(str.encode(" "))
#############################################################

##### LIBRARY MENUES ########################################
def libLines():
    global library_top
    
    library_top = Toplevel(root)
    mLine = Frame(library_top)
    title = Label(mLine, height=1, pady=4, text="Line Library")
    button_X = Button(mLine, text="zero-Xend", command=lambda : libSend_line("D600B00 00 00 00 0F FF 00 00\n"))
    button_Y = Button(mLine, text="zero-Yend", command=lambda : libSend_line("D600B00 00 00 00 00 00 0F FF\n"))
    button_Diag = Button(mLine, text="zero-diagonal", command=lambda : libSend_line("D600B00 00 00 00 0F FF 0F FF\n"))
    back = Button(mLine, text="Back", width=3, pady=1, bd=2, command=lambda : close_top('library', 'line'))

    back.place(x=0, y=0)
    title.pack(side=TOP)
    button_X.pack(side=LEFT)
    button_Y.pack(side=LEFT)
    button_Diag.pack(side=LEFT)
    mLine.pack()

def libCircles():
    global library_top

    library_top = Toplevel(root)
    mCircle = Frame(library_top)
    mCircle2 = Frame(library_top)
    title = Label(mCircle, height=1, pady=4, text="Circle Library")
    title.pack(side=TOP)
    # radius = 1
    b_r1_1_1 = Button(mCircle, text="rad1_X1_Y1", command=lambda : libSend_circle("D601B00 64 00 64 00 64\n"))
    b_r1_2_2 = Button(mCircle, text="rad1_X2_Y2", command=lambda : libSend_circle("D601B00 64 00 C8 00 C8\n"))
    b_r1_3_3 = Button(mCircle, text="rad1_X3_Y3", command=lambda : libSend_circle("D601B00 64 01 00 01 00\n"))
    # radius = 2
    b_r2_1_1 = Button(mCircle2, text="rad1_X1_Y1", command=lambda : libSend_circle("D601B00 C8 00 64 00 64\n"))
    b_r2_2_2 = Button(mCircle2, text="rad1_X2_Y2", command=lambda : libSend_circle("D601B00 C8 00 C8 00 C8\n"))
    b_r2_3_3 = Button(mCircle2, text="rad1_X3_Y3", command=lambda : libSend_circle("D601B00 C8 01 00 01 00\n"))
    
    back = Button(mCircle, text="Back", width=3, pady=1, bd=2, command=lambda : close_top('library', 'circle'))
    back.place(x=0, y=0)

    b_r1_1_1.pack(side=LEFT)
    b_r1_2_2.pack(side=LEFT)
    b_r1_3_3.pack(side=LEFT)
    b_r2_1_1.pack(side=LEFT)
    b_r2_2_2.pack(side=LEFT)
    b_r2_3_3.pack(side=LEFT)
    mCircle.pack()
    mCircle2.pack()

def libSquares():
    global library_top
    library_top = Toplevel(root)
    mSquare = Frame(library_top)
    title = Label(mSquare, height=1, pady=4, text="Square Library")
    button_X = Button(mSquare, text="zero-Xend", command=lambda : libSend_square("D600B00 00 00 00 0F FF 00 00\n"))
    button_Y = Button(mSquare, text="zero-Yend", command=lambda : libSend_square("D600B00 00 00 00 00 00 0F FF\n"))
    button_Diag = Button(mSquare, text="zero-diagonal", command=lambda : libSend_square("D600B00 00 00 00 0F FF 0F FF\n"))
    back = Button(mSquare, text="Back", width=3, pady=1, bd=2, command=lambda : close_top('library', 'square'))

    back.place(x=0, y=0)
    title.pack(side=TOP)
    button_X.pack(side=LEFT)
    button_Y.pack(side=LEFT)
    button_Diag.pack(side=LEFT)
    mSquare.pack()
def drawMario():
    print(str.encode('D603B\n'))
    #serial_send.write(str.encode("D603B \n"))
#############################################################

##### SHAPE MENUES ##########################################
def lineMenu():
    global menu2
    menu2 = Toplevel(root)
    mLine = Frame(menu2)
    title = Label(mLine, height=1, pady=4, text="Line Menu")
    button_Lib = Button(mLine, text="Library", width=10, height=2, bd=2, command=lambda : close_top2('line', True))
    button_Input = Button(mLine, text="Input Values", width=10, height=2, bd=2, command=lambda : close_top2('line', False))
    back = Button(mLine, text="Back", width=3, pady=1, command=lambda : close_top('menu2', 'line'))

    back.place(x=0, y=1)
    title.pack(side=TOP)
    button_Lib.pack(side=LEFT)
    button_Input.pack(side=LEFT)
    mLine.pack()
def circleMenu():
    global menu2
    menu2 = Toplevel(root)
    mCircle = Frame(menu2)
    title = Label(mCircle, height=1, pady=4, text="Circle Menu")
    button_Lib = Button(mCircle, text="Library", width=10, height=2, bd=2, command=lambda : close_top2('circle', True))
    button_Input = Button(mCircle, text="Input Values", width=10, height=2, bd=2, command=lambda : close_top2('circle', False))
    back = Button(mCircle, text="Back", width=3, pady=1, command=lambda : close_top('menu2', 'circle'))

    back.place(x=0, y=1)
    title.pack(side=TOP)
    button_Lib.pack(side=LEFT)
    button_Input.pack(side=LEFT)
    mCircle.pack()
def squareMenu():
    global menu2
    menu2 = Toplevel(root)
    mSquare = Frame(menu2)
    title = Label(mSquare, height=1, pady=4, text="Square Menu")
    button_Lib = Button(mSquare, text="Library", width=10, height=2, bd=2, command=lambda : close_top2('square', True)) 
    button_Input = Button(mSquare, text="Input Values", width=10, height=2, bd=2, command=lambda : close_top2('square', False))
    back = Button(mSquare, text="Back", width=3, pady=1, command=lambda : close_top('menu2', 'square'))

    back.place(x=0, y=1)
    title.pack(side=TOP)
    button_Lib.pack(side=LEFT)
    button_Input.pack(side=LEFT)
    mSquare.pack()

##############################################################

############## LINE ##########################################  
def line(): 
    global coordinates, input_top
    
    input_top = Toplevel(root)
    tLine = Frame(input_top)
    title = Label(tLine, text="PLOT LINE")
    back = Button(tLine, text="Back", pady=1, command=lambda : close_top('top', 'line'))
    coordinates = []
    coordinates.append(Entry(tLine, width=5))
    coordinates.append(Entry(tLine, width=5))
    coordinates.append(Entry(tLine, width=5))
    coordinates.append(Entry(tLine, width=5))
    coordinates.append(Entry(tLine, width=5))
    coordinates.append(Entry(tLine, width=5))
    coordinates.append(Entry(tLine, width=5))
    coordinates.append(Entry(tLine, width=5))
   
    send_button = Button(tLine, text="Send", padx=10, command= lambda : clickSend("600"))

    l_x0 = Label(tLine, text=" x0:")
    l_y0 = Label(tLine, text=" y0:")
    l_x1 = Label(tLine, text=" x1:")
    l_y1 = Label(tLine, text=" y1:")

    back.place(x=0, y=0)
    title.pack(side=TOP)
    l_x0.pack(side=LEFT)
    coordinates[0].pack(side=LEFT)
    coordinates[1].pack(side=LEFT)
    l_y0.pack(side=LEFT)
    coordinates[2].pack(side=LEFT)
    coordinates[3].pack(side=LEFT)
    l_x1.pack(side=LEFT)
    coordinates[4].pack(side=LEFT)
    coordinates[5].pack(side=LEFT)
    l_y1.pack(side=LEFT)
    coordinates[6].pack(side=LEFT)
    coordinates[7].pack(side=LEFT)
    send_button.pack(side=LEFT)
    tLine.pack()
    input_top.protocol("WM_DELETE_WINDOW", lambda : close_top('top', 'line'))
    
#######################################################################################

############# CIRCLE ##################################################################
def circle():
    global coordinates, input_top
    
    input_top = Toplevel()
    tCircle = Frame(input_top)
    title = Label(tCircle, text="PLOT CIRCLE")

    back = Button(tCircle, text="Back", pady=1, command = lambda : close_top('top', 'circle'))
    coordinates = []                                                                  
    coordinates.append(Entry(tCircle, width = 5 ))
    coordinates.append(Entry(tCircle, width = 5 ))
    coordinates.append(Entry(tCircle, width = 5 ))
    coordinates.append(Entry(tCircle, width = 5 ))
    coordinates.append(Entry(tCircle, width = 5 ))
    coordinates.append(Entry(tCircle, width = 5 ))
    coordinates.append(Entry(tCircle, width = 5 ))
    send_button = Button(tCircle, text = "Send", command = lambda : clickSend("601")) 

    rad_label = Label(tCircle, text = " Radius:")
    x0_label = Label(tCircle, text = " x0:")
    y0_label = Label(tCircle, text = " y0:")

    back.place(x=0, y=0)
    title.pack(side=TOP)
    rad_label.pack(side=LEFT)
    coordinates[0].pack(side=LEFT)
    coordinates[1].pack(side=LEFT) 
    x0_label.pack(side=LEFT)   
    coordinates[2].pack(side=LEFT)
    coordinates[3].pack(side=LEFT)
    y0_label.pack(side=LEFT)
    coordinates[4].pack(side=LEFT)
    coordinates[5].pack(side=LEFT)
      

    send_button.pack(side=LEFT, padx=10)
    tCircle.pack()
    input_top.protocol("WM_DELETE_WINDOW", lambda : close_top('top', 'circle'))
########################################################################################

############## SQUARE ##################################################################
def square():
    global coordinates, input_top
    
    input_top = Toplevel()
    tsquare = Frame(input_top)
    title = Label(tsquare, text="PLOT SQUARE")

    back = Button(tsquare, text="Back", pady=1, command=lambda : close_top('top', 'square'))
    coordinates = []                                                                     
    coordinates.append(Entry(tsquare, width = 5 ))
    coordinates.append(Entry(tsquare, width = 5 ))
    coordinates.append(Entry(tsquare, width = 5 ))
    coordinates.append(Entry(tsquare, width = 5 ))
    coordinates.append(Entry(tsquare, width = 5 ))
    coordinates.append(Entry(tsquare, width = 5 ))
    coordinates.append(Entry(tsquare, width = 5 ))
    send_button = Button(tsquare, text = "Send", command = lambda : clickSend("602"))
    
    s_id = Label(tsquare, text=" mID:")
    x0_label = Label(tsquare, text = " x center:")
    y0_label = Label(tsquare, text = " y center:")
    length_label = Label(tsquare, text = " length:")

    back.place(x=0, y=0)
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
    tsquare.pack()

    input_top.protocol("WM_DELETE_WINDOW", lambda : close_top('top', 'square'))
#########################################################################################

############## TRAVEL ###################################################################  
def travel(): 
    global coordinates, input_top
    root.withdraw()             # Hide main menu
    input_top = Toplevel(root)
    tLine = Frame(input_top)
    title = Label(tLine, text="TRAVEL")
    back = Button(tLine, text="Back", pady=1, command=lambda : close_top('top', 'travel'))
    coordinates = []
    coordinates.append(Entry(tLine, width=5))
    coordinates.append(Entry(tLine, width=5))
    coordinates.append(Entry(tLine, width=5))
    coordinates.append(Entry(tLine, width=5))
    coordinates.append(Entry(tLine, width=5))
    coordinates.append(Entry(tLine, width=5))
    coordinates.append(Entry(tLine, width=5))
    coordinates.append(Entry(tLine, width=5))
     
    send_button = Button(tLine, text="Send", padx=10, bd=2, command= lambda : clickSend("604"))   

    l_x0 = Label(tLine, text=" x0:")
    l_y0 = Label(tLine, text=" y0:")
    l_x1 = Label(tLine, text=" x1:")
    l_y1 = Label(tLine, text=" y1:")

    back.place(x=0, y=0)
    title.pack(side=TOP)
    l_x0.pack(side=LEFT)
    coordinates[0].pack(side=LEFT)
    coordinates[1].pack(side=LEFT)
    l_y0.pack(side=LEFT)
    coordinates[2].pack(side=LEFT)
    coordinates[3].pack(side=LEFT)
    l_x1.pack(side=LEFT)
    coordinates[4].pack(side=LEFT)
    coordinates[5].pack(side=LEFT)
    l_y1.pack(side=LEFT)
    coordinates[6].pack(side=LEFT)
    coordinates[7].pack(side=LEFT)
    send_button.pack(side=LEFT)

    tLine.pack()
    input_top.protocol("WM_DELETE_WINDOW", lambda : close_top('top', 'travel'))
#########################################################################################

############ MAIN MENU ################################################################## 
mainTitle = Label(root, text='Main Menu', height=1)
mainTitle.grid(row=0, columnspan=3, pady=5)
lineb = Button(root, text="Line", width=9, height=2, bd=2, command=lambda : close_top('main', 'line'))
circb = Button(root, text="Circle", width=9, height=2, bd=2, command=lambda : close_top('main', 'circle'))
sqb = Button(root, text="Square", width=9, height=2, bd=2, command=lambda : close_top('main', 'square'))
mariob = Button(root, text="Draw Mario", width=9, height=2, bd=2, command=drawMario)
travelb = Button(root, text="Travel", width=9, height=2, bd=2, command=travel)

lineb.grid(row=1, column=0)
circb.grid(row=1, column=1)
sqb.grid(row=1, column=2)
mariob.grid(row=2, column=0)
travelb.grid(row=2, column=1)
#########################################################################################
root.mainloop()

#arkivMenu = Menu(menubar, tearoff=0)
#arkivMenu.add_separator()
#arkivMenu.add_command(label = "Exit", command=root.quit)
#arkivMenu.add_command(label = "Circle", command = circleMenu)
#arkivMenu.add_command(label = "Square", command = lambda : forget_frame("602"))
#arkivMenu.add_command(label = "Triangle", command = lambda : forget_frame("603"))
#shapeMenu.add_command(label = "XY-axis", command = lambda : forget_frame("604"))
#menubar.add_cascade(label = "File", menu = arkivMenu)
#####################################################################################
#shapeMenu = Menu(menubar, tearoff=0)
#shapeMenu.add_command(label = "Line", command=lineMenu)
#shapeMenu.add_command(label = "Circle", command = circleMenu)
#shapeMenu.add_command(label = "Square", command = squareMenu)
#shapeMenu.add_separator()
#shapeMenu.add_command(label = "Mario", command = marioMenu)
#shapeMenu.add_command(label = "Travel", command = lambda : line("605"))
#shapeMenu.add_command(label = "XY-axis", command = lambda : forget_frame("604"))
#menubar.add_cascade(label = "Shapes", menu = shapeMenu)
#####################################################################################

########### HELP ####################################################################    
#helpmenu.add_command(label = "Help Index", command = donothing)
#helpmenu.add_command(label = "About...", command = donothing)
#menubar.add_cascade(label = "Help", menu = helpmenu)
#####################################################################################  
#root.config(menu = menubar)


