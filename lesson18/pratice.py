'''
學習Canvas
'''
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class Window(tk.Tk):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)        
        self.title("Image")
        self.geometry("300x250")
        self.configure(background='#E79460')

class MyFrame(tk.Frame):
    def __init__(self,master,**kwargs):
        super().__init__(master,**kwargs)
        self.configure(background='#9E7A7A')
        self.img = Image.open("requests.jpg")
        self.pets = ImageTk.PhotoImage(self.img)
        canvas = tk.Canvas(self,
                           width=150,
                           height=180
                           )
        canvas.create_image(75,50,image=self.pets,anchor=tk.CENTER)
        canvas.pack()
        self.pack(expand=1, fill='both')


def main():    
    window = Window()
    myFrame = MyFrame(window)
    window.mainloop()

if __name__ == "__main__":
    main()