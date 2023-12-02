import serial
import time
from tkinter import *
from datetime import datetime

ardData = serial.Serial('com10',9600) #Create object to take data
time.sleep(1)

def updates():
    dataPack = ardData.readline() #If there is data, store them in the dataPack variable
    dataPack = str(dataPack,'utf-8') #Get rid of unwanted characters
    dataPack = dataPack.strip('\r\n') #Get rid of the newline and other characters
    print(dataPack)

    if dataPack[0] == "1":
        sf1_state.set("SF 1 - ACTIVE") 
        label_sf1.config(background="green") 
        label_sf1.update()

    else:
        sf1_state.set("SF 1 - INACTIVE")
        label_sf1.config(background="red")  
        label_sf1.update()

        
    if dataPack[2] == "1":

        sf2_state.set("SF 2 - ACTIVE") 
        label_sf2.config(background="green") 
        label_sf2.update()

    else:
        sf2_state.set("SF 2 - INACTIVE")
        label_sf2.config(background="red") 
        label_sf2.update()




    root.after(1000,updates)



root = Tk()

p1c1 = IntVar()
p2c1 = IntVar()
p3c1 = IntVar()
p4c1 = IntVar()

p1c2 = IntVar()
p2c2 = IntVar()
p3c2 = IntVar()
p4c2 = IntVar()

global cmd

def Onclick():
 


    ardData = serial.Serial('com10',9600) #Create object to take data
    time.sleep(1) #Delay to make sure the com port is initialized 

    


    #if (e1.get() == "YES"):
    #    p1c1 = 1
    #if (e1.get() =="NO"):
    #    p1c1 = 0

    #if (e2.get() == "YES"):

    #    p2c1 = 1
    #if (e2.get() =="NO"):
    #    p2c1 = 0

    #if (e3.get() == "YES"):
    #    p3c1 = 1
    #if (e3.get() =="NO"):
    #    p3c1 = 0

    #if (e4.get() == "YES"):
    #    p4c1 = 1
    #if (e4.get() =="NO"):
    #    p4c1 = 0

   # ardData.write(struct.pack('>iiii',p2c1,p2c1,p3c1,p4c1))
    cmd = str(p1c1.get())+":"+str(p2c1.get())+":"+str(p3c1.get())+":"+str(p4c1.get())+":"+str(p1c2.get())+":"+str(p2c2.get())+":"+str(p3c2.get())+":"+str(p4c2.get())+"\r"
    print(cmd)
    for n in range (0,100):
        ardData.write(cmd.encode())
        print(cmd)



    #dt = datetime.now()
    #time_hour = dt.hour

    #Timeslot 8 - 10
    #if ((p1c1 == True) and (time_hour == 8 or time_hour == 9)):
    #        cmd = "ON"

    #Timeslot 10- 12

    #elif ((p2c1 == True) and (time_hour == 10 or time_hour == 12)):
    #        print("AWA")
    #        cmd = "ON"
          
    #Timeslot 1 - 3

    #elif ((p3c1 == True) and (time_hour == 13 or time_hour == 15)):
    #        cmd = "ON"

    #Timeslot 3 - 5

    #elif ((p4c1 == True) and (time_hour == 15 or time_hour == 17)):
    #        cmd = "ON"


    #else:
    #        cmd = "OFF"

    
    
 
    #print(cmd)
    #newcmd = cmd+"\r"
    #while True:
    #    print(cmd)
    #    ardData.write(newcmd.encode())
    #    print(time_hour)


    #cmd = e1.get()
    #ardData.write(cmd.encode())


mylabel = Label(root,text="Classroom Resource Controller")
label_Title1 = Label(root,text="Time Period")
label_period1 = Label(root,text="08:00 - 10:00")
label_period2 = Label(root,text="10:00 - 12:00")
label_period3 = Label(root,text="13:00 - 15:00")
label_period4 = Label(root,text="15:00 - 17:00")

label_Title2 = Label(root,text="SF-1")

R1 = Radiobutton(root, text="YES", variable=p1c1, value=1)
R2 = Radiobutton(root, text="NO", variable=p1c1, value=0)

R3 = Radiobutton(root, text="YES", variable=p2c1, value=1)
R4 = Radiobutton(root, text="NO", variable=p2c1, value=0)

R5 = Radiobutton(root, text="YES", variable=p3c1, value=1)
R6 = Radiobutton(root, text="NO", variable=p3c1, value=0)

R7 = Radiobutton(root, text="YES", variable=p4c1, value=1)
R8 = Radiobutton(root, text="NO", variable=p4c1, value=0)

label_Title3 = Label(root,text="SF-2")

R9 = Radiobutton(root, text="YES", variable=p1c2, value=1)
R10 = Radiobutton(root, text="NO", variable=p1c2, value=0)

R11= Radiobutton(root, text="YES", variable=p2c2, value=1)
R12 = Radiobutton(root, text="NO", variable=p2c2, value=0)

R13= Radiobutton(root, text="YES", variable=p3c2, value=1)
R14= Radiobutton(root, text="NO", variable=p3c2, value=0)

R15= Radiobutton(root, text="YES", variable=p4c2, value=1)
R16= Radiobutton(root, text="NO", variable=p4c2, value=0)


#e1 = Entry(root,width=30,fg="White",bg="black")
#e2 = Entry(root,width=30,fg="White",bg="black")
#e3 = Entry(root,width=30,fg="White",bg="black")
#e4 = Entry(root,width=30,fg="White",bg="black")

b1 = Button(root,text="Upload",width=50,bg="Green",command=Onclick)

mylabel.grid(row=0,columnspan=3)

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

#e1.grid(row =2, column=1)
#e2.grid(row =3, column=1)
#e3.grid(row =4, column=1)
#e4.grid(row =5, column=1)

b1.grid(row =6,columnspan=5)




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