import customtkinter as ctt
from PIL import Image
from functions import *

class Alarms(ctt.CTkFrame):
    def __init__(self, parent, appParent):
        super().__init__(parent)

        self.appParent = appParent
        self.alarmsList = []
        
        self.createWidgets()
    
    def createWidgets(self):
        # Menu Frame to create new alarms
        alarmMenuFrame = ctt.CTkFrame(self)

        newAlarmButton = ctt.CTkButton(alarmMenuFrame, text="+", font=("Arial", 30), anchor="center", fg_color="transparent", 
                                       command=lambda: self.appParent.showFrame(self.appParent.createAlarms))
        newAlarmButton.place(relx=0.9, rely=0.5, relwidth=0.1, relheight=0.5, anchor="center")
        
        # Simulate the white border for just one of the sides
        simulateBorder = ctt.CTkCanvas(alarmMenuFrame, bg="White", highlightthickness=0)
        simulateBorder.place(relx=0, rely=1, relwidth=1, relheight=0.01, anchor="sw")
        
        alarmMenuFrame.place(relx=0, rely=0, relwidth=1, relheight=0.1)
        
        # The frame for the alarms
        self.restOfTheFrame = ctt.CTkScrollableFrame(self)
        self.restOfTheFrame.place(relx=0, rely=0.1, relwidth=1, relheight=0.9)

    def createFrameForAlarm(self, alarm, text):
        imagePath = getPathFile("Images", "trash.png")
        trashImage = ctt.CTkImage(Image.open(imagePath), size=(24, 24))
        
        frame = ctt.CTkFrame(self.restOfTheFrame, height=80, border_color="grey", border_width=1)

        label = ctt.CTkLabel(frame, text=alarm, font=("Arial", 50))
        label.place(relx=0.3, rely=0.5, anchor="center")
        
        self.booleanVar = ctt.BooleanVar(value=True)
        checkButton = ctt.CTkCheckBox(frame, text="", onvalue=True, offvalue=False, variable=self.booleanVar, 
                                      command=lambda alarm=alarm: self.findAlarmAndRemove(alarm))
        checkButton.place(relx=0.78, rely=0.5, anchor="center")
        
        button = ctt.CTkButton(frame, text="", fg_color="red", image=trashImage, anchor="center", command=lambda frame=frame, alarm=alarm: self.removeAllAlarms(frame, alarm))
        button.place(relx=0.9, rely=0.5, relheight=0.4, relwidth=0.09, anchor="center")

        textLabel = ctt.CTkLabel(frame, text=text, font=("Arial", 10), height=5)
        textLabel.place(relx=0.23, rely=0.85, anchor="center")
        
        frame.pack(fill="x", padx=5, pady=10)

    def removeAllAlarms(self, frame, alarm):
        self.appParent.alarms.remove(alarm)
        if self.appParent.alarm in self.appParent.alarmsToUse:
            self.appParent.alarmsToUse.remove(alarm)
            
        frame.destroy()
        
    def findAlarmAndRemove(self, alarm):
        if self.booleanVar.get():
            self.appParent.alarmsToUse.append(alarm)
        else:
            self.appParent.alarmsToUse.remove(alarm)