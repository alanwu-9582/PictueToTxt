#Picture-To-txt by XxAlanXDxX
import numpy as np
import cv2
import tkinter as tk
import tkinter.ttk as ttk

output = []

#start
def start():
    global output
    black = int(BlackSenEntry.get())
    gray = int(GraySenEntry.get())
    scales = int(scaleEntry.get())
    texts = textEntry.get()
    
    img = cv2.imread('pic.png')
    height, width, _ = img.shape
    
    output = []
    start = False
    
    for i in range(0, height, scales): #read pixel
        ostr = ""
        for j in range(0, width, scales):
            if img[i, j].sum() < black:
                ostr += texts
            
            elif img[i, j].sum() < gray :
                ostr += texts[0]

                for k in range(len(texts) - 1):
                    ostr += " "

            else:
                for k in range(len(texts)):
                    ostr += " "
                
        if start == False:
            for j in ostr:
                if j != " ":
                    start = True
                    break
                
        if start == True:
            ostr += "\n"
            output.append(ostr)

    hint.config(text = "Done!")
    textOutput(output)

#output
def textOutput(output):
    file = open('output.txt', 'w')
    file.writelines(output)
    file.close()

#save
def save():
    name = fileNameEntry.get()
    if name != "":
        savefrom = open('output.txt', 'r')
        saveto = open('./saves/' + name + '.txt', 'w')

        for line in savefrom:
            saveto.write(line)
            
        hint.config(text = name + ".txt Saved successfully!")
        fileNameVar.set('')
        
        fileName.config(fg = "#000000", text = "Filename") 
        savefrom.close()
        saveto.close()

    else:
        hint.config(text = "Please enter filename")
        fileName.config(fg = "#db818d",  text = "*Filename*") 

#Auto adjust value
def autoAdjustVal():
    img = cv2.imread('pic.png')
    height, width, _ = img.shape

    scales = int(scaleEntry.get())

    Min = 1000
    Max = -1

    for i in range(0, height, scales):
        for j in range(0, width, scales):
            if img[i, j].sum() < Min:
                Min = img[i, j].sum()
            
            elif img[i, j].sum() > Max:
                Max = img[i, j].sum()

    if Min > 100:
        val = str(int((Min + 10) * 2.7))

    elif int((Min + 10) * 15.7) > 350:
        val = "350"
    
    else:
        val = str(int((Min + 10) * 15.4))
    
    BlackSenVar.set(val)
    GraySenVar.set(str(int((Max - (Min * 0.2)) * 0.815)))

    hint.config(text = "Set to [" + val + ", " + str(int((Max - (Min * 0.2)) * 0.815)) + "]")

#os
import os
def openFolder():
    hint.config(text = "PictureToTextBot v1.1")
    os.startfile('output.txt')

def opfile():
    hint.config(text = "PictureToTextBot v1.1")
    os.startfile('saves')

#pillow 
from PIL import Image, ImageGrab
def clipBoard(): #load from ClipBoard
    im = ImageGrab.grabclipboard()
    if isinstance(im, Image.Image):
        im.save('./pic.png')

        img = cv2.imread('pic.png')
        height, width, _ = img.shape

        hint.config(text = "Loaded successfully! (size " + str(width) + "*" + str(height) + ")")

    else:
        hint.config(text = "Something Error!")
        
#win
win = tk.Tk() 
win.geometry('350x230')
win.title("PictureToTxt v1.1")
win.iconbitmap('.\icons\PictureToText.ico')
win.config(bg="#eeeeee", padx = 5, pady = 5)

#frame
Hintframe = tk.Frame(win)
Hintframe.pack(padx = 5, pady = 5) 
frame = tk.Frame(win)
frame.pack(padx = 5, pady = 5) 
frame1 = tk.Frame(win)
frame1.pack(padx = 5, pady = 5)
Imgframe = tk.Frame(win)
Imgframe.pack(padx = 5, pady = 5)

#hint
hint = tk.Label(Hintframe, bg="#dddddd", font = "System 15", text = "PictureToTextBot v1.1")
hint.config(width = 30) 
hint.grid(row = 0, column = 0)

#BlackValue
BlackSenVar = tk.StringVar()
BlackSenEntry = tk.Entry(frame, bg="#ffffff", textvariable = BlackSenVar, font = "System 12", borderwidth = 1)
BlackSenEntry.config(width = 10) 
BlackSenEntry.insert(0, "250")
BlackSenEntry.grid(row = 0, column = 1)

sen = tk.Label(frame, bg="#eeeeee", font = "System 12", text = "BlackValue")
sen.config(width = 15) 
sen.grid(row = 0, column = 0)

#GrayValue
GraySenVar = tk.StringVar()
GraySenEntry = tk.Entry(frame, bg="#ffffff", textvariable = GraySenVar, font = "System 12", borderwidth = 1)
GraySenEntry.config(width = 10) 
GraySenEntry.insert(0, "-1")
GraySenEntry.grid(row = 1, column = 1)

Graysen = tk.Label(frame, bg="#eeeeee", font = "System 12", text = "GrayValue")
Graysen.config(width = 15) 
Graysen.grid(row = 1, column = 0)

#DisplayedTexts
textEntry = tk.Entry(frame, bg="#ffffff", font = "System 12", borderwidth = 1)
textEntry.config(width = 10) 
textEntry.insert(0, "87")
textEntry.grid(row = 2, column = 1)

text = tk.Label(frame, bg="#eeeeee", font = "System 12", text = "DisplayedTexts")
text.config(width = 15) 
text.grid(row = 2, column = 0)

#ReductionAmount
scaleEntry = tk.Entry(frame, bg="#ffffff", font = "System 12", borderwidth = 1)
scaleEntry.config(width = 10) 
scaleEntry.insert(0, "2")
scaleEntry.grid(row = 3, column = 1)

scale = tk.Label(frame, bg="#eeeeee", font = "System 12", text = "ReductionAmount")
scale.config(width = 15) 
scale.grid(row = 3, column = 0)

#Filename
fileNameVar = tk.StringVar()
fileNameEntry = tk.Entry(frame, bg="#ffffff", textvariable = fileNameVar, font = "System 12", borderwidth = 1)
fileNameEntry.config(width = 10) 
fileNameEntry.insert(0, "")
fileNameEntry.grid(row = 4, column = 1)

fileName = tk.Label(frame, bg="#eeeeee", font = "System 12", text = "Filename")
fileName.config(width = 15) 
fileName.grid(row = 4, column = 0)

#buttons
btnLoad = ttk.Button(frame1, text = "ClipBoard", command = clipBoard)
btnLoad.grid(row = 0, column = 0)
btnStart = ttk.Button(frame1, text = "Start", command = start)
btnStart.grid(row = 0, column = 1)
btnOutput = ttk.Button(frame1, text = "ShowResult", command = openFolder)
btnOutput.grid(row = 0, column = 2)
btnAuto = ttk.Button(frame1, text = "AdjustValue", command = autoAdjustVal)
btnAuto.grid(row = 1, column = 0)

btnSave = ttk.Button(frame1, text = "Save", command = save)
btnSave.grid(row = 1, column = 1)
btnFile = ttk.Button(frame1, text = "OpenFolder", command = opfile)
btnFile.grid(row = 1, column = 2)

#repeat
win.mainloop()

