import customtkinter as ctt
import CustomTkinterMessagebox as messageBox
import datetime

from timer import *
from stop_watch import *
from create_alarm import *
from alarms import *
from functions import *

# Main app class that handles different features like alarms, timer, and stopwatch.
class App(ctt.CTk):
    def __init__(self, title: str, size: tuple[int], resizable: tuple[bool], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title(title)
        self.resizable(resizable[0], resizable[1])
        
        # Set the window to appear in the middle of the screen
        self.geometry(f"{size[0]}x{size[1]}+{self.winfo_screenwidth()//2-size[0]//2}+{self.winfo_screenheight()//2-size[1]//2}")
        
        # Used for the alarms
        self.alarms: str = [] # List to store all of the alarms
        
        # List of active alarms
        # The infinite is just for it to be going infinite, as it's not an alarm
        self.alarmsToUse: str = ["infinite"] 
        
        # Creates all the screen changeable frames
        self.alarmsClass = Alarms(self.changeFrame, self)
        self.createAlarms = CreateAlarm(self.changeFrame, self)
        self.timerClass = Timer(self.changeFrame, self)
        self.stopWatchClass = StopWatch(self.changeFrame, self)
        
        # Makes a list for all the frames
        self.framesList: list[ctt.CTkFrame] = [self.alarmsClass, self.createAlarms, self.timerClass, self.stopWatchClass]
        self.index = 0 # Used to get the current frame being displayed
        
        self.createWidgets()
        self.continuousCountingAlarm()
        
        # Will show the initial frame
        self.showFrame(self.alarmsClass)
    
    # Creates the widgets
    def createWidgets(self):
        # This variables will be used to make the buttons in the Menu Frame equal in every aspect
        buttonsCount: int = 3 # How many buttons are in the menu
        buttonWidth: float = int(1/(buttonsCount+1)*10)/10  # 1/(buttonsCount+1) is the space between the buttons, the rest is just to make it look better
        buttonsHeight: float = 0.4 # The height of the buttons
        relxForButtons: float = 1/(buttonsCount+1) # Positions of the buttons, so they are equally spaced, just like 'space-around' in CSS
        
        # The frame that contains the content that can be switched between different screens
        self.changeFrame = ctt.CTkFrame(self)
        self.changeFrame.place(relx=0, rely=0, relwidth=1, relheight=0.8)

        # Menu frame containing navigation buttons for switching between features (Alarms, Timer, Stopwatch)
        menuFrame = ctt.CTkFrame(self)
        menuFrame.place(relx=0, rely=0.8, relwidth=1, relheight=0.2)
        
        # Simulates a white border as CustomTkinter does not support single-side borders
        simulateBorder = ctt.CTkCanvas(menuFrame, bg="White", highlightthickness=0)
        simulateBorder.place(relx=0, rely=0, relwidth=1, relheight=0.01, anchor="nw")
        
        # Creates the alarms button
        alarmsButton = ctt.CTkButton(menuFrame, text="Alarms", command=lambda: self.showFrame(self.alarmsClass))
        alarmsButton.place(relx=relxForButtons, rely=0.5, relwidth=buttonWidth, relheight=buttonsHeight, anchor="center")
        
        # Creates the timer button
        timerButton = ctt.CTkButton(menuFrame, text="Timer", command=lambda: self.showFrame(self.timerClass))
        timerButton.place(relx=relxForButtons*2, rely=0.5, relwidth=buttonWidth, relheight=buttonsHeight, anchor="center")
        
        # Creates the stopwatch button
        stopWatchButton = ctt.CTkButton(menuFrame, text="Stop Watch", command=lambda: self.showFrame(self.stopWatchClass))
        stopWatchButton.place(relx=relxForButtons*3, rely=0.5, relwidth=buttonWidth, relheight=buttonsHeight, anchor="center")

    # Changes the frame that appear in the changeFrame
    def showFrame(self, frameToGo: ctt.CTkFrame):
        # Removes the last frame used
        self.framesList[self.index].forget()
        
        # Puts the new frame
        frameToGo.pack(fill="both", expand=True)
        frameToGo.tkraise()
        
        # Change the index to be the current frame, which is frameToGo
        for i, frame in enumerate(self.framesList):
            if frame == frameToGo:
                self.index = i
    
    # Continuously checks if the current time matches any active alarm time
    # Runs indefinitely until the program is closed
    def continuousCountingAlarm(self):
        # Get the current time
        currentTime: datetime.datetime = datetime.datetime.now()
        
        # Make an alarm with the current time
        currentAlarm: str = f"{currentTime.hour:02d}:{currentTime.minute:02d}"
        
        for alarm in self.alarmsToUse:
            if alarm == currentAlarm:
                messageBox.CTkMessagebox.messagebox(title="Alarm", text=f"{alarm}")
                playSound(getPathFile("Sound", "sound.wav"))
        
        # Adjusts the next check time so the function is called at the start of the next minute
        subtractTime: int = (currentTime.second * 1000) # Converts to milliseconds
        
        # Call the function again after 60000 milliseconds, which is 1 minute
        self.after(60000-subtractTime, self.continuosCountingAlarm)