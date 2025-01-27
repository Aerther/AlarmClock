import time
import datetime 
import customtkinter as ctt

class App(ctt.CTk):
    def __init__(self, title, size, resizable, *args, **kwargs):
        super().__init__(*args, **kwargs)
        ctt.set_appearance_mode("dark")
        
        self.title(title)
        self.resizable(resizable[0], resizable[1])
        self.geometry(f"{size[0]}x{size[1]}")
        self.minsize(size[0], size[1])
        self.createWidgets()
    
    def createWidgets(self):
        hours = [str(hour) for hour in range(24)]
        time60 = [str(time) for time in range(60)]
        
        # relwidth relheigth
        # Button to start the count
        buttonStart = ctt.CTkButton(self, text="Start Alarm", width=100, height=30, command=lambda: self.startAlarm(comboHours.get(), comboMinutes.get(), comboSeconds.get()))
        buttonStart.place(relx=0.4, rely=0.7)
        
        # For Hours
        labelHours = ctt.CTkLabel(self, text="Hours")
        labelHours.place(relx=0.1, rely=0.12)

        comboHours = ctt.CTkComboBox(self, values=hours, width=100)
        comboHours.place(relx=0.1, rely=0.2)
        
        # For Minutes
        labelMinutes = ctt.CTkLabel(self, text="Minutes")
        labelMinutes.place(relx=0.4, rely=0.12)

        comboMinutes = ctt.CTkComboBox(self, values=time60, width=100)
        comboMinutes.place(relx=0.4, rely=0.2)
        
        # For Seconds
        labelSeconds = ctt.CTkLabel(self, text="Seconds")
        labelSeconds.place(relx=0.7, rely=0.12)

        comboSeconds = ctt.CTkComboBox(self, values=time60, width=100)
        comboSeconds.place(relx=0.7, rely=0.2)
        
        # Setting all the inicial numbers to 0
        comboHours.set(value="0")
        comboMinutes.set(value="0")
        comboSeconds.set(value="0")
        
        # Setting the events for invalid input
        comboHours.bind("<KeyRelease>", lambda event, combobox=comboHours: self.validateInput(combobox))
        comboMinutes.bind("<KeyRelease>", lambda event, combobox=comboMinutes: self.validateInput(combobox))
        comboSeconds.bind("<KeyRelease>", lambda event, combobox=comboSeconds: self.validateInput(combobox))
    
    def startAlarm(self, hours, minutes, seconds):
        self.checkAlarmTime(int(hours), int(minutes), int(seconds))
    
    def checkAlarmTime(self, hours, minutes, seconds):
        actualTime = datetime.datetime.now()

        if actualTime.hour == hours and actualTime.minute == minutes and actualTime.second == seconds:
            print("Teste")
        else:
            print(f"{actualTime.hour}, {actualTime.minute}, {actualTime.second}")
            self.after(1000, self.checkAlarmTime, hours, minutes, seconds)
    
    def validateInput(self, combobox: ctt.CTkComboBox):
        if combobox.get() not in combobox._values:
            combobox.set(value="")
        

app = App(title="Alarm Clock", size=(600, 300), resizable=(True, True))
app.mainloop()