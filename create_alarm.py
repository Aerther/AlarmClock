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
        # Variables
        entryCount = 2 # Used as a count of the entry's
        labelFont = ctt.CTkFont(family="Arial", size=16)
        font = ctt.CTkFont(family="Arial", size=50)
        
        # Register the commands
        validateCommandHours = (self.register(lambda input: self.validateInput(input, 23)), "%P")
        validateCommandElse = (self.register(lambda input: self.validateInput(input, 59)), "%P")
        
        # Frame
        self.frame = ctt.CTkFrame(self)
        self.frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        # Labels
        # Labels to indicate minute, hour and reminder
        hourLabel = ctt.CTkLabel(self.frame, text="Hour", font=labelFont)
        hourLabel.place(relx=1/(entryCount+1), rely=0.43, anchor="center")
        
        minuteLabel = ctt.CTkLabel(self.frame, text="Minute", font=labelFont)
        minuteLabel.place(relx=1/(entryCount+1)*2, rely=0.43, anchor="center")
        
        reminderLabel = ctt.CTkLabel(self.frame, text="Reminder", font=labelFont)
        reminderLabel.place(relx=0.28, rely=0.55, anchor="center")
        
        # Label for the separation in the Entry's
        label1 = ctt.CTkLabel(self.frame, text=":", font=font)
        label1.place(relx=0.5, rely=0.3, anchor="center")
        
        # Entry's
        # Hour entry
        self.hourVar = ctt.StringVar(value="00")
        self.hourEntry = ctt.CTkEntry(self.frame, textvariable=self.hourVar, font=font, justify="center",
                                      validate="key", validatecommand=validateCommandHours)
        self.hourEntry.place(relx=1/(entryCount+1), rely=0.3, relheight=0.2, relwidth=0.25, anchor="center")
        
        # Minute entry
        self.minuteVar = ctt.StringVar(value="00")
        self.minuteEntry = ctt.CTkEntry(self.frame, textvariable=self.minuteVar, font=font, justify="center", 
                                        validate="key", validatecommand=validateCommandElse)
        self.minuteEntry.place(relx=1/(entryCount+1)*2, rely=0.3, relheight=0.2, relwidth=0.25, anchor="center")
        
        # Reminder entry
        self.reminderValue = ctt.StringVar(value="")
        reminderEntry = ctt.CTkEntry(self.frame, textvariable=self.reminderValue)
        reminderEntry.place(relx=0.5, rely=0.63, relwidth=0.7, anchor="center")
        
        # Buttons
        # Add button
        addButton = ctt.CTkButton(self.frame, text="Add", command=lambda: self.addToAlarms(self.hourVar.get(), self.minuteVar.get()))
        addButton.place(relx=0.33, rely=0.85, relheight=0.1, relwidth=0.2, anchor="center")
        
        # Cancel button
        cancelButton = ctt.CTkButton(self.frame, text="Cancel", command=lambda: self.appParent.showFrame(self.appParent.alarmsClass))
        cancelButton.place(relx=0.66, rely=0.85, relheight=0.1, relwidth=0.2, anchor="center")
    
    # Check if the input is valid, if it's not the key will not be displayed
    def validateInput(self, input: str, value: int):
        if not input.isdecimal() and input != "":
            return False
        
        if len(input) > 2:
            return False
        
        if input != "":
            if int(input) > value:
                return False
        
        return True
    
    # Check if the alarm is valid
    def isValidAlarm(self, hour: str, minute: str):
        hoursList = [hour for hour in range(24)] # Stores a range of numbers from 0 to 23
        minutesList = [minute for minute in range(60)] # Stores a range of numbers from 0 to 59
        
        isValid = True # Used to see if the alarm is valid
        
        # Check if the hour isn't valid
        if hour not in hoursList:
            text = "Hour is invalid"
            isValid = False
        
        # Check if the minute isn't valid
        if minute not in minutesList:
            text = "Minute is invalid"
            isValid = False
        
        # Check if minute and hour isn't valid
        if minute not in minutesList and hour not in hoursList:
            text = "Hour and minute is invalid"

        if not isValid:
            messageBox.CTkMessagebox.messagebox(title="Invalid", text=text, button_text="OK")
        
        return isValid
    
    # Add the alarm to the alarms list in the app class
    def addToAlarms(self, hour: str, minute: str): 
        # Check if the alarm is valid
        if not self.isValidAlarm(int(hour), int(minute)):
            return
        
        # Used to create the alarm str
        alarm = f"{int(hour):02d}:{int(minute):02d}"
        
        # Check if the alarm is in the alarms
        if alarm not in self.appParent.alarms:
            self.appParent.alarms.append(alarm)
            self.appParent.alarmsToUse.append(alarm)
            self.appParent.showFrame(self.appParent.alarmsClass)
            self.appParent.alarmsClass.createFrameForAlarm(alarm, self.reminderValue.get())
        else:
            messageBox.CTkMessagebox.messagebox(title="Message", text="This alarm already exists", button_text="OK")