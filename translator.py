from tkinter import Tk, Frame, Text, Label
from tkinter import ttk
import re
from utils.playSound import PlaySound


class MorseTranslator(Frame):
    """ Morse code translator class """

    # Base cases for English-to-Morse and Morse-to-English
    E2M = { "A": ".-", "B": "-...", "C": "-.-.", "D": "-..", "E": ".",
        "F": "..-.", "G": "--.", "H": "....", "I": "..", "J": ".---",
        "K": "-.-", "L": ".-..", "M": "--", "N": "-.", "O": "---", "P": ".--.",
        "Q": "--.-", "R": ".-.", "S": "...", "T": "-", "U": "..-", "V": "...-",
        "W": ".--", "X": "-..-", "Y": "-.--", "Z": "--..", "0": "-----",
        "1": ".----", "2": "..---", "3": "...--", "4": "....-", "5": ".....",
        "6": "-....", "7": "--...", "8": "---..", "9": "----.", " ": "/",
    }

    M2E = {value: key for key, value in E2M.items()}

    def __init__(self, master):
        """ Initialize properties """
        super().__init__(master)
        self.windowSettings(master)
        self.mainMenu()
        self.player = PlaySound()
        self.playingid = None
        self.pack()

    def windowSettings(self, master):
        """ Set the main window settings """
        self.master.geometry("930x230")
        self.master.title("Morse Code Translator")
        self.master.configure(bg="#2b2b2b")

        self.configure(
            bg="#2b2b2b",
            highlightbackground="#2b2b2b",
            highlightcolor="#2b2b2b",
            highlightthickness=5,
        )

        self.pack_propagate(False)
        self.master.resizable(False, False)

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

        play = ttk.Button(self, text="Play", command=self._play)

        # highlightthickness=2, highlightbackground='red')
        self.error = Label(
            self, text="Please sanitize the text", bg="#deaf9d", fg="#2b2b2b"
        )

        self.playing = Label(
            self, text="Playing the morse code in box #2", bg="#deaf9d", fg="#2b2b2b"
        )
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
        play.grid(row=2, column=3, ipadx=10, padx=5)

        # --------------------------------------------------------------------

        #                   Widget bindings
        # --------------------------------------------------------------------
        #                   Translate on <CR>
        self.box1.bind("<Return>", lambda x: self._translate())

        #                   Empty the text box on Delete
        self.box1.bind("<Delete>", lambda x: self.box1.delete("1.0", "end"))
        self.box2.bind("<Delete>", lambda x: self.box2.delete("1.0", "end"))

    def _play(self):
        """ Play the content of box #2 """
        if self.playingid is not None:
            self.after_cancel(self.playingid)

        _text2 = self.box2.get("1.0", "end").strip("\n")
        self.player.setCode(_text2)
        self.player.play()
        self.playing.grid(
            row=3, column=1, ipadx=10, padx=5, pady=5, sticky="WENS", columnspan=2
        )
        self.playingid = self.after(3000, self.playing.grid_forget)

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

        self.error.grid_forget()
        # Remove new lines, replaces new line characters to make them behave like spaces
        # .strip() will only remove the new lines at the end/beginning of a string
        # but not the ones in between.
        _text1 = self.box1.get("1.0", "end").strip("\n").replace("\n", " ")

        # print(repr(_text1))

        # Regex to remove spaces if the string is in English:
        # Only used in case we don't want to use / for spaces

        # _text1 = _text1.replace(" ", "") if re.search("[a-zA-Z]+", _text1) else _text1

        try:
            translation = (
                self.to_morse(_text1)
                if re.search("[a-zA-Z]+", _text1)
                else self.from_morse(_text1)
            )

            self.box2.delete("1.0", "end")
            self.box2.insert("1.0", translation)

        except:
            # Console output
            print("We're sorry. The text you entered could not be processed.")

            # Display error message
            self.error.grid(
                row=2, column=1, ipadx=10, padx=5, sticky="WENS", columnspan=2
            )

    # Helper functions
    def to_morse(self, englishstr) -> str:
        return " ".join(self.E2M.get(i.upper()) for i in englishstr)

    def from_morse(self, morsestr) -> str:
        return "".join(self.M2E.get(i) for i in morsestr.split())
