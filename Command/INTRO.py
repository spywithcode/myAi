import time
from tkinter import *                           #pip install tkinter
from pygame import mixer
from PIL import Image,ImageTk,ImageSequence     #pip install Pillow

mixer.init()
root = Tk()
root.geometry("1000x500")

def play_gif():
    root.lift()
    root.attributes("-topmost",True)
    global img
    img = Image.open("C:\\Users\\mrsan\\OneDrive\\Desktop\\myAi\\Command\\ironsnap2.gif")
    lbl = Label(root)
    lbl.place(x=0,y=0)
    i=0
    mixer.music.load("C:\\Users\\mrsan\\OneDrive\\Desktop\\myAi\\Command\\Startup.mp3")
    mixer.music.play()
    
    for img in ImageSequence.Iterator(img):
        img = img.resize((1000,500))
        img = ImageTk.PhotoImage(img)
        lbl.config(image=img)
        root.update()
        time.sleep(0.05)
    root.destroy()

# play_gif()
# root.mainloop()