import tkinter
#gui is only for filedialog so it might be bad
from tkinter import filedialog
import random
import os
import re

MaxX = 512 #max x in editor that i can set without using file so yea 
MaxY = 384 #same as previous
#btw i tested with cs 4 so maybe in other cs this values will be other but i dont care

Filename = None

def Parse(Filename):
    FileLines = []
    with open(Filename,"r") as File:
        for Line in File:
            FileLines.append(Line)

    return FileLines

def SetFile():
    global Filename
    Filename = filedialog.askopenfilename()
    SelectedMapLabel.configure(text=os.path.split(Filename)[1])    

def Shuffle():
    global Filename
    if not Filename:
        StatusLabel.configure(text="No file selected")
        return
    
    DiffName = DiffNameEntry.get()
    if not DiffName:
        StatusLabel.configure(text="Enter diff name")
        return
    
    FileTuple = os.path.split(Filename)
    NewDiffName = re.sub(r"\[.+\]",f"[{DiffName}]",FileTuple[1])

    FileRawData = Parse(Filename)

    HitObjectsStartIndex = FileRawData.index("[HitObjects]\n")
    OnlyHitObjects = FileRawData[FileRawData.index("[HitObjects]\n") + 1:len(FileRawData)]
    for i in range(len(OnlyHitObjects)):
        HitObjectStuff = OnlyHitObjects[i].split(",")
        HitObjectStuff[0] = str(random.randint(0,MaxX))
        HitObjectStuff[1] = str(random.randint(0,MaxY))
        OnlyHitObjects[i] = ",".join(HitObjectStuff)

    NewFileData = FileRawData[0:HitObjectsStartIndex + 1] + OnlyHitObjects
    for line in NewFileData:
        if "Version:" in line:
            NewFileData[NewFileData.index(line)] = f"Version:{DiffName}\n"
            break

    with open(f"{FileTuple[0]}\\{NewDiffName}","w") as file:
        file.writelines(NewFileData)
    StatusLabel.configure(text="success!")
    Filename = None
    SelectedMapLabel.configure(text="")
    

window = tkinter.Tk()
window.title("osu! Shuffler")
try:
    window.iconbitmap("icon.ico")
except:
    pass
window.geometry("500x200")

GetFileButton = tkinter.Button(window,text="Choose file",command=SetFile)
CreateDiffButton = tkinter.Button(window,text="Shuffle!",command=Shuffle)

DiffNameEntry = tkinter.Entry(window,width=25)

DiffNameLabel = tkinter.Label(window,text="Enter diff name")
StatusLabel = tkinter.Label(window,text="")
SelectedMapLabel = tkinter.Label(window,text="")

DiffNameLabel.grid(column=0,row=0)
DiffNameEntry.grid(column=1,row=0)
SelectedMapLabel.place(x=25,y=50)
CreateDiffButton.grid(column=1,row=1)
StatusLabel.grid(column=2,row=1)
GetFileButton.grid(column=0,row=1)


window.mainloop()