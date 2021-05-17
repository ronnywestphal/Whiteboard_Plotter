from tkinter import *
from serial import *
from PIL import Image,ImageTk
#Update:
#Allting typ dubbelt så stort.
#Mainrutan alltid i center.
#Ny funktion "toogle_state" sätter en ruta till 'normal' eller 'disabled'. Tillagd i flera widgets och i close_top2()
#command = lambda : ( f1(), f2() ) kan använda flera funktioner.
#Plotrutan i ny ruta över toppen av mainrutan samt att mainrutan blir 'disabled'.
#Plotrutan använder samma crop av bilden som mainrutan.
#Lagt till funktioner i klassen "ButtonMain" för att ändra aktiva och vanliga inställningar.


##### Settings for reusable widgets ########################
class ButtonMain(Button):
    def __init__(self,parent=None, txt='', dim=[]):
        Button.__init__(self, parent)
        self['background'] = 'grey5'
        self['foreground'] = 'cyan3'
        self['activebackground'] = 'grey6'
        self['activeforeground'] = 'cyan2'
        self['highlightthickness'] = 0
        self['text'] = txt
        self['width'] = dim[0]
        self['height'] = dim[1]
        self['padx'] = dim[2]
        self['pady'] = dim[3]

# Hover over buttons #
        self.bind("<Enter>", self.enter)
        self.bind("<Leave>", self.leave)

    def enter(self, e):
        self['background'] = 'grey6'
        self['foreground'] = 'cyan2'
    def leave(self, e):
        self['background'] = 'grey5'
        self['foreground'] = 'cyan3'
        
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

# Main Window dimensions and position center #
root_W = 800 
root_H = 560
root_left = int(root.winfo_screenwidth()/2 - root_W/2)
root_top = int(root.winfo_screenheight()/2 - root_H/2)
root.geometry("{}x{}+{}+{}".format(root_W, root_H, root_left, root_top))
# Plot Window height #
plot_H = 170

##### BACKGROUND IMAGES ####################################
im = Image.open("linjer1.jpeg")
im2 = im.resize((800,600))
bimg = ImageTk.PhotoImage(im2)
myLabel = Label(root, image=bimg, bg="grey10")
myLabel.place(x=0,y=0)
# Wide Version #
bimg_tmp = Image.open("linjer1.jpeg")
bimg_tmp2 = bimg_tmp.resize((1150,285))
bimg_re = ImageTk.PhotoImage(bimg_tmp2)
# MARIO IMAGE #
img1 = Image.open("Super-Mario.jpg")
reimg = img1.resize((800,600))
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
        root.geometry("{}x{}+{}+{}".format(root_W, root_H, root_left, root_top))
        
    if (top != 'menu2'):        
        if (shape=='line'):
            secondMenu(shape, 'Line Menu')
        elif (shape=='circle'):
            secondMenu(shape, 'Circle Menu')
        elif (shape=='square'):
            secondMenu(shape, 'Square Menu')
        else:                   # travel or mario = bring back root
            root.deiconify()
            root.geometry("{}x{}+{}+{}".format(root_W, root_H, root_left, root_top))       
        
# CLOSE SECOND MENU WINDOW # 
def close_top2(shape, lib):        # (which shape, library/user input)
    global menu2
    if (lib):
        menu2.destroy()
        if(shape=='line'):
            libLines()
        elif (shape=='circle'):
            libCircles()
        else:
            libSquares()
    else:
        toggle_state('disable', False)
        if(shape=='line'):
            line()
        elif (shape=='circle'):
            circle()
        else:
            square()


def toggle_state(state, root_win):
    if (root_win):    
        for child in root.winfo_children():
            try:
                child['state']=str(state)
            except:
                pass
    else:
        for child in menu2.winfo_children():
            try:
                child['state']=str(state)
            except:
                pass    
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
    library_top.geometry("{}x{}+{}+{}".format(root_W, root_H, root_left, root_top))

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

    button_X.place(x=309,y=90)
    button_Y.place(x=309,y=180)
    button_Diag.place(x=309,y=270)
    library_top.protocol("WM_DELETE_WINDOW", lambda : root.quit())

def libCircles():
    global library_top

    library_top = Toplevel(root)
    library_top.geometry("{}x{}+{}+{}".format(root_W, root_H, root_left, root_top))

    myLabel = Label(library_top, image=bimg, bg='grey5')
    myLabel.place(x=0,y=0)
    title = TitleMain(library_top, 'Circle Library')    
    title.pack(side=TOP)
    back = ButtonMain(library_top, 'Back', dimB) 
    back.config(command = lambda : close_top('library', 'circle'))
    back.place(x=0, y=0)

    # radius = 1
    b_r1_1_1 = ButtonMain(library_top, '1rad_1X_1Y', dim)
    b_r1_1_1.config(command=lambda : libSend_circle("D602B00 64 00 64 00 64\n"))
    b_r1_2_2 = ButtonMain(library_top, '1rad_2X_2Y', dim)
    b_r1_1_1.config(command=lambda : libSend_circle("D602B00 64 00 C8 00 C8\n"))
    b_r1_3_3 = ButtonMain(library_top, '1rad_3X_3Y', dim)
    b_r1_3_3.config(command=lambda : libSend_circle("D602B00 64 01 00 01 00\n"))
    # radius = 2
    b_r2_1_1 = ButtonMain(library_top, '1rad_1X_1Y', dim)
    b_r2_1_1.config(command=lambda : libSend_circle("D602B00 C8 00 64 00 64\n"))
    b_r2_2_2 = ButtonMain(library_top, '1rad_2X_2Y', dim)
    b_r2_2_2.config(command=lambda : libSend_circle("D602B00 C8 00 C8 00 C8\n"))
    b_r2_3_3 = ButtonMain(library_top, '1rad_3X_3Y', dim)
    b_r2_3_3.config(command=lambda : libSend_circle("D602B00 C8 01 00 01 00\n"))

    b_r1_1_1.place(x=200,y=90)
    b_r1_2_2.place(x=200,y=180)
    b_r1_3_3.place(x=200,y=270)
    b_r2_1_1.place(x=418, y=90)
    b_r2_2_2.place(x=418, y=180)
    b_r2_3_3.place(x=418, y=270)

    library_top.protocol("WM_DELETE_WINDOW", lambda : root.quit())

def libSquares():
    global library_top
    library_top = Toplevel(root)
    library_top.geometry("{}x{}+{}+{}".format(root_W, root_H, root_left, root_top))

    myLabel = Label(library_top, image=bimg, bg='grey5')
    myLabel.place(x=0,y=0)
    
    title = TitleMain(library_top, 'Square Library')
    title.pack(side=TOP)

    button_X = ButtonMain(library_top, '1len_1X_1Y', dim)
    button_X.config(command=lambda : libSend_square("D603B00 64 00 64 00 64\n"))
    button_Y = ButtonMain(library_top, '2len_2X_2Y', dim)
    button_Y.config(command=lambda : libSend_square("D603B00 64 00 C8 00 C8\n"))
    button_Diag = ButtonMain(library_top, '3len_3X_3Y', dim)
    button_Diag.config(command=lambda : libSend_square("D603B00 64 01 00 01 00\n"))
    
    back = ButtonMain(library_top, 'Back', dimB) 
    back.config(command = lambda : close_top('library', 'square'))
    back.place(x=0, y=0)

    button_X.place(x=309, y=90)
    button_Y.place(x=309, y=180)
    button_Diag.place(x=309, y=270)

    library_top.protocol("WM_DELETE_WINDOW", lambda : root.quit())

######################################################################################

##### SECOND MENUES ##################################################################
def secondMenu(aShape, header): # parameters decide which menu
    global menu2
    menu2 = Toplevel(root)
    menu2.geometry("{}x{}+{}+{}".format(root_W, root_H, root_left, root_top))
    
    myLabel = Label(menu2, image=bimg, bg='grey5')
    myLabel.place(x=0,y=0)
    title = TitleMain(menu2, header)
    title.place(x=363,y=10)

    button_Lib = ButtonMain(menu2, 'Library', dim)
    button_Lib.config(command=lambda : close_top2(aShape, True))
    button_Lib.place(x=309,y=90)
    button_Input = ButtonMain(menu2, 'Input Values', dim)
    button_Input.config(command=lambda : close_top2(aShape, False))
    button_Input.place(x=309,y=180)
    back = ButtonMain(menu2, 'Back', dimB) 
    back.config(command = lambda : close_top('menu2', aShape))
    back.place(x=0, y=0)
  
    menu2.protocol("WM_DELETE_WINDOW", lambda : root.quit())
    
######################################################################################

############## LINE ##################################################################  
def line(): 
    global coordinates, input_top
    
    input_top = Toplevel(root)
    input_top.geometry("{}x{}+{}+{}".format(root_W, plot_H, root_left, root_top))
    

    myLabel = Label(input_top, image=bimg, bg='black')
    myLabel.place(x=0,y=0)    
    title = TitleMain(input_top, 'PLOT LINE')
    title.pack(side=TOP)
   
    send_button = ButtonMain(input_top, 'Send', dimS)
    send_button.config(command = lambda : clickSend("601"))
    send_button.place(x=605, y=70)
    back = ButtonMain(input_top, 'Back', dimB) 
    back.config(command = lambda : (toggle_state('normal', False), input_top.destroy()))
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

    l_x0.place(x=20, y=80)
    coordinates[0].place(x=50, y=80) 
    l_y0.place(x=160, y=80)
    coordinates[1].place(x=190, y=80)
    l_x1.place(x=300, y=80)
    coordinates[2].place(x=330, y=80)
    l_y1.place(x=440, y=80)
    coordinates[3].place(x=470, y=80)
   
    input_top.protocol("WM_DELETE_WINDOW", lambda : (toggle_state('normal', False), input_top.destroy()))
    
#######################################################################################

############# CIRCLE ##################################################################
def circle():
    global coordinates, input_top
    
    input_top = Toplevel()
    input_top.geometry("{}x{}+{}+{}".format(root_W,plot_H,root_left,root_top))

    myLabel = Label(input_top, image=bimg, bg='grey5')
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
    send_button.place(x=530, y=70)
    back = ButtonMain(input_top, 'Back', dimB) 
    back.config(command = lambda : (toggle_state('normal', False), input_top.destroy()))
    back.place(x=0, y=0)

    rad_label.place(x=20, y=80)
    coordinates[0].place(x=90, y=80)
    x0_label.place(x=210, y=80)   
    coordinates[1].place(x=245, y=80)
    y0_label.place(x=360, y=80)
    coordinates[2].place(x=395, y=80)

    input_top.protocol("WM_DELETE_WINDOW", lambda : (toggle_state('normal', False), input_top.destroy()))


########################################################################################

############## SQUARE ##################################################################
def square():
    global coordinates, input_top
    
    input_top = Toplevel()
    input_top.geometry("{}x{}+{}+{}".format(root_W,plot_H,root_left,root_top))

    myLabel = Label(input_top, image=bimg, bg='grey5')
    myLabel.place(x=0,y=0)  
    title = TitleMain(input_top, 'PLOT SQUARE')
    title.pack(side=TOP)


    send_button = ButtonMain(input_top, 'Send', dimS)
    send_button.config(command = lambda : clickSend("602"))
    send_button.place(x=530, y=70)
    back = ButtonMain(input_top, 'Back', dimB) 
    back.config(command = lambda : (toggle_state('normal', False), input_top.destroy()))
    back.place(x=0, y=0)

    coordinates = [] 
    coordinates.append(InputBox(input_top))
    coordinates.append(InputBox(input_top))
    coordinates.append(InputBox(input_top))
    length_label = LabelBox(input_top, ' Length:')
    x0_label = LabelBox(input_top, ' x0:')
    y0_label = LabelBox(input_top, ' y0:')

    length_label.place(x=20, y=80)
    coordinates[0].place(x=90, y=80)
    x0_label.place(x=210, y=80)   
    coordinates[1].place(x=245, y=80)
    y0_label.place(x=360, y=80)
    coordinates[2].place(x=395, y=80)

    input_top.protocol("WM_DELETE_WINDOW", lambda : (toggle_state('normal', False), input_top.destroy()))


#########################################################################################

############## TRAVEL ###################################################################  
def travel(): 
    global coordinates, input_top
    
    input_top = Toplevel(root)
    input_top.geometry("{}x{}+{}+{}".format(root_W,plot_H,root_left,root_top))

    myLabel = Label(input_top, image=bimg, bg='grey5')
    myLabel.place(x=0,y=0)    
    title = TitleMain(input_top, 'Travel')
    title.pack(side=TOP)

    send_button = ButtonMain(input_top, 'Send', dimS)
    send_button.config(command = lambda : clickSend("604"))
    send_button.place(x=605, y=70)
    back = ButtonMain(input_top, 'Back', dimB) 
    back.config(command = lambda : (toggle_state('normal', True), input_top.destroy()))
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

    l_x0.place(x=20, y=80)
    coordinates[0].place(x=50, y=80) 
    l_y0.place(x=160, y=80)
    coordinates[1].place(x=190, y=80)
    l_x1.place(x=300, y=80)
    coordinates[2].place(x=330, y=80)
    l_y1.place(x=440, y=80)
    coordinates[3].place(x=470, y=80)
   
    input_top.protocol("WM_DELETE_WINDOW", lambda : (toggle_state('normal', True), input_top.destroy()))


#########################################################################################

############## DRAW MARIO ###############################################################
def mario():
    global input_top
    root.withdraw()
    input_top = Toplevel(root)
    input_top.geometry("{}x{}+{}+{}".format(root_W, root_H, root_left, root_top))

    myLabel = Label(input_top, image=mariPic, bg='black')
    myLabel.place(x=0,y=0)

    back = Button(input_top, text='Back', width=5, fg='dodger blue', bg='blue4',
                    activebackground='blue4', activeforeground='deep sky blue',
                    highlightthickness=0, command=lambda: close_top('top', 'mario'))
    send = Button(input_top, text='Draw Mario!', width=10,height=2, bg='red2', fg='white',
                    activebackground='darkred', activeforeground='white',
                    highlightthickness=0, highlightbackground='red',
                    command=lambda : print(str.encode('D603B\n')))
    back.pack(side=LEFT, anchor=N)
    send.place(x=330, y=290)
    input_top.protocol("WM_DELETE_WINDOW", lambda : root.quit())



#########################################################################################
# Some special button dimensions       ##
global dim,dimS,dimB                   ##
# [width,height,padx]                  ##
dim = [20,2,2,5]      # Regular Button ## 
dimS = [12,2,0,0]     # Send Button    ##
dimB = [10,1,0,5]     # Back Button    ##
#########################################

############ MAIN MENU ################################################################## 
mainTitle = TitleMain(root, 'Main Menu')
mainTitle.place(x=363,y=10)
#mainTitle.pack(side=TOP)
lineb = ButtonMain(root, 'Line', dim)
lineb.config(command=lambda : close_top('main', 'line'))
circb = ButtonMain(root, 'Circle',dim)
circb.config(command=lambda : close_top('main', 'circle'))
sqb = ButtonMain(root, 'Square',dim)
sqb.config(command=lambda : close_top('main', 'square'))
mariob = ButtonMain(root, 'Draw Mario',dim)
mariob.config(command=mario)
travelb = ButtonMain(root, 'Travel',dim)
travelb.config(command=lambda : (toggle_state('disable', True), travel()))

lineb.place(x=309,y=90)
circb.place(x=309,y=180)
sqb.place(x=309,y=270)
mariob.place(x=309,y=360)
travelb.place(x=309,y=450)

#########################################################################################

root.mainloop()

