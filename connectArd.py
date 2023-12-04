import serial
import time
from tkinter import *
from datetime import datetime
from datetime import timedelta



sf1_prevtime = datetime.now()
sf2_prevtime = datetime.now()

noMotion_time_Sf1 = 0
noMotion_time_Sf2 = 0

ardData = serial.Serial('com10',9600) #Create object to take data
time.sleep(1)


def updates():
    dataPack = ardData.readline() #If there is data, store them in the dataPack variable
    dataPack = str(dataPack,'utf-8') #Get rid of unwanted characters
    dataPack = dataPack.strip('\r\n') #Get rid of the newline and other characters
    print(dataPack)

    #SF 1 Active Status
    if dataPack[0] == "1":
        sf1_state.set("SF 1 - ACTIVE") 
        label_sf1.config(background="green") 
        label_sf1.update()

    else:
        sf1_state.set("SF 1 - INACTIVE")
        label_sf1.config(background="red")  
        label_sf1.update()

    
    #SF 2 Active Status
    if dataPack[2] == "1":

        sf2_state.set("SF 2 - ACTIVE") 
        label_sf2.config(background="green") 
        label_sf2.update()

    else:
        sf2_state.set("SF 2 - INACTIVE")
        label_sf2.config(background="red") 
        label_sf2.update()

    #SF 1 Sensor Reading
    
    #sf1_prevtime = now.strftime("%H:%M:%S")
    
    if dataPack[4] == "1":
        
        global sf1_prevtime 
        sf1_prevtime = datetime.now()
        
        #sf1_prevtime = now.strftime("%H:%M:%S")
      
        
        sf1_state_sensor.set("SF 1 - DETECTED") 
        label_sf1_sensor.config(background="green") 
        label_sf1_sensor.update()

    else:
        now = datetime.now()
        diff = now-sf1_prevtime
        a = int(diff.total_seconds())
        noMotion_time_Sf1 = a

       # if (noMotion_time_Sf1> 600):
            

        #print(str(a))

        sf1_state_sensor.set("SF 1 - Last Detected "+str(a)+" seconds ago!")
        label_sf1_sensor.config(background="red") 
        label_sf1_sensor.update()

#SF 2 Sensor Reading
    if dataPack[6] == "1":

        
        global sf2_prevtime 
        sf2_prevtime = datetime.now()
        
        sf2_state_sensor.set("SF 2 - DETECTED") 
        label_sf2_sensor.config(background="green") 
        label_sf2_sensor.update()

    else:
        now = datetime.now()
        diff = now-sf2_prevtime
        a = int(diff.total_seconds())
        noMotion_time_Sf2 = a

       # if (noMotion_time_Sf1> 600):
            

        #print(str(a))

        sf2_state_sensor.set("SF 2 - Last Detected "+str(a)+" seconds ago!")
        label_sf2_sensor.config(background="red") 
        label_sf2_sensor.update()

    root.after(1000,updates)



root = Tk()
frame_control =Frame(root,padx="10",pady="10")
frame_status =Frame(root,width="60",padx="10",pady="10")
frame_sensorReading = Frame(root,width="60",padx="10",pady="10")

p1c1 = IntVar()
p2c1 = IntVar()
p3c1 = IntVar()
p4c1 = IntVar()

p1c2 = IntVar()
p2c2 = IntVar()
p3c2 = IntVar()
p4c2 = IntVar()

#SF state variables
sf1_state = StringVar()
sf2_state = StringVar()


sf1_color = StringVar()
sf1_color.set("red")
sf2_color = StringVar()
sf2_color.set("red")


#SF sensor variables
sf1_state_sensor = StringVar()
sf2_state_sensor = StringVar()


sf1_color_sensor = StringVar()
sf1_color_sensor.set("red")
sf2_color_sensor = StringVar()
sf2_color_sensor.set("red")




global cmd

def Onclick():
   
    cmd = str(p1c1.get())+":"+str(p2c1.get())+":"+str(p3c1.get())+":"+str(p4c1.get())+":"+str(p1c2.get())+":"+str(p2c2.get())+":"+str(p3c2.get())+":"+str(p4c2.get())+"\r"
    print(cmd)
    ardData.write(cmd.encode())





#Tkinter






mylabel = Label(root,text="Classroom Resource Controller",font="15")

label_Title1 = Label(frame_control,text="Time Period")
label_period1 = Label(frame_control,text="08:00 - 10:00")
label_period2 = Label(frame_control,text="10:00 - 12:00")
label_period3 = Label(frame_control,text="13:00 - 15:00")
label_period4 = Label(frame_control,text="15:00 - 17:00")

label_Title2 = Label(frame_control,text="SF-1")

R1 = Radiobutton(frame_control, text="YES", variable=p1c1, value=1)
R2 = Radiobutton(frame_control, text="NO", variable=p1c1, value=0)

R3 = Radiobutton(frame_control, text="YES", variable=p2c1, value=1)
R4 = Radiobutton(frame_control, text="NO", variable=p2c1, value=0)

R5 = Radiobutton(frame_control, text="YES", variable=p3c1, value=1)
R6 = Radiobutton(frame_control, text="NO", variable=p3c1, value=0)

R7 = Radiobutton(frame_control, text="YES", variable=p4c1, value=1)
R8 = Radiobutton(frame_control, text="NO", variable=p4c1, value=0)

label_Title3 = Label(frame_control,text="SF-2")

R9 = Radiobutton(frame_control, text="YES", variable=p1c2, value=1)
R10 = Radiobutton(frame_control, text="NO", variable=p1c2, value=0)

R11= Radiobutton(frame_control, text="YES", variable=p2c2, value=1)
R12 = Radiobutton(frame_control, text="NO", variable=p2c2, value=0)

R13= Radiobutton(frame_control, text="YES", variable=p3c2, value=1)
R14= Radiobutton(frame_control, text="NO", variable=p3c2, value=0)

R15= Radiobutton(frame_control, text="YES", variable=p4c2, value=1)
R16= Radiobutton(frame_control, text="NO", variable=p4c2, value=0)

frame_control.grid(row=2,column=0)

#e1 = Entry(root,width=30,fg="White",bg="black")
#e2 = Entry(root,width=30,fg="White",bg="black")
#e3 = Entry(root,width=30,fg="White",bg="black")
#e4 = Entry(root,width=30,fg="White",bg="black")

b1 = Button(frame_control,text="Upload",width=50,bg="Green",command=Onclick)



#Frame_Status

frame_status.grid(row=2,column=1)
label_Title4 = Label(frame_status,text="Current Status")

label_sf1 = Label(frame_status,textvariable=sf1_state,background=sf1_color.get())
label_sf2 = Label(frame_status,textvariable=sf2_state,background=sf1_color.get())

#Frame_SensorRead
frame_sensorReading.grid(row= 2,column=2)
label_Title5 = Label(frame_sensorReading,text="Sensor Detection")

label_sf1_sensor = Label(frame_sensorReading,textvariable=sf1_state_sensor,background=sf1_color_sensor.get())
label_sf2_sensor = Label(frame_sensorReading,textvariable=sf2_state_sensor,background=sf2_color_sensor.get())


#Frame control grid
mylabel.grid(row=1,columnspan=4)

label_Title1.grid(row =1, column=0)
label_period1.grid(row =2, column=0)
label_period2.grid(row =3, column=0)
label_period3.grid(row =4, column=0)
label_period4.grid(row =5, column=0)

label_Title2.grid(row =1, column=1, columnspan=2)

R1.grid(row=2, column=1)
R2.grid(row=2, column=2)

R3.grid(row=3, column=1)
R4.grid(row=3, column=2)

R5.grid(row=4, column=1)
R6.grid(row=4, column=2)

R7.grid(row=5, column=1)
R8.grid(row=5, column=2)


label_Title3.grid(row =1, column=3, columnspan=2)

R9.grid(row=2, column=3)
R10.grid(row=2, column=4)

R11.grid(row=3, column=3)
R12.grid(row=3, column=4)

R13.grid(row=4, column=3)
R14.grid(row=4, column=4)

R15.grid(row=5, column=3)
R16.grid(row=5, column=4)

b1.grid(row =6,columnspan=5)





#Frame status grid
label_Title4.grid(row = 0, column=0)
label_sf1.grid(row =1, column=0)
label_sf2.grid(row =2, column=0)

#Frame_SensorRead
label_Title5.grid(row=0,column=0)
label_sf1_sensor.grid(row =1, column=0)
label_sf2_sensor.grid(row =2, column=0)


    
root.after(1000,updates)

root.mainloop()
    
    #When sending python data to arduino, we have to kill the arduino program before uploading arduino code to board.
    #And also the data sended on python cannot read by serial monitor because the com Port is already locked up by python


#while True:
#   while(ardData.inWaiting()==0):
#        pass #If there is no data to read, keep looping 
#
#    dataPack = ardData.readline() #If there is data, store them in the dataPack variable
#    dataPack = str(dataPack,'utf-8') #Get rid of unwanted characters
#    dataPack = dataPack.strip('\r\n') #Get rid of the newline and other characters
#    print(dataPack)