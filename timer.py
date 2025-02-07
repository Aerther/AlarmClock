import customtkinter as ctt
import CustomTkinterMessagebox as messageBox
from functions import *

class Timer(ctt.CTkFrame):
    def __init__(self, parent, appParent):
        super().__init__(parent)
        
        self.appParent = appParent
        self.totalSeconds = 0
        self.stopped = False
        
        self.createWidgets()
    
    def createWidgets(self):
        frame = ctt.CTkFrame(self)
        frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        font = ctt.CTkFont(family="Arial", size=50)
        validateCommandHours = (self.register(lambda input: self.validateInput(input, 99)), "%P")
        validateCommandElse = (self.register(lambda input: self.validateInput(input, 59)), "%P")
        
        self.hourVar = ctt.StringVar(value="00")
        self.hourEntry = ctt.CTkEntry(frame, textvariable=self.hourVar, font=font, justify="center",
                                      validate="key", validatecommand=validateCommandHours)
        self.hourEntry.place(relx=0.2, rely=0.4, relheight=0.2, relwidth=0.25, anchor="center")
        
        self.minuteVar = ctt.StringVar(value="00")
        self.minuteEntry = ctt.CTkEntry(frame, textvariable=self.minuteVar, font=font, justify="center", 
                                        validate="key", validatecommand=validateCommandElse)
        self.minuteEntry.place(relx=0.5, rely=0.4, relheight=0.2, relwidth=0.25, anchor="center")
        
        self.secondVar = ctt.StringVar(value="00")
        self.secondEntry = ctt.CTkEntry(frame, textvariable=self.secondVar, font=font, justify="center", 
                                        validate="key", validatecommand=validateCommandElse)
        self.secondEntry.place(relx=0.8, rely=0.4, relheight=0.2, relwidth=0.25, anchor="center")
        
        labelHour = ctt.CTkLabel(frame, text="Hour", justify="center")
        labelHour.place(relx=0.2, rely=0.54, anchor="center")
        
        labelMinute = ctt.CTkLabel(frame, text="Minute", justify="center")
        labelMinute.place(relx=0.5, rely=0.54, anchor="center")
        
        labelSecond = ctt.CTkLabel(frame, text="Second", justify="center")
        labelSecond.place(relx=0.8, rely=0.54, anchor="center")
        
        label1 = ctt.CTkLabel(frame, text=":", font=font)
        label1.place(relx=0.35, rely=0.4, anchor="center")
        
        label2 = ctt.CTkLabel(frame, text=":", font=font)
        label2.place(relx=0.65, rely=0.4, anchor="center")
        
        self.button1 = ctt.CTkButton(frame, text="+1 Minute", command=lambda: self.addTotalSeconds(60))
        self.button1.place(relx=0.23, rely=0.68, relheight=0.08, relwidth=0.23, anchor="center")
        
        self.button10 = ctt.CTkButton(frame, text="+10 Minutes", command=lambda: self.addTotalSeconds(600))
        self.button10.place(relx=0.5, rely=0.68, relheight=0.08, relwidth=0.23, anchor="center")
        
        self.button15 = ctt.CTkButton(frame, text="+15 Seconds", command=lambda: self.addTotalSeconds(15))
        self.button15.place(relx=0.78, rely=0.68, relheight=0.08, relwidth=0.23, anchor="center")
        
        self.startButton = ctt.CTkButton(frame, text="Start", command=self.startTimer)
        self.startButton.place(relx=0.5, rely=0.85, relheight=0.1, relwidth=0.2, anchor="center")
        
        self.stopButton = ctt.CTkButton(frame, text="Stop", fg_color="red", text_color="white", command=lambda: self.stopTimer())
    
    def validateInput(self, input: str, value: int):
        if not input.isdecimal() and input != "":
            return False
        
        if len(input) > 2:
            return False
        
        if input != "":
            if int(input) > value:
                return False
        
        return True

    def addTotalSeconds(self, seconds):
        self.checkEntrys()
        self.totalSeconds = int(self.hourVar.get())*3600 + int(self.minuteVar.get())*60 + int(self.secondVar.get())
        self.totalSeconds += seconds
        self.updateTime()
        
        if int(self.hourVar.get()) > 99:
            self.hourVar.set("99")
            self.minuteVar.set("59")
            self.secondVar.set("59")
            self.totalSeconds -= 3600
        
    def stopTimer(self):
        self.changeButtons(self.stopButton, self.startButton)
        self.stopped = True
        
    def changeButtons(self, buttonToHide, buttonToDisplay):
        buttonToHide.place_forget()
        buttonToDisplay.place(relx=0.5, rely=0.85, relheight=0.1, relwidth=0.2, anchor="center")
        
    def changeStateOfWidgets(self, state):
        self.hourEntry.configure(state=state)
        self.minuteEntry.configure(state=state)
        self.secondEntry.configure(state=state)
        
        self.button1.configure(state=state)
        self.button10.configure(state=state)
        self.button15.configure(state=state)
    
    def checkEntrys(self):
        if self.hourVar.get() == "":
            self.hourVar.set("00")
        
        if self.minuteVar.get() == "":
            self.minuteVar.set("00")
        
        if self.secondVar.get() == "":
            self.secondVar.set("00")
            
    def startTimer(self):
        self.checkEntrys()
        self.totalSeconds = int(self.hourVar.get())*3600 + int(self.minuteVar.get())*60 + int(self.secondVar.get())
        self.stopped = False
        self.changeStateOfWidgets("disabled")
        self.changeButtons(self.startButton, self.stopButton)
        self.continueTimer()
    
    def updateTime(self):
        self.hourVar.set(f"{(self.totalSeconds//3600):02d}")
        self.minuteVar.set(f"{((self.totalSeconds % 3600)//60):02d}")
        self.secondVar.set(f"{(self.totalSeconds % 60):02d}")
        
    def continueTimer(self):
        if self.stopped or self.totalSeconds == 0:
            self.changeStateOfWidgets("normal")
            self.changeButtons(self.stopButton, self.startButton)
            
            if self.totalSeconds == 0:
                filePath = self.appParent.getPathFile("Sound", "sound.wav")
                playSound(filePath)
                messageBox.CTkMessagebox.messagebox(title="Timer", text="Timer is done", button_text="OK")
                
            return
        
        self.totalSeconds -= 1
        self.updateTime()
        
        self.after(1000, self.continueTimer)