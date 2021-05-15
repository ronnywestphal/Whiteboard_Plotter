from tkinter import *
from serial import *
from PIL import Image,ImageTk

##### Settings for reusable widgets ########################
class ButtonMain(Button):
    def __init__(self,parent=None, txt='', dim=[]):
        Button.__init__(self, parent)
        self['background'] = 'grey5'
        self['foreground'] = 'cyan3'
        self['activebackground'] = 'grey10'
        self['activeforeground'] = 'cyan2'
        self['highlightthickness'] = 0
        self['text'] = txt
        self['width'] = dim[0]
        self['height'] = dim[1]
        self['padx'] = dim[2]
        
class TitleMain(Label):
    def __init__(self,parent=None, txt=''):
        Label.__init__(self,parent)
        self['background'] = 'black'
        self['foreground'] = 'cyan3'
        self['highlightthickness'] = 0
        self['text'] = txt
        self['height']=1
        self['pady']=8  
class LabelBox(Label):
    def __init__(self,parent=None, txt=''):
        Label.__init__(self, parent)
        self['background'] = 'black'
        self['foreground'] = 'cyan3'
        self['text'] = txt
class InputBox(Entry):
    def __init__(self,parent=None):
        Entry.__init__(self,parent)
        self['background'] = 'grey5'
        self['foreground'] = 'cyan3'
        self['highlightbackground'] = 'cyan3'
        self['highlightthickness'] = 1
        self['width'] = 10
############################################################

##### WINDOW ###############################################
root = Tk()
root.title("Whiteboard Plotter")
root.option_add('*Font', '21')
root.configure(bg="black")
root.geometry("400x280")

#### BACKGROUND IMAGES #####################################
im = Image.open("linjer1.jpeg")
im2 = im.resize((400,350))
bimg = ImageTk.PhotoImage(im2)
myLabel = Label(root, image=bimg, bg="grey10")
myLabel.place(x=0,y=0)
# Wide Version #
bimg_tmp = Image.open("linjer1.jpeg")
bimg_tmp2 = bimg_tmp.resize((780,400))
bimg_re = ImageTk.PhotoImage(bimg_tmp2)
# MARIO IMAGE
img1 = Image.open("Super-Mario.jpg")
reimg = img1.resize((400,350))
mariPic = ImageTk.PhotoImage(reimg)

############################################################

#### SERIAL SEND SETTINGS ##################################
serial_port = '/dev/ttyACM0'
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
    print(str.encode(send_string))
    #serial_send.write(str.encode(send_string + '\n'))
    
############################################################

###### CLOSE WINDOW ########################################
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
            secondMenu(shape, 'Line Menu')
        elif (shape=='circle'):
            secondMenu(shape, 'Circle Menu')
        elif (shape=='square'):
            secondMenu(shape, 'Square Menu')
        else:                   # travel or mario = bring back root
            root.deiconify()       
        
# CLOSE SECOND MENU WINDOW # 
def close_top2(aShape,lib):   # (which shape, library/user input)
    global menu2
    menu2.destroy()
    
    if (aShape=='line'):
        if (lib):
            libLines()
        else: 
            line()
    elif (aShape=='circle'): 
        if(lib):
            libCircles()
        else: 
            circle()
    elif (aShape=='square'):
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
    library_top.geometry("400x280")

    myLabel = Label(library_top, image=bimg, bg='grey5')
    myLabel.place(x=0,y=0)
    title = TitleMain(library_top, 'Line Library')    
    title.pack(side=TOP)
    back = ButtonMain(library_top, 'Back', dimB) 
    back.config(command = lambda : close_top('library', 'line'))
    back.place(x=0, y=0)

    button_X = ButtonMain(library_top, 'Zero->X', dim)
    button_X.config(command=lambda : libSend_line("D601B0000 0000 01FF 0000\n"))
    button_Y = ButtonMain(library_top, 'Zero^Y', dim)
    button_Y.config(command=lambda : libSend_line("D601B0000 0000 0000 01FF\n"))
    button_Diag = ButtonMain(library_top, 'Zero_Diag', dim)
    button_Diag.config(command=lambda : libSend_line("D601B0000 0000 01FF 01FF\n"))

    button_X.place(x=5, y=60)
    button_Y.place(x=145, y=60)
    button_Diag.place(x=290, y=60)
    library_top.protocol("WM_DELETE_WINDOW", lambda : root.quit())

def libCircles():
    global library_top

    library_top = Toplevel(root)
    library_top.geometry("400x280")

    myLabel = Label(library_top, image=bimg, bg='grey5')
    myLabel.place(x=0,y=0)
    title = TitleMain(library_top, 'Circle Library')    
    title.pack(side=TOP)
    back = ButtonMain(library_top, 'Back', dimB) 
    back.config(command = lambda : close_top('library', 'circle'))
    back.place(x=0, y=0)

    # radius = 1
    b_r1_1_1 = ButtonMain(library_top, 'rad1_X1_Y1', dim)
    b_r1_1_1.config(command=lambda : libSend_circle("D602B00 64 00 64 00 64\n"))
    b_r1_2_2 = ButtonMain(library_top, 'rad1_X2_Y2', dim)
    b_r1_1_1.config(command=lambda : libSend_circle("D602B00 64 00 C8 00 C8\n"))
    b_r1_3_3 = ButtonMain(library_top, 'rad1_X3_Y3', dim)
    b_r1_3_3.config(command=lambda : libSend_circle("D602B00 64 01 00 01 00\n"))
    # radius = 2
    b_r2_1_1 = ButtonMain(library_top, 'rad2_X1_Y1', dim)
    b_r2_1_1.config(command=lambda : libSend_circle("D602B00 C8 00 64 00 64\n"))
    b_r2_2_2 = ButtonMain(library_top, 'rad2_X2_Y2', dim)
    b_r2_2_2.config(command=lambda : libSend_circle("D602B00 C8 00 C8 00 C8\n"))
    b_r2_3_3 = ButtonMain(library_top, 'rad2_X3_Y3', dim)
    b_r2_3_3.config(command=lambda : libSend_circle("D602B00 C8 01 00 01 00\n"))

    b_r1_1_1.place(x=5, y=60)
    b_r1_2_2.place(x=145, y=60)
    b_r1_3_3.place(x=290, y=60)
    b_r2_1_1.place(x=5, y=110)
    b_r2_2_2.place(x=145, y=110)
    b_r2_3_3.place(x=290, y=110)

    library_top.protocol("WM_DELETE_WINDOW", lambda : root.quit())

def libSquares():
    global library_top
    library_top = Toplevel(root)
    library_top.geometry("400x280")

    myLabel = Label(library_top, image=bimg, bg='grey5')
    myLabel.place(x=0,y=0)
    
    title = TitleMain(library_top, 'Square Library')
    title.pack(side=TOP)

    button_X = ButtonMain(library_top, 'rad1_X1_Y1', dim)
    button_X.config(command=lambda : libSend_square("D603B00 64 00 64 00 64\n"))
    button_Y = ButtonMain(library_top, 'rad1_X2_Y2', dim)
    button_Y.config(command=lambda : libSend_square("D603B00 64 00 C8 00 C8\n"))
    button_Diag = ButtonMain(library_top, 'rad1_X3_Y3', dim)
    button_Diag.config(command=lambda : libSend_square("D603B00 64 01 00 01 00\n"))
    
    back = ButtonMain(library_top, 'Back', dimB) 
    back.config(command = lambda : close_top('library', 'square'))
    back.place(x=0, y=0)

    button_X.place(x=5, y=60)
    button_Y.place(x=145, y=60)
    button_Diag.place(x=290, y=60)

    library_top.protocol("WM_DELETE_WINDOW", lambda : root.quit())

######################################################################################

##### SECOND MENUES ##################################################################
def secondMenu(aShape, header): # parameters decide which menu
    global menu2
    menu2 = Toplevel(root)
    menu2.geometry("400x280")
    
    myLabel = Label(menu2, image=bimg, bg='grey5')
    myLabel.place(x=0,y=0)
    title = TitleMain(menu2, header)
    title.pack(side=TOP)

    button_Lib = ButtonMain(menu2, 'Library', dim)
    button_Lib.config(command=lambda : close_top2(aShape, True))
    button_Lib.place(x=148,y=45)
    button_Input = ButtonMain(menu2, 'Input Values', dim)
    button_Input.config(command=lambda : close_top2(aShape, False))
    button_Input.place(x=148,y=90)
    back = ButtonMain(menu2, 'Back', dimB) 
    back.config(command = lambda : close_top('menu2', 'circle'))
    back.place(x=0, y=0)
  
    menu2.protocol("WM_DELETE_WINDOW", lambda : root.quit())
    
######################################################################################

############## LINE ##################################################################  
def line(): 
    global coordinates, input_top
    
    input_top = Toplevel(root)
    input_top.geometry("700x145")
    input_top.configure(bg='black')

    myLabel = Label(input_top, image=bimg_re, bg='black')
    myLabel.place(x=0,y=0)    
    title = TitleMain(input_top, 'PLOT LINE')
    title.pack(side=TOP)
   
    send_button = ButtonMain(input_top, 'Send', dimS)
    send_button.config(command = lambda : clickSend("601"))
    send_button.place(x=613, y=57)
    back = ButtonMain(input_top, 'Back', dimB) 
    back.config(command = lambda : close_top('top', 'circle'))
    back.place(x=0, y=0)

    coordinates = []
    coordinates.append(InputBox(input_top))
    coordinates.append(InputBox(input_top))
    coordinates.append(InputBox(input_top))    
    coordinates.append(InputBox(input_top))
    l_x0 = LabelBox(input_top, ' x0:')
    l_y0 = LabelBox(input_top, ' y0:')
    l_x1 = LabelBox(input_top, ' x1:')
    l_y1 = LabelBox(input_top, ' y1:')

    l_x0.place(x=5, y=60)
    coordinates[0].place(x=40, y=60)
    l_y0.place(x=155, y=60)
    coordinates[1].place(x=190, y=60)
    l_x1.place(x=305, y=60)
    coordinates[2].place(x=340, y=60)
    l_y1.place(x=455, y=60)
    coordinates[3].place(x=490, y=60)
   
    input_top.protocol("WM_DELETE_WINDOW", lambda : root.quit())
    
#######################################################################################

############# CIRCLE ##################################################################
def circle():
    global coordinates, input_top
    
    input_top = Toplevel()
    input_top.geometry("620x145")

    myLabel = Label(input_top, image=bimg_re, bg='grey5')
    myLabel.place(x=0,y=0)  
    title = TitleMain(input_top, 'PLOT CIRCLE')
    title.pack(side=TOP)

    coordinates = []   
    coordinates.append(InputBox(input_top))
    coordinates.append(InputBox(input_top))
    coordinates.append(InputBox(input_top))    

    rad_label = LabelBox(input_top, ' Radius:')
    x0_label = LabelBox(input_top, ' x0:')
    y0_label = LabelBox(input_top, ' y0:')

    send_button = ButtonMain(input_top, 'Send', dimS)
    send_button.config(command = lambda : clickSend("601"))
    send_button.place(x=503, y=57)
    back = ButtonMain(input_top, 'Back', dimB) 
    back.config(command = lambda : close_top('top', 'circle'))
    back.place(x=0, y=0)

    rad_label.place(x=5, y=60)
    coordinates[0].place(x=80, y=60)
    x0_label.place(x=195, y=60)   
    coordinates[1].place(x=230, y=60)
    y0_label.place(x=345, y=60)
    coordinates[2].place(x=380, y=60)

    input_top.protocol("WM_DELETE_WINDOW", lambda : root.quit())

########################################################################################

############## SQUARE ##################################################################
def square():
    global coordinates, input_top
    
    input_top = Toplevel()
    input_top.geometry("620x145")

    myLabel = Label(input_top, image=bimg_re, bg='grey5')
    myLabel.place(x=0,y=0)  
    title = TitleMain(input_top, 'PLOT SQUARE')
    title.pack(side=TOP)


    send_button = ButtonMain(input_top, 'Send', dimS)
    send_button.config(command = lambda : clickSend("602"))
    send_button.place(x=493, y=57)
    back = ButtonMain(input_top, 'Back', dimB) 
    back.config(command = lambda : close_top('top', 'square'))
    back.place(x=0, y=0)

    coordinates = [] 
    coordinates.append(InputBox(input_top))
    coordinates.append(InputBox(input_top))
    coordinates.append(InputBox(input_top))
    length_label = LabelBox(input_top, ' Length:')
    x0_label = LabelBox(input_top, ' x0:')
    y0_label = LabelBox(input_top, ' y0:')

    length_label.place(x=5, y=60)
    coordinates[0].place(x=75, y=60)
    x0_label.place(x=185, y=60)   
    coordinates[1].place(x=220, y=60)
    y0_label.place(x=335, y=60)
    coordinates[2].place(x=370, y=60)

    input_top.protocol("WM_DELETE_WINDOW", lambda : root.quit())

#########################################################################################

############## TRAVEL ###################################################################  
def travel(): 
    global coordinates, input_top
    root.withdraw()    
    input_top = Toplevel(root)
    input_top.geometry("700x145")

    myLabel = Label(input_top, image=bimg_re, bg='grey5')
    myLabel.place(x=0,y=0)    
    title = TitleMain(input_top, 'Travel')
    title.pack(side=TOP)

    send_button = ButtonMain(input_top, 'Send', dimS)
    send_button.config(command = lambda : clickSend("604"))
    send_button.place(x=613, y=57)
    back = ButtonMain(input_top, 'Back', dimB) 
    back.config(command = lambda : close_top('top', 'travel'))
    back.place(x=0, y=0)

    coordinates = []
    coordinates.append(InputBox(input_top))
    coordinates.append(InputBox(input_top))
    coordinates.append(InputBox(input_top))    
    coordinates.append(InputBox(input_top))
    l_x0 = LabelBox(input_top, ' x0:')
    l_y0 = LabelBox(input_top, ' y0:')
    l_x1 = LabelBox(input_top, ' x1:')
    l_y1 = LabelBox(input_top, ' y1:')

    l_x0.place(x=5, y=60)
    coordinates[0].place(x=40, y=60) 
    l_y0.place(x=155, y=60)
    coordinates[1].place(x=190, y=60)
    l_x1.place(x=305, y=60)
    coordinates[2].place(x=340, y=60)
    l_y1.place(x=455, y=60)
    coordinates[3].place(x=490, y=60)
   
    input_top.protocol("WM_DELETE_WINDOW", lambda : root.quit())

#########################################################################################

############## DRAW MARIO ###############################################################
def mario():
    global input_top
    root.withdraw()
    input_top = Toplevel(root)
    input_top.geometry("400x350")

    myLabel = Label(input_top, image=mariPic, bg='black')
    myLabel.place(x=0,y=0)

    back = Button(input_top, text='Back', width=5, fg='dodger blue', bg='blue4',
                    activebackground='blue4', activeforeground='deep sky blue',
                    highlightthickness=0, command=lambda: close_top('top', 'mario'))
    send = Button(input_top, text='Draw Mario!', height=1, bg='blue4', fg='dodger blue',
                    activebackground='blue4', activeforeground='deep sky blue',
                    highlightthickness=0, command=lambda : print(str.encode('D603B\n')))
    back.pack(side=LEFT, anchor=N)
    send.place(x=160, y=250)
    input_top.protocol("WM_DELETE_WINDOW", lambda : root.quit())

#########################################################################################
# Some special button dimensions    ##
global dim,dimS,dimB                ##
# [width,height,padx]               ##
dim = [7,1,15]     # Regular Button ## 
dimS = [7,1,0]     # Send Button    ##
dimB = [5,1,0]     # Back Button    ##
######################################

############ MAIN MENU ################################################################## 
mainTitle = TitleMain(root, 'Main Menu')
mainTitle.pack(side=TOP)

lineb = ButtonMain(root, 'Line', dim)
lineb.config(command=lambda : close_top('main', 'line'))
circb = ButtonMain(root, 'Circle',dim)
circb.config(command=lambda : close_top('main', 'circle'))
sqb = ButtonMain(root, 'Square',dim)
sqb.config(command=lambda : close_top('main', 'square'))
mariob = ButtonMain(root, 'Draw Mario',dim)
mariob.config(command=mario)
travelb = ButtonMain(root, 'Travel',dim)
travelb.config(command=travel)

lineb.place(x=148,y=45)
circb.place(x=148,y=90)
sqb.place(x=148,y=135)
mariob.place(x=148,y=180)
travelb.place(x=148,y=225)

#########################################################################################

root.mainloop()

