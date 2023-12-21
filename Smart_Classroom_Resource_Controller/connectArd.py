import serial
import time
from tkinter import *
from datetime import datetime
from datetime import timedelta
from tkinter import messagebox
from PIL import Image, ImageTk

sf1_prevtime = datetime.now()
sf2_prevtime = datetime.now()


try:

    ardData = serial.Serial('com10',9600) #Create object to take data
    time.sleep(1)
except:
    messagebox.showerror("Error Occured! ","Error connecting to the system. Check the followings, \nPort\nConnection Cable\nSerial Communication of the microcontroller"); 
    exit()

def updates():
    
    try:
        dataPack = ardData.readline() #If there is data, store them in the dataPack variable
        dataPack = str(dataPack,'utf-8') #Get rid of unwanted characters
        dataPack = dataPack.strip('\r\n') #Get rid of the newline and other characters
        dataPack = dataPack.split(",")
        print(dataPack)

    except:
        messagebox.showerror("Error Occured! ","No response from the system."); 
        exit()
    #status == 0 -> Not active 
    #status == 1 -> Active (Lecture Ongoing) 
    #status == 2 -> Before Delay (Pre condition)
    #status == 3 -> After Delay (Time before automatically switch off)
    #status == 4 -> Power Saving 

    try:
    #SF 1 Status
        if dataPack[0] == "1":
            sf1_state.set("SF 1 - ACTIVE") 
            label_sf1.config(background="green") 
            label_sf1.update()

        elif dataPack[0] == "2":
            sf1_state.set("SF 1 - Pre Conditioning") 
            label_sf1.config(background="khaki") 
            label_sf1.update()


        elif dataPack[0] == "3":
            sf1_state.set("SF 1 - Post active delay") 
            label_sf1.config(background="salmon1") 
            label_sf1.update()

        elif dataPack[0] == "4":
            sf1_state.set("SF 1 - Power Saving") 
            label_sf1.config(background="SpringGreen2") 
            label_sf1.update()

        else:
            sf1_state.set("SF 1 - INACTIVE")
            label_sf1.config(background="IndianRed1")  
            label_sf1.update()

        #SF 2  Status
        if dataPack[1] == "1":

            sf2_state.set("SF 2 - ACTIVE") 
            label_sf2.config(background="green") 
            label_sf2.update()

        elif dataPack[1] == "2":
            sf2_state.set("SF 2 - Pre Conditioning") 
            label_sf2.config(background="khaki") 
            label_sf2.update()


        elif dataPack[1] == "3":
            sf2_state.set("SF 2 - Post active delay") 
            label_sf2.config(background="salmon1") 
            label_sf2.update()

        elif dataPack[1] == "4":
            sf2_state.set("SF 2 - Power Saving") 
            label_sf2.config(background="SpringGreen2") 
            label_sf2.update()
        
        else:
            sf2_state.set("SF 2 - INACTIVE")
            label_sf2.config(background="IndianRed1") 
            label_sf2.update()

    #SF 1 Sensor Reading

        if dataPack[2] == "1":
            
            global sf1_prevtime 
            sf1_prevtime = datetime.now()
            
    
            sf1_state_sensor.set("SF 1 - DETECTED") 
            label_sf1_sensor.config(background="green") 
            label_sf1_sensor.update()

        else:
            now = datetime.now()
            diff = now-sf1_prevtime
            a = int(diff.total_seconds())


            sf1_state_sensor.set("SF 1 - Last Detected "+str(a)+" seconds ago!")
            label_sf1_sensor.config(background="IndianRed1") 
            label_sf1_sensor.update()

    #SF 2 Sensor Reading
        if dataPack[3] == "1":

            
            global sf2_prevtime 
            sf2_prevtime = datetime.now()
            
            sf2_state_sensor.set("SF 2 - DETECTED") 
            label_sf2_sensor.config(background="green") 
            label_sf2_sensor.update()

        else:
            now = datetime.now()
            diff = now-sf2_prevtime
            a = int(diff.total_seconds())


            sf2_state_sensor.set("SF 2 - Last Detected "+str(a)+" seconds ago!")
            label_sf2_sensor.config(background="IndianRed1") 
            label_sf2_sensor.update()

        #Update delay labels

        label_sf1_beforeDelay.config(text="Before Delay :"+dataPack[4])
        label_sf1_beforeDelay.update()


        label_sf1_afterDelay.config(text="After Delay :"+dataPack[5])
        label_sf1_afterDelay.update()


        label_sf2_beforeDelay.config(text="Before Delay :"+dataPack[6])
        label_sf2_beforeDelay.update()


        label_sf2_afterDelay.config(text="After Delay :"+dataPack[7])
        label_sf2_afterDelay.update()

        #Update powerSaving Labels

        if dataPack[8] == "1":
            label_sf1_psMode.config(text="Power Saving : ON")

        else:
            label_sf1_psMode.config(text="Power Saving : OFF")


        if dataPack[9] == "1":
            label_sf2_psMode.config(text="Power Saving : ON")

        else:
            label_sf2_psMode.config(text="Power Saving : OFF")


        #Updating Time label
        
        clock.config(text=dataPack[10]+":"+dataPack[11]+":"+dataPack[12])
        clock.update()

    except:
        print("Attempt Failed!")
    
    window.after(100,updates)

  

#Tkinter Objects and Variables
    


window = Tk()

dwidth= window.winfo_screenwidth()
dheight= window.winfo_screenheight()

left=int ((dwidth-1024)/2)
top=int ((dheight-576)/2)


window.geometry(f'{1024}x{570}+{left}+{top}')
#window.config(background="#9edaf0")

window.title("Classroom Resource Management System")
window.iconbitmap('icon.ico')
window.resizable(False,False)


#c=Canvas(window,bg="gray16",height=200,width=200)
filename=PhotoImage(file="Untitled-1 copy.png")
background_label=Label(window,image=filename)
background_label.place(x=0,y=0,relwidth=1,relheight=1)

# CLOCK

#def update_time():
  #  current_time =time. strftime('%I:%M:%S %p')
   # clock.config(text=current_time)
   # clock.after(200, update_time)

clock = Label(window,font=("time",15,"bold"),background='#461e4e',fg="white" )
clock.place(x= 880, y=65)

#update_time()



p1c1 = IntVar()
p2c1 = IntVar()
p3c1 = IntVar()
p4c1 = IntVar()

p1c2 = IntVar()
p2c2 = IntVar()
p3c2 = IntVar()
p4c2 = IntVar()

ps_state_sf1 = IntVar()
ps_state_sf2 = IntVar()

#SF state variables
sf1_state = StringVar()
sf2_state = StringVar()


sf1_color = StringVar()
sf1_color.set("IndianRed1")
sf2_color = StringVar()
sf2_color.set("IndianRed1")


#SF sensor variables
sf1_state_sensor = StringVar()
sf2_state_sensor = StringVar()


sf1_color_sensor = StringVar()
sf1_color_sensor.set("IndianRed1")
sf2_color_sensor = StringVar()
sf2_color_sensor.set("IndianRed1")

global cmd

def Onclick():
    try:
    
        cmd = str(p1c1.get())+":"+str(p2c1.get())+":"+str(p3c1.get())+":"+str(p4c1.get())+":"+str(p1c2.get())+":"+str(p2c2.get())+":"+str(p3c2.get())+":"+str(p4c2.get())+":"+str(beforeDelay_sf1.get())+":"+str(afterDelay_sf1.get())+":"+str(beforeDelay_sf2.get())+":"+str(afterDelay_sf2.get())+":"+str(ps_state_sf1.get())+":"+str(ps_state_sf2.get())+"\r"
        print(cmd)
        ardData.write(cmd.encode())
        messagebox.showinfo("Data changed", "Data change successful!") 

    except:
        messagebox.showerror("Error", "No changes were done, Try again!") 



def change1(tmp): 
    print(tmp)
    if tmp > 1:
        b1.configure(bg="#24ff53")
        b2.configure(bg="white",fg="black")
    else :
        b1.configure(bg="white")
        b2.configure(bg="red",fg="white")

def change2(tmp): 
    if tmp > 1:
        b3.configure(bg="#24ff53")
        b4.configure(bg="white",fg="black")
    else :
        b3.configure(bg="white")
        b4.configure(bg="red",fg="white")

def change3(tmp): 
    if tmp > 1:
        b5.configure(bg="#24ff53")
        b6.configure(bg="white",fg="black")
    else :
        b5.configure(bg="white")
        b6.configure(bg="red",fg="white")

def change4(tmp): 
    if tmp > 1:
        b7.configure(bg="#24ff53")
        b8.configure(bg="white",fg="black")
    else :
        b7.configure(bg="white")
        b8.configure(bg="red",fg="white")



b1 = Radiobutton(window, text = "ON",value=8,variable=p1c1,font=("Arial",10,"bold"),fg="#012b3b", command=lambda:change1(p1c1.get()))
b1.place(x=350, y=180)
b2 = Radiobutton(window, text = "OFF",value=0,variable=p1c1,font=("Arial",10,"bold",),fg="#012b3b",command=lambda:change1(p1c1.get()))
b2.place(x=430, y=180,)

b3 = Radiobutton(window, text = "ON",value=10,variable=p2c1,font=("Arial",10,"bold"),fg="#012b3b",command=lambda:change2(p2c1.get()))
b3.place(x=350, y=214)
b4 = Radiobutton(window, text = "OFF",value=0,variable=p2c1,font=("Arial",10,"bold"),fg="#012b3b",command=lambda:change2(p2c1.get()))
b4.place(x=430, y=214)

b5 = Radiobutton(window, text = "ON",value=13,variable=p3c1,font=("Arial",10,"bold"),fg="#012b3b",command=lambda:change3(p3c1.get()))
b5.place(x=350, y=248)
b6 = Radiobutton(window, text = "OFF",value=0,variable=p3c1,font=("Arial",10,"bold"),fg="#012b3b",command=lambda:change3(p3c1.get()))
b6.place(x=430, y=248)

b7 = Radiobutton(window, text = "ON",value=15,variable=p4c1,font=("Arial",10,"bold"),fg="#012b3b",command=lambda:change4(p4c1.get()))
b7.place(x=350, y=281)
b8 = Radiobutton(window, text = "OFF",value=0,variable=p4c1,font=("Arial",10,"bold"),fg="#012b3b",command=lambda:change4(p4c1.get()))
b8.place(x=430, y=281)




# SF 01 Radio B


def change5(tmp): 
    if tmp > 1:
        b9.configure(bg="#24ff53")
        b10.configure(bg="white",fg="black")
    else :
        b9.configure(bg="white")
        b10.configure(bg="red",fg="white")

def change6(tmp): 
    if tmp > 1:
        b11.configure(bg="#24ff53")
        b12.configure(bg="white",fg="black")
    else :
        b11.configure(bg="white")
        b12.configure(bg="red",fg="white")

def change7(tmp): 
    if tmp > 1:
        b13.configure(bg="#24ff53")
        b14.configure(bg="white",fg="black")
    else :
        b13.configure(bg="white")
        b14.configure(bg="red",fg="white")

def change8(tmp): 
    if tmp > 1:
        b15.configure(bg="#24ff53")
        b16.configure(bg="white",fg="black")
    else :
        b15.configure(bg="white")
        b16.configure(bg="red",fg="white")

b9 = Radiobutton(window, text = "ON",value=8,variable=p1c2,font=("Arial",10,"bold"),fg="#012b3b",command=lambda:change5(p1c2.get()))
b9.place(x=645, y=180)
b10 = Radiobutton(window, text = "OFF",value=0,variable=p1c2,font=("Arial",10,"bold",),fg="#012b3b",command=lambda:change5(p1c2.get()))
b10.place(x=725, y=180,)

b11 = Radiobutton(window, text = "ON",value=10,variable=p2c2,font=("Arial",10,"bold"),fg="#012b3b",command=lambda:change6(p2c2.get()))
b11.place(x=645, y=214)
b12 = Radiobutton(window, text = "OFF",value=0,variable=p2c2,font=("Arial",10,"bold"),fg="#012b3b",command=lambda:change6(p2c2.get()))
b12.place(x=725, y=214)

b13 = Radiobutton(window, text = "ON",value=13,variable=p3c2,font=("Arial",10,"bold"),fg="#012b3b",command=lambda:change7(p3c2.get()))
b13.place(x=645, y=248)
b14 = Radiobutton(window, text = "OFF",value=0,variable=p3c2,font=("Arial",10,"bold"),fg="#012b3b",command=lambda:change7(p3c2.get()))
b14.place(x=725, y=248)

b15 = Radiobutton(window, text = "ON",value=15,variable=p4c2,font=("Arial",10,"bold"),fg="#012b3b",command=lambda:change8(p4c2.get()))
b15.place(x=645, y=281)
b16 = Radiobutton(window, text = "OFF",value=0,variable=p4c2,font=("Arial",10,"bold"),fg="#012b3b",command=lambda:change8(p4c2.get()))
b16.place(x=725, y=281)




#Before delay times SF01///

#l1 = Label(window, text = "Before Delay (In minites)", font=("Arial",8,"bold"),fg="#012b3b", bg="white")
#l1.place(x=200, y= 334)

#l2 = Label(window, text = "Before Delay (In minites)", font=("Arial",8,"bold"),fg="#012b3b", bg="white")
#l2.place(x=200, y= 351)

beforeDelay_sf1 = Entry(window, width=35,fg="white",bg="grey")
beforeDelay_sf1.place(x=299, y=320)
#beforeDelay_sf1.insert(0,"Enter Time",)

afterDelay_sf1 = Entry(window, width=35,fg="white",bg="grey")
afterDelay_sf1.place(x=299, y=348)
#afterDelay_sf1.insert(0,"Enter Time",)




# check button///
ps_state_sf1 = IntVar()
ps_state_sf2 = IntVar()

c1 = Checkbutton(window,variable=ps_state_sf1, onvalue=1, offvalue=0)
c1.place(x=299, y=370)


#Before delay times SF02///

beforeDelay_sf2 = Entry(window, width=35,fg="white",bg="grey")
beforeDelay_sf2.place(x=732, y=320)
#beforeDelay_sf2.insert(0,"Enter Time",)

afterDelay_sf2 = Entry(window, width=35,fg="white",bg="grey")
afterDelay_sf2.place(x=732, y=348)
#afterDelay_sf2.insert(0,"Enter Time",)

c2 = Checkbutton(window,variable=ps_state_sf2, onvalue=1, offvalue=0)
c2.place(x=732, y=370)


#Apply Change Button

bb = Button(window,width=122, text = " Apply Changes",font=("Arial",10,"bold"),fg="white",bg="#2b1130", activebackground="#e9b303",command=Onclick)
bb.place(x= 20, y=535, )



# SF 01 Live Status

#label_sf1 = Label(frame_sf1_status,textvariable=sf1_state,background=sf1_color.get())
label_sf1 = Label(window, text = "SF 1 INACTIVE ", font=("Arial",8,"bold"),fg="black", bg="red",textvariable=sf1_state)
label_sf1.place(x=300, y=420)

#label_sf1_sensor = Label(frame_sf1_status,textvariable=sf1_state_sensor,background=sf1_color_sensor.get())
label_sf1_sensor = Label(window, text = "Last detected 8 secons ago !", font=("Arial",8,"bold"),fg="black", bg="indian red" ,textvariable=sf1_state_sensor)
label_sf1_sensor.place(x=300, y=441)

#label_sf1_beforeDelay = Label(frame_sf1_status)
label_sf1_beforeDelay = Label(window, text = "Before Delay : 0", font=("Arial",8,"bold"))
label_sf1_beforeDelay.place(x=300, y=461)

#label_sf1_afterDelay = Label(frame_sf1_status)
label_sf1_afterDelay = Label(window, text = "After Delay : 0", font=("Arial",8,"bold"))
label_sf1_afterDelay.place(x=300, y=481)

#label_sf1_psMode = Label(frame_sf1_status)
label_sf1_psMode = Label(window, text = "Power Saving : OFF", font=("Arial",8,"bold"))
label_sf1_psMode.place(x=300, y=501)




# SF 01 Live Status

#label_sf2 = Label(frame_sf2_status,textvariable=sf2_state,background=sf2_color.get())
label_sf2 = Label(window, text = "SF 2 INACTIVE ", font=("Arial",8,"bold"),fg="black", bg="red" ,textvariable=sf2_state)
label_sf2.place(x=732, y=420)

#label_sf2_sensor = Label(frame_sf2_status,textvariable=sf2_state_sensor,background=sf2_color_sensor.get())
label_sf2_sensor = Label(window, text = "Last detected 0 secons ago !", font=("Arial",8,"bold"),fg="black", bg="indian red",textvariable=sf2_state_sensor)
label_sf2_sensor.place(x=732, y=441)

#label_sf2_beforeDelay = Label(frame_sf2_status)
label_sf2_beforeDelay = Label(window, text = "Before Delay : 0", font=("Arial",8,"bold"))
label_sf2_beforeDelay.place(x=732, y=461)

#label_sf2_afterDelay = Label(frame_sf2_status)
label_sf2_afterDelay = Label(window, text = "After Delay : 0", font=("Arial",8,"bold"))
label_sf2_afterDelay.place(x=732, y=481)

#label_sf2_psMode = Label(frame_sf2_status)
label_sf2_psMode = Label(window, text = "Power Saving : OFF", font=("Arial",8,"bold"))
label_sf2_psMode .place(x=732, y=501)

window.after(100,updates)
window.mainloop()



