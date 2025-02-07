import customtkinter as ctt
import datetime
from functions import *

class StopWatch(ctt.CTkFrame):
    def __init__(self, parent, appParent):
        super().__init__(parent)
        
        self.appParent = appParent
        self.stopped = False
        
        self.createWidgets()
        
    def createWidgets(self):
        frame = ctt.CTkFrame(self)
        frame.place(relx=0, rely=0, relheight=1, relwidth=1)
        
        labelFont = ctt.CTkFont(family="Arial", size=55)
        self.stringVar = ctt.StringVar(value="00:00:00,00")
        stopWatchLabel = ctt.CTkLabel(frame, textvariable=self.stringVar, font=labelFont)
        stopWatchLabel.place(relx=0.5, rely=0.25, anchor="center")
        
        self.startButton = ctt.CTkButton(frame, text="Start", command=lambda: self.startStopWatch())
        self.startButton.place(relx=0.5, rely=0.85, relheight=0.08, relwidth=0.23, anchor="center")
        
        self.stopButton = ctt.CTkButton(frame, text="Stop", fg_color="red", command=lambda: self.stopStopWatch())
        self.saveButton = ctt.CTkButton(frame, text="Save", command=lambda: self.saveStopWatch())
        
        self.scrollFrame = ctt.CTkScrollableFrame(frame)
        self.scrollFrame.place(relx=0.5, rely=0.55, relheight=0.3, relwidth=0.9, anchor="center")
    
    def addFrameToScrollFrame(self):
        frame = ctt.CTkFrame(self.scrollFrame, height=35)
        frame.pack(fill="x", pady=5, padx=5, side="bottom")
        
        label = ctt.CTkLabel(frame, text=self.timeText, font=("Arial", 30))
        label.place(relx=0.5, rely=0.5, anchor="center")

    def changeButtons(self, isHiding):
        if isHiding:
            self.startButton.place_forget()
            self.stopButton.place(relx=0.5, rely=0.85, relheight=0.08, relwidth=0.23, anchor="center")
            self.saveButton.place(relx=0.5, rely=0.85, relheight=0.08, relwidth=0.23, anchor="center")
        else:
            self.startButton.place(relx=0.5, rely=0.85, relheight=0.08, relwidth=0.23, anchor="center")
            self.stopButton.place_forget()
            self.saveButton.place_forget()
    
    def saveStopWatch(self):
        self.addFrameToScrollFrame()
    
    def buttonAnimation(self, startRelX, endRelX, changeRelX, isChange):
        if isChange:
            if endRelX > startRelX+changeRelX:
                changeRelX += 0.01
                self.stopButton.place(relx=startRelX-changeRelX, rely=0.85, relheight=0.08, relwidth=0.23, anchor="center")
                self.saveButton.place(relx=startRelX+changeRelX, rely=0.85, relheight=0.08, relwidth=0.23, anchor="center")
                self.after(5, lambda: self.buttonAnimation(startRelX, endRelX, changeRelX, True))
        else:
            if endRelX < startRelX+changeRelX:
                changeRelX -= 0.01
                self.stopButton.place(relx=(1-startRelX)-changeRelX, rely=0.85, relheight=0.08, relwidth=0.23, anchor="center")
                self.saveButton.place(relx=startRelX+changeRelX, rely=0.85, relheight=0.08, relwidth=0.23, anchor="center")
                self.after(5, lambda: self.buttonAnimation(startRelX, endRelX, changeRelX, False))
            else:
                self.changeButtons(False)
                self.changeStatsOfButton(self.stopButton, "Stop", "red", lambda: self.stopStopWatch())
                self.changeStatsOfButton(self.saveButton, "Save", self.saveButton.cget("fg_color"), lambda: self.saveStopWatch())
                
    def changeStatsOfButton(self, button, text, fgColor, command):
        button.configure(text=text, fg_color=fgColor, command=command)
    
    def continueStopWatch(self):
        self.stopped = False
        
        self.changeStatsOfButton(self.stopButton, "Stop", "red", lambda: self.stopStopWatch())
        self.changeStatsOfButton(self.saveButton, "Save", self.saveButton.cget("fg_color"), lambda: self.saveStopWatch())
        
        self.inicialDateTime = datetime.datetime.now()
        self.beGoingStopWatch(self.totalSeconds)
    
    def restartStopWatch(self):
        self.after(5, lambda: self.buttonAnimation(0.75, 0.5, 0, False))
        self.stringVar.set("00:00:00,00")
        
        for frame in self.scrollFrame.winfo_children():
            frame.destroy()

    def stopStopWatch(self):
        self.stopped = True
        
        self.changeStatsOfButton(self.stopButton, "Continue", self.saveButton.cget("fg_color"), lambda: self.continueStopWatch())
        self.changeStatsOfButton(self.saveButton, "Restart", self.saveButton.cget("fg_color"), lambda: self.restartStopWatch())
        
    def startStopWatch(self):
        self.inicialDateTime = datetime.datetime.now()
        self.stopped = False
        
        self.changeButtons(True)
        self.after(5, lambda: self.buttonAnimation(0.5, 0.75, 0, True))
        self.beGoingStopWatch()
    
    def beGoingStopWatch(self, addSeconds=0):
        if self.stopped:
            return
        
        currentDateTime = datetime.datetime.now()
        timeDiff = currentDateTime - self.inicialDateTime

        self.totalSeconds = timeDiff.total_seconds() + addSeconds
        
        hours = int(self.totalSeconds // 3600)
        minutes = int((self.totalSeconds % 3600) // 60)
        seconds = int(self.totalSeconds % 60)
        milliseconds = int((self.totalSeconds - int(self.totalSeconds)) * 100)
        
        self.timeText = f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:02d}"
        self.stringVar.set(self.timeText)
        
        self.after(10, lambda: self.beGoingStopWatch(addSeconds))