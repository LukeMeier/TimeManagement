import ctypes
from hashlib import new
from multiprocessing.connection import wait
from re import I
import keyboard
import datetime
import time

def writetext(text):
    datei = open("./timemanage.txt", "a")
    datei.write(text)
    datei.write("\n")
    datei.close()

aktuelles_datum = datetime.date.today()
formatiertes_datum = aktuelles_datum.strftime("%d.%m.%Y")
workingday = 0

def on_unlock():
    aktuelle_zeit = datetime.datetime.now()
    formatierte_zeit = aktuelle_zeit.strftime("%H:%M")
    writetext(formatierte_zeit)
    print("Der PC wurde entsperrt!")
    

def on_lock():
    aktuelle_zeit = datetime.datetime.now()
    formatierte_zeit = aktuelle_zeit.strftime("%H:%M")
    writetext(formatierte_zeit)
    print("Der Pc wurde gespeert!")

def is_locked():
    user32 = ctypes.windll.User32
    return user32.GetForegroundWindow() == 0

locked = is_locked()

def on_key_press(event):
    global newlock
    global locked
    if event.event_type == 'down' and event.name == 'linke windows' and locked == False :
        on_lock()
        locked = True
        keyboard.unhook(on_key_press)
        newlock = True
    elif event.event_type == 'down' and event.name == 'l':
        locked
        keyboard.unhook(on_key_press)
    else:
        locked = False
        keyboard.unhook(on_key_press)

if __name__ == "__main__":
    newlock = True
    aktuelle_zeit = datetime.datetime.now().strftime("%H:%M:%S")

    while True:
        
        #überprüft ob noch der gleiche Tag ist
        if  formatiertes_datum != datetime.datetime.today().strftime("%d.%m.%Y") or workingday == 0:
            formatiertes_datum = datetime.datetime.today().strftime("%d.%m.%Y")
            writetext(formatiertes_datum)
            workingday = 1

        if aktuelle_zeit != datetime.datetime.now().strftime("%H:%M:%S"):

            #löst aus wenn der Pc entspeert wird
            if locked == False and newlock == True:
                on_unlock()
                locked = False
                newlock = False
            
            #löst aus wenn der PC gespeert wird
            keyboard.hook(on_key_press)
            aktuelle_zeit = datetime.datetime.now().strftime("%H:%M:%S")
            time.sleep(1)
