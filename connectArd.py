import serial
import time
from tkinter import *
from datetime import datetime
from datetime import timedelta
from tkinter import messagebox


sf1_prevtime = datetime.now()
sf2_prevtime = datetime.now()

ardData = serial.Serial('com10',9600) #Create object to take data
time.sleep(1)


def updates():
    
    dataPack = ardData.readline() #If there is data, store them in the dataPack variable
    dataPack = str(dataPack,'utf-8') #Get rid of unwanted characters
    dataPack = dataPack.strip('\r\n') #Get rid of the newline and other characters
    dataPack = dataPack.split(",")
    print(dataPack)

    #status == 0 -> Not active 
    #status == 1 -> Active (Lecture Ongoing) 
    #status == 2 -> Before Delay (Pre condition)
    #status == 3 -> After Delay (Time before automatically switch off)
    #status == 4 -> Power Saving 

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

    root.after(1000,updates)

#Tkinter Objects and Variables
root = Tk()
root.title("Classroom Resource Management System")

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


# -- Tkinter Design -- 

mylabel = Label(root,text="Control Panel",font="Times 20 bold")
mylabel.grid(row=1,columnspan=5)


#Control Frame

frame_control =Frame(root,padx=10,pady=10)
frame_control.grid(row=2,column=0)


label_Title1 = Label(frame_control,text="Time Period",font="Times 12 bold")
label_period1 = Label(frame_control,text="08:00 - 10:00")
label_period2 = Label(frame_control,text="10:00 - 12:00")
label_period3 = Label(frame_control,text="13:00 - 15:00")
label_period4 = Label(frame_control,text="15:00 - 17:00")


label_Title1.grid(row =1, column=0)
label_period1.grid(row =2, column=0)
label_period2.grid(row =3, column=0)
label_period3.grid(row =4, column=0)
label_period4.grid(row =5, column=0)


label_Title2 = Label(frame_control,text="SF-1",font="Times 12 bold")
label_Title2.grid(row =1, column=1, columnspan=2)


R1 = Radiobutton(frame_control, text="YES", variable=p1c1, value=8)
R2 = Radiobutton(frame_control, text="NO", variable=p1c1, value=0)

R3 = Radiobutton(frame_control, text="YES", variable=p2c1, value=10)
R4 = Radiobutton(frame_control, text="NO", variable=p2c1, value=0)

R5 = Radiobutton(frame_control, text="YES", variable=p3c1, value=13)
R6 = Radiobutton(frame_control, text="NO", variable=p3c1, value=0)

R7 = Radiobutton(frame_control, text="YES", variable=p4c1, value=15)
R8 = Radiobutton(frame_control, text="NO", variable=p4c1, value=0)

R1.grid(row=2, column=1)
R2.grid(row=2, column=2)

R3.grid(row=3, column=1)
R4.grid(row=3, column=2)

R5.grid(row=4, column=1)
R6.grid(row=4, column=2)

R7.grid(row=5, column=1)
R8.grid(row=5, column=2)


label_beforeDelay_sf1 = Label(frame_control,text="Before Delay (In minuites)")
label_afterDelay_sf1 = Label(frame_control,text="After Delay (In minuites)")


label_beforeDelay_sf1.grid(row = 6, column=1)
label_afterDelay_sf1.grid(row=7,column=1)


beforeDelay_sf1 = Entry(frame_control,width=30,fg="black",bg="grey")
afterDelay_sf1 = Entry(frame_control,width=30,fg="black",bg="grey")
beforeDelay_sf1.grid(row=6, column=2)
afterDelay_sf1.grid(row=7, column=2)


c1 = Checkbutton(frame_control, text='Power Saving ',variable=ps_state_sf1, onvalue=1, offvalue=0)
c1.grid(row=8,column=1,columnspan=2)




dividerFrame =Frame(frame_control,width=2,padx=20,bg="grey",height=350,border=10)
dividerFrame.grid(row=1,rowspan=10,column=3,padx=5,pady=5)




label_Title3 = Label(frame_control,text="SF-2",font="Times 12 bold")
label_Title3.grid(row =1, column=4, columnspan=2)




R9 = Radiobutton(frame_control, text="YES", variable=p1c2, value=8)
R10 = Radiobutton(frame_control, text="NO", variable=p1c2, value=0)

R11= Radiobutton(frame_control, text="YES", variable=p2c2, value=10)
R12 = Radiobutton(frame_control, text="NO", variable=p2c2, value=0)

R13= Radiobutton(frame_control, text="YES", variable=p3c2, value=13)
R14= Radiobutton(frame_control, text="NO", variable=p3c2, value=0)

R15= Radiobutton(frame_control, text="YES", variable=p4c2, value=15)
R16= Radiobutton(frame_control, text="NO", variable=p4c2, value=0)

R9.grid(row=2, column=4)
R10.grid(row=2, column=5)

R11.grid(row=3, column=4)
R12.grid(row=3, column=5)

R13.grid(row=4, column=4)
R14.grid(row=4, column=5)

R15.grid(row=5, column=4)
R16.grid(row=5, column=5)


label_beforeDelay_sf2 = Label(frame_control,text="Before Delay (In minuites)")
label_afterDelay_sf2 = Label(frame_control,text="After Delay (In minuites)")

label_beforeDelay_sf2.grid(row = 6, column=4)
label_afterDelay_sf2.grid(row=7,column=4)

beforeDelay_sf2 = Entry(frame_control,width=30,fg="black",bg="grey")
afterDelay_sf2 = Entry(frame_control,width=30,fg="black",bg="grey")

beforeDelay_sf2.grid(row=6, column=5)
afterDelay_sf2.grid(row=7, column=5)

c2 = Checkbutton(frame_control, text='Power Saving ',variable=ps_state_sf2, onvalue=1, offvalue=0)
c2.grid(row=8,column=4,columnspan=2)

b1 = Button(frame_control,text="Apply Changes",width="100",activeforeground="white", activebackground="black",bg="grey64",command=Onclick,font="Times 12 bold")
b1.grid(row =11,columnspan=7,pady=5)


#Frame sf1 (SubFrame within the Control Frame)

frame_sf1_status = Frame(frame_control,highlightbackground="grey" , highlightthickness=2,width=100)

label_sf1Topic = Label(frame_sf1_status,text="SF 1 Live Status",font="Times 12 bold")
label_sf1Topic.grid(row=0,column=0,columnspan=2)


frame_sf1_status.grid(row=10,column=1,columnspan=2)
label_sf1 = Label(frame_sf1_status,textvariable=sf1_state,background=sf1_color.get())
label_sf1.grid(row=1,column=0,pady=5)

label_sf1_sensor = Label(frame_sf1_status,textvariable=sf1_state_sensor,background=sf1_color_sensor.get())
label_sf1_sensor.grid(row=2,column=0)

label_sf1_beforeDelay = Label(frame_sf1_status)
label_sf1_beforeDelay.grid(row=3,column=0)

label_sf1_afterDelay = Label(frame_sf1_status)
label_sf1_afterDelay.grid(row=4,column=0)

label_sf1_psMode = Label(frame_sf1_status)
label_sf1_psMode.grid(row = 5, column = 0)



#Frame sf2 (Subframe within the control frame)

frame_sf2_status = Frame(frame_control,highlightbackground="grey" , highlightthickness=2,width=100)

label_sf2Topic = Label(frame_sf2_status,text="SF 2 Live Status",font="Times 12 bold")
label_sf2Topic.grid(row=0,column=0,columnspan=2)

frame_sf2_status.grid(row=10,column=4,columnspan=2)

label_sf2 = Label(frame_sf2_status,textvariable=sf2_state,background=sf2_color.get())
label_sf2.grid(row=1,column=0,pady=5)

label_sf2_sensor = Label(frame_sf2_status,textvariable=sf2_state_sensor,background=sf2_color_sensor.get())
label_sf2_sensor.grid(row=2,column=0)


label_sf2_beforeDelay = Label(frame_sf2_status)
label_sf2_beforeDelay.grid(row=3,column=0)

label_sf2_afterDelay = Label(frame_sf2_status)
label_sf2_afterDelay.grid(row=4,column=0)


label_sf2_psMode = Label(frame_sf2_status)
label_sf2_psMode .grid(row = 5, column = 0)

root.after(1000,updates)

root.mainloop()