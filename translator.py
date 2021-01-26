from tkinter import Tk, Frame, Text
from tkinter import ttk
import re

# Base cases for English-to-Morse and Morse-to-English
E2M = { 'A': '.-',     'B': '-...',   'C': '-.-.', 
        'D': '-..',    'E': '.',      'F': '..-.',
        'G': '--.',    'H': '....',   'I': '..',
        'J': '.---',   'K': '-.-',    'L': '.-..',
        'M': '--',     'N': '-.',     'O': '---',
        'P': '.--.',   'Q': '--.-',   'R': '.-.',
        'S': '...',    'T': '-',      'U': '..-',
        'V': '...-',   'W': '.--',    'X': '-..-',
        'Y': '-.--',   'Z': '--..',

        '0': '-----',  '1': '.----',  '2': '..---',
        '3': '...--',  '4': '....-',  '5': '.....',
        '6': '-....',  '7': '--...',  '8': '---..',
        '9': '----.',  ' ': '/'
        }

M2E = {value: key for key, value in E2M.items()}

# Helper functions
def to_morse(s):
    return " ".join(E2M.get(i.upper()) for i in s)


def from_morse(s):
    return "".join(M2E.get(i) for i in s.split())


class MorseTranslator(Frame):
    """ Morse code translator class """

    def __init__(self, master):
        super().__init__(master)
        self.windowSettings(master)
        self.mainMenu()
        self.pack()

    def windowSettings(self, master):
        """ Set the main window settings """
        self.master.geometry("930x250")
        self.master.title("Morse Code Translator")
        self.master.configure(bg="#2b2b2b")

        self.configure(
            bg="#2b2b2b",
            highlightbackground="#2b2b2b",
            highlightcolor="#2b2b2b",
            highlightthickness=5,
        )

        self.master.resizable(False, False)
        self.master.grid_propagate(False)
        self.master.pack_propagate(False)

    def mainMenu(self):
        """ Create and grid the main frame widgets """

        #                           Style configuration
        # ---------------------------------------------------------------------
        style = ttk.Style()

        style.theme_use("alt")
        style.configure(
            "TButton",
            width=15,
            relief="flat",
            background="#deaf9d",
            foreground="#2b2b2b",
            fieldbackground="#2b2b2b",
        )

        style.map("TButton", background=[("active", "#ba9384")])

        #                           Widgets
        # ---------------------------------------------------------------------
        translate = ttk.Button(self, text="Translate", command=self._translate)

        swap = ttk.Button(self, text="Swap", command=self._swap)
        # ---------------------------------------------------------------------

        #                           Text boxes
        # ---------------------------------------------------------------------
        self.box1 = Text(
            self,
            fg="#deaf9d",
            background="#4d4747",
            font=("monospace", 11),
            highlightbackground="#2b2b2b",
            highlightcolor="#4d4747",
            bd=0,
            highlightthickness=10,
            width=20,
            height=8,
            wrap="word",
            insertbackground="#deaf9d",
            selectbackground="#deaf9d",
        )

        self.box2 = Text(
            self,
            fg="#deaf9d",
            background="#4d4747",
            font=("monospace", 11),
            highlightcolor="#4d4747",
            highlightbackground="#2b2b2b",
            bd=0,
            highlightthickness=10,
            width=20,
            height=8,
            wrap="word",
            insertbackground="#deaf9d",
            selectbackground="#deaf9d",
        )
        # ---------------------------------------------------------------------

        #                   Place the widgets in the grid
        # --------------------------------------------------------------------
        self.box1.grid(row=1, column=0, sticky="WENS", ipadx=50, pady=15)
        self.box2.grid(row=1, column=3, sticky="WENS", ipadx=50, pady=15)

        translate.grid(row=1, column=1, ipadx=10, padx=5)
        swap.grid(row=1, column=2, ipadx=10, padx=5)
        # --------------------------------------------------------------------

        #                   Widget bindings
        # --------------------------------------------------------------------
        #                   Translate on <CR>
        self.box1.bind("<Return>", lambda x: self._translate())

        #                   Empty the text box on Delete
        self.box1.bind("<Delete>", lambda x: self.box1.delete('1.0', 'end'))
        self.box2.bind("<Delete>", lambda x: self.box2.delete('1.0', 'end'))


    def _swap(self):
        """ Swap the content of the text boxes """

        _text1 = self.box1.get("1.0", "end").strip("\n")
        _text2 = self.box2.get("1.0", "end").strip("\n")

        self.box1.delete("1.0", "end")
        self.box1.insert("1.0", _text2)

        self.box2.delete("1.0", "end")
        self.box2.insert("1.0", _text1)

    def _translate(self):
        """ Translate the contents of the left box(box1) to the opposite language """

        # Remove new lines, replaces new line characters to make them behave like spaces
        # .strip() will only remove the new lines at the end/beginning of a string 
        # but not the ones in between.
        _text1 = self.box1.get("1.0", "end").strip("\n").replace('\n', ' ')

        # print(repr(_text1))

        # Regex to remove spaces if the string is in English:
        # Only used in case we don't want to use / for spaces

        # _text1 = _text1.replace(" ", "") if re.search("[a-zA-Z]+", _text1) else _text1

        try:
            translation =  to_morse(_text1) if re.search("[a-zA-Z]+", _text1) \
                else from_morse(_text1)

            self.box2.delete("1.0", "end")
            self.box2.insert("1.0", translation)
            
        except:
            print("We're sorry. The text you entered could not be processed.")

