#!/usr/bin/env python3.6
from translator import MorseTranslator, Tk
from tkinter import Image

if __name__ == "__main__":

    root = Tk()

    img = Image('photo', file=r'icon.png')
    root.tk.call('wm','iconphoto', root._w, img)

    root.attributes('-topmost', True)
    app = MorseTranslator(master=root)
    app.mainloop()
