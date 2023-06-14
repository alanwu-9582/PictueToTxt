import numpy as np
import cv2
import tkinter as tk
import tkinter.ttk as ttk
import os
from PIL import Image, ImageGrab
import threading

import json
with open('./options.json', 'r', encoding="utf8") as jfile:
  options = json.load(jfile)


ENCODING = options['ENCODING']
ASCII_CHARS = options['ASCII_CHARS']
DEFULT_REPLACEMENT = options['DEFULT_REPLACEMENT']

class PNG2TEXTGUI():
    def __init__(self, master):
        self.m_img = m_image(cv2.imread('./assets/image.png'))
        self.is_progressing = False

        self.master = master 
        self.master.geometry('620x200')
        self.master.title("PNG2TEXT")
        self.master.config(bg="#eeeeee", padx = 5, pady = 5)

        #Left
        self.left_frame = tk.Frame(self.master)
        self.left_frame.grid(row=0, column=0, padx=5, pady=5)
        
        #Left_Top
        self.left_top_frame = tk.Frame(self.left_frame)
        self.left_top_frame.grid(row=0, column=0, padx=5, pady=1)

        self.DarkValue = tk.StringVar()
        Spinbox = tk.Spinbox(self.left_top_frame, from_=1, to=765, textvariable=self.DarkValue, wrap = True, increment=50)
        Spinbox.config(width = 5, bg="#ffffff", font = "System 12")
        Spinbox.grid(row = 0, column = 1, padx = 1)
        self.DarkValue.set("350")
 

        self.BrightValue = tk.StringVar()
        Spinbox = tk.Spinbox(self.left_top_frame, from_=1, to=765, textvariable=self.BrightValue, increment=50)
        Spinbox.config(width = 5, bg="#ffffff", font = "System 12")
        Spinbox.grid(row = 0, column = 2, padx = 1)
        self.BrightValue.set("550")

        Label = tk.Label(self.left_top_frame, bg="#eeeeee", font = "System 12", text = "亮度值 [深, 淺]")
        Label.config(width = 15) 
        Label.grid(row = 0, column = 0)

        self.WidthObscure = tk.StringVar()
        Spinbox = tk.Spinbox(self.left_top_frame, from_=1, to=10, textvariable=self.WidthObscure)
        Spinbox.config(width = 5, bg="#ffffff", font = "System 12")
        Spinbox.grid(row = 1, column = 1, padx = 1)
        self.WidthObscure.set("1")

        self.HeightObscure = tk.StringVar()
        Spinbox = tk.Spinbox(self.left_top_frame, from_=1, to=10, textvariable=self.HeightObscure)
        Spinbox.config(width = 5, bg="#ffffff", font = "System 12")
        Spinbox.grid(row = 1, column = 2, padx = 1)
        self.HeightObscure.set("1")

        Label = tk.Label(self.left_top_frame, bg="#eeeeee", font = "System 12", text = "壓縮量 [寬, 高]")
        Label.config(width = 15) 
        Label.grid(row = 1, column = 0)

        #Left_Middle
        self.left_middle_frame = tk.Frame(self.left_frame)
        self.left_middle_frame.grid(row=1, column=0, padx=5, pady=1)

        self.Scale = tk.StringVar()
        Spinbox = tk.Spinbox(self.left_middle_frame, from_=1, to=300, textvariable=self.Scale, increment=10)
        Spinbox.config(width = 10)
        Spinbox.grid(row = 0, column = 1)
        self.Scale.set("100")

        Label = tk.Label(self.left_middle_frame, bg="#eeeeee", font = "System 12", text = "縮放值 (%)")
        Label.config(width = 15) 
        Label.grid(row = 0, column = 0)

        self.replacement = tk.StringVar()
        Entry = tk.Entry(self.left_middle_frame, bg="#ffffff", textvariable = self.replacement, font = "System 12", borderwidth = 1)
        Entry.config(width = 10) 
        self.replacement.set(DEFULT_REPLACEMENT)
        Entry.grid(row = 1, column = 1)

        Label = tk.Label(self.left_middle_frame, bg="#eeeeee", font = "System 12", text = "顯示文字")
        Label.config(width = 15) 
        Label.grid(row = 1, column = 0)

        self.fileName = tk.StringVar()
        Entry = tk.Entry(self.left_middle_frame, bg="#ffffff", textvariable = self.fileName, font = "System 12", borderwidth = 1)
        Entry.config(width = 10) 
        self.fileName.set("")
        Entry.grid(row = 2, column = 1)

        Label = tk.Label(self.left_middle_frame, bg="#eeeeee", font = "System 12", text = "存檔檔名")
        Label.config(width = 15) 
        Label.grid(row = 2, column = 0)

        #Left_Bottom
        self.left_bottom_frame = tk.Frame(self.left_frame)
        self.left_bottom_frame.grid(row=2, column=0, padx=5, pady=5)

        Button_width = 8
        Button = ttk.Button(self.left_bottom_frame, text = "剪貼簿", width = Button_width, command = self.clipBoard)
        Button.grid(row = 0, column = 0)

        Button = ttk.Button(self.left_bottom_frame, text = "調整數值", width = Button_width, command = self.autoAdjustValue)
        Button.grid(row = 0, column = 1)

        Button = ttk.Button(self.left_bottom_frame, text = "執行", width = Button_width, command = self.start)
        Button.grid(row = 0, column = 2)

        self.UseASCII = tk.BooleanVar()
        Checkbutton = ttk.Checkbutton(self.left_bottom_frame, text='ASCII', variable=self.UseASCII)
        Checkbutton.grid(row = 0, column = 3)

        Button = ttk.Button(self.left_bottom_frame, text = "顯示結果", width = Button_width, command = self.showResult)
        Button.grid(row = 1, column = 0)

        Button = ttk.Button(self.left_bottom_frame, text = "資料夾", width = Button_width, command = self.showFolder)
        Button.grid(row = 1, column = 1)

        Button = ttk.Button(self.left_bottom_frame, text = "儲存輸出", width = Button_width, command = self.saveResult)
        Button.grid(row = 1, column = 2)

        Button = ttk.Button(self.left_bottom_frame, text = "重載圖片", width = Button_width, command = self.refresh)
        Button.grid(row = 1, column = 3)

        #Middle
        self.middle_frame = tk.Frame(self.master)
        self.middle_frame.grid(row=0, column=1, padx=10, pady=5)

        self.log = tk.Text(self.middle_frame, width=35, height=10, font=("System", 10))
        self.log.grid(pady=5, columnspan=40)
        self.log_count = 0

        # #Right
        # self.right_frame = tk.Frame(self.master)
        # self.right_frame.grid(row=0, column=2, padx=10, pady=5)

    def updateLog(self, arg:str):
        if self.log_count >= 10:
            self.log.delete("1.0", "end")
            self.log_count = 0

        self.log.insert("end", f"{arg}\n")
        self.log_count += 1

    def clipBoard(self):
        im = ImageGrab.grabclipboard()
        if isinstance(im, Image.Image):
            im.save('./assets/image.png')
            self.m_img = m_image(cv2.imread('./assets/image.png'))
            self.updateLog(f"載入成功! (圖片大小{self.m_img.width}, {self.m_img.height})")

        else:
            self.updateLog(f"剪貼簿讀取失敗!")

    def autoAdjustValue(self):
        dark_value, bright_value = self.m_img.calculateValue()
        self.DarkValue.set(str(dark_value))
        self.BrightValue.set(str(bright_value))
        self.updateLog(f"亮度值調整為 {dark_value} {bright_value}")

    def getNextText(self, replace_text, flag, repeat_times):
        next_text = ""
        for i in range(repeat_times):
            if flag >= len(replace_text):
                flag = 0

            next_text += replace_text[flag]
            flag += 1

        return next_text, flag

    def PNG2TEXT(self, img):
        replace_text = self.replacement.get()
        dark_value = int(self.DarkValue.get())
        bright_value = int(self.BrightValue.get())
        width_obscure = int(self.WidthObscure.get())
        height_obscure = int(self.HeightObscure.get())
        height, width, _ = img.shape

        flag = 0
        self.output = []

        height_obscure = height_obscure if height_obscure in range(1, height) else 1
        width_obscure = width_obscure if width_obscure in range(1, width) else 1

        for i in range(0, height, height_obscure):
            Line = ""
            for j in range(0, width, width_obscure):
                self.master.update()
                pixel_sum = img[i, j].sum()
                if pixel_sum < dark_value:
                    next_text, flag = self.getNextText(replace_text, flag, 2)
                    Line += next_text
                elif pixel_sum < bright_value:
                    next_text, flag = self.getNextText(replace_text, flag, 1)
                    Line += next_text + " "
                else:
                    Line += "  "

            Line += "\n"
            self.output.append(Line)

    def PNG2ASCII(self, img):
        width_obscure = int(self.WidthObscure.get())
        height_obscure = int(self.HeightObscure.get())
        height, width, _ = img.shape

        partitionValue = self.m_img.sorted_pixelsSum[int((self.m_img.height*self.m_img.width) / len(ASCII_CHARS))+1]

        self.output = []

        height_obscure = height_obscure if height_obscure in range(1, height) else 1
        width_obscure = width_obscure if width_obscure in range(1, width) else 1

        for i in range(0, height, height_obscure):
            Line = ""
            for j in range(0, width, width_obscure):
                self.master.update()
                ASCII_index = int(img[i, j].sum() / partitionValue)
                Line += ASCII_CHARS[ASCII_index if ASCII_index < len(ASCII_CHARS) else len(ASCII_CHARS)-1]

            Line += "\n"
            self.output.append(Line)

    def start(self):
        if not self.is_progressing and not self.m_img.is_progressing:
            self.is_progressing = True

            new_size = int(self.Scale.get())
            if new_size != 100:
                new_size /= 100
                img = cv2.resize(self.m_img.image, (int(self.m_img.width * new_size), int(self.m_img.height * new_size)))
            else:
                img = self.m_img.image

            UseASCII = self.UseASCII.get()

            self.updateLog(f'開始執行.. ({["Text","ASCII"][UseASCII]})')
            if UseASCII:
                self.PNG2ASCII(img)
            else:
                self.PNG2TEXT(img)

            with open('output.txt', 'w', encoding=ENCODING) as file:
                file.writelines(self.output)

            self.updateLog(f"執行成功!")
            self.is_progressing = False
        else:
            self.updateLog(f"目前正在執行中..")

    def showResult(self):
        os.startfile('output.txt')

    def showFolder(self):
        os.startfile('saves')

    def saveResult(self):
        name = self.fileName.get()
        if name != "":
            with open('output.txt', 'r', encoding=ENCODING) as savefrom, open(f'saves/{name}.txt', 'w', encoding=ENCODING) as saveto:
                for line in savefrom:
                    saveto.write(line)
            self.updateLog(f"儲存為 {name}.txt")
            self.fileName.set('')

        else:
            self.updateLog(f"請輸入檔名")

    def refresh(self):
        self.m_img = m_image(cv2.imread('./assets/image.png'))
        self.updateLog(f"載入成功! (圖片大小{self.m_img.width}, {self.m_img.height})")

class m_image:
    def __init__(self, src):
        self.image = src
        self.height, self.width, _ = self.image.shape
        self.pixelsSum = []

        startcalculateSum = threading.Thread(target=self.calculateSum)
        startcalculateSum.start()

    def calculateSum(self):
        self.is_progressing = True
        width, height = self.width, self.height
        for i in range(height):
            for j in range(width):
                self.pixelsSum.append(self.image[i, j].sum())

        self.sorted_pixelsSum = sorted(self.pixelsSum)
        self.is_progressing = False

    def calculateValue(self):
        splitIndex = len(self.sorted_pixelsSum) // 3
        return self.sorted_pixelsSum[splitIndex], self.sorted_pixelsSum[splitIndex*2]   

if __name__ == "__main__":
    root = tk.Tk()
    gui = PNG2TEXTGUI(root)
    root.mainloop()
