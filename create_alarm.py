import customtkinter as ctt
import CustomTkinterMessagebox as messageBox
from functions import *

# Frame Class to create alarms
class CreateAlarm(ctt.CTkFrame):
    def __init__(self, parent: ctt.CTkFrame, appParent): # appParent is an App class type
        # Makes the class have a master parent
        super().__init__(parent)
        
        # Stores the appParent
        self.appParent = appParent
        
        self.createWidgets()
    
    # Creates the widgets
    def createWidgets(self):
        entryCount = 2
        
        self.frame = ctt.CTkFrame(self)
        self.frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        labelFont = ctt.CTkFont(family="Arial", size=16)
        
        hourLabel = ctt.CTkLabel(self.frame, text="Hour", font=labelFont)
        hourLabel.place(relx=1/(entryCount+1), rely=0.43, anchor="center")
        
        minuteLabel = ctt.CTkLabel(self.frame, text="Minute", font=labelFont)
        minuteLabel.place(relx=1/(entryCount+1)*2, rely=0.43, anchor="center")
        
        font = ctt.CTkFont(family="Arial", size=50)
        label1 = ctt.CTkLabel(self.frame, text=":", font=font)
        label1.place(relx=0.5, rely=0.3, anchor="center")
        
        reminderLabel = ctt.CTkLabel(self.frame, text="Reminder", font=labelFont)
        reminderLabel.place(relx=0.28, rely=0.55, anchor="center")
        
        self.reminderValue = ctt.StringVar(value="")
        reminderEntry = ctt.CTkEntry(self.frame, textvariable=self.reminderValue)
        reminderEntry.place(relx=0.5, rely=0.63, relwidth=0.7, anchor="center")
        
        validateCommandHours = (self.register(lambda input: self.validateInput(input, 23)), "%P")
        validateCommandElse = (self.register(lambda input: self.validateInput(input, 59)), "%P")
        
        self.hourVar = ctt.StringVar(value="00")
        self.hourEntry = ctt.CTkEntry(self.frame, textvariable=self.hourVar, font=font, justify="center",
                                      validate="key", validatecommand=validateCommandHours)
        self.hourEntry.place(relx=1/(entryCount+1), rely=0.3, relheight=0.2, relwidth=0.25, anchor="center")
        
        self.minuteVar = ctt.StringVar(value="00")
        self.minuteEntry = ctt.CTkEntry(self.frame, textvariable=self.minuteVar, font=font, justify="center", 
                                        validate="key", validatecommand=validateCommandElse)
        self.minuteEntry.place(relx=1/(entryCount+1)*2, rely=0.3, relheight=0.2, relwidth=0.25, anchor="center")
        
        addButton = ctt.CTkButton(self.frame, text="Add", command=lambda: self.addToAlarms(self.hourVar.get(), self.minuteVar.get()))
        addButton.place(relx=0.33, rely=0.85, relheight=0.1, relwidth=0.2, anchor="center")
        
        cancelButton = ctt.CTkButton(self.frame, text="Cancel", command=lambda: self.appParent.showFrame(self.appParent.alarmsClass))
        cancelButton.place(relx=0.66, rely=0.85, relheight=0.1, relwidth=0.2, anchor="center")
    
    def validateInput(self, input: str, value: int):
        if not input.isdecimal() and input != "":
            return False
        
        if len(input) > 2:
            return False
        
        if input != "":
            if int(input) > value:
                return False
        
        return True
    
    def isValidAlarm(self, hour, minute):
        hoursList = [hour for hour in range(24)]
        minutesList = [minute for minute in range(60)]
        
        entered = False
        if hour not in hoursList:
            text = "Hour is invalid"
            entered = True
        
        if minute not in minutesList:
            text = "Minute is invalid"
            entered = True
        
        if minute not in minutesList and hour not in hoursList:
            text = "Hour and minute is invalid"
            entered = True

        if entered:
            messageBox.CTkMessagebox.messagebox(title="Invalid", text=text, button_text="OK")
        
        return not entered
    
    def addToAlarms(self, hour, minute):    
        if not self.isValidAlarm(int(hour), int(minute)):
            return
        
        alarm = f"{int(hour):02d}:{int(minute):02d}"
        
        if alarm not in self.appParent.alarms:
            self.appParent.alarms.append(alarm)
            self.appParent.alarmsToUse.append(alarm)
            self.appParent.showFrame(self.appParent.alarmsClass)
            self.appParent.alarmsClass.createFrameForAlarm(alarm, self.reminderValue.get())
        else:
            messageBox.CTkMessagebox.messagebox(title="Message", text="This alarm already exists", button_text="OK")