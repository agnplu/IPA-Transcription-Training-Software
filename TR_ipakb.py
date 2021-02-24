import tkinter as tk

class IPAKB(tk.Frame):

    # Each key on the physical keyboard is associated with a unique code,
    # so 'a' corresponds to the button 'A', while 'A' corresponds to the
    # combination 'Shift+A'.
    # This map maps every such code to a certain IPA symbol.
    kb_map={
        # NASALS
        'm': 'm', 'n': 'n', 'N': 'ŋ',
        # UNVOICED PLOSIVES/AFFRICATES/FRICATIVES
        'p': 'p', 't': 't', 'T': 'θ', 'k': 'k', 'f': 'f', 's': 's', 'S': 'ʃ',
        # VOICED PLOSIVES/AFFRICATES/FRICATIVES
        'b': 'b', 'd': 'd', 'D': 'ð', 'g': 'ɡ', 'v': 'v', 'z': 'z', 'Z': 'ʒ', 'h': 'h',
        # APPROXIMANTS
        'l': 'l', 'r': 'r', 'j': 'j', 'w': 'w',
        # A-LIKE VOWELS
        'A': 'ɑ', 'a': 'a', 'V': 'ʌ', 'q': 'æ',
        # E-LIKE VOWELS
        'e': 'e', 'E': 'ɛ',
        # I-LIKE VOWELS
        'i': 'i', 'I': 'ɪ',
        # O-LIKE VOWELS
        'o': 'o', 'O': 'ɔ',
        # U-LIKE VOWELS
        'u': 'u', 'U': 'ʊ',
        # SCHWA
        'y': 'ə', 'Y': 'ɜ',
        # SPECIAL
        '<comma>': 'ˌ', '<quoteright>': 'ˈ', '<Return>': ''
    }


    top_rows=[['l', 'r', 'j', 'w', 'm', 'n', 'ŋ'],
                ['p', 't', 'θ', 'k', 'f', 's', 'ʃ']]
    bot_rows=[['b', 'd', 'ð', 'ɡ', 'v', 'z', 'ʒ', 'h'],
                ['ɑ', 'a', 'ʌ', 'æ', 'e', 'ɛ', 'ə', 'ˌ'],
                ['i', 'ɪ', 'o', 'ɔ', 'u', 'ʊ', 'ɜ', 'ˈ']]

    def __init__(self, root, on_enter):
        super().__init__(root)

        self.on_enter=on_enter

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        self.init_text_box()
        self.init_keyboard()

    def init_text_box(self):
        """Creates and initializes a tk.Text widget and re-binds all
        keys used to write IPA symbols."""

        self.textbox=tk.Text(self, width=40, height=4, font=("Helvetica", 14))
        self.textbox.grid(row=0, column=0, sticky='nesw')
        for k in IPAKB.kb_map.keys():
            self.textbox.bind(k, self.write_evt)

    def init_keyboard(self):
        """Creates and initializes a tk.Frame widget containing
        a grid of 6 rows and 8 columns, representing a keyboard.

        The first three rows contain consonants, with nasals and
        approximants in the first, voiceless sounds in the second,
        and their voiced counterparts in the third row.
        The Enter key is in the last column of the first two rows.

        Vowels are located in the 4th and 5th rows, in no particular
        order other than alphabetical resemblance.
        The last column of the 4th and 5th rows contains the stress
        and prolongation symbols.

        The Space key spans the whole 6th row."""

        # Create a root frame
        self.kb_buttons=tk.Frame(self)
        self.kb_buttons.grid(row=1, column=0, sticky='nesw')

        # Define its layout as a 6 by 8 grid
        for r in range(6):
            self.kb_buttons.rowconfigure(r, weight=1)
        for c in range(8):
            self.kb_buttons.columnconfigure(c, weight=1)

        # Create and place the top two rows of buttons into the grid
        for r in range(len(IPAKB.top_rows)):
            for c in range(len(IPAKB.top_rows[0])):
                btn=tk.Button(self.kb_buttons, text=IPAKB.top_rows[r][c], command=lambda key=IPAKB.top_rows[r][c]: self.write(key))
                btn.grid(row=r, column=c, sticky='news')

        # Create and place the Enter button
        enter=tk.Button(self.kb_buttons, text="Enter", command=lambda: self.on_enter(self.textbox.get("1.0", 'end-1c')))
        enter.grid(row=0, rowspan=2, column=7, sticky='news')

        # Create and place rows 3-5
        for r in range(len(IPAKB.bot_rows)):
            for c in range(len(IPAKB.bot_rows[0])):
                btn=tk.Button(self.kb_buttons, text=IPAKB.bot_rows[r][c], command=lambda key=IPAKB.bot_rows[r][c]: self.write(key))
                btn.grid(row=r+2, column=c, sticky='nesw')

        # Create and place the Space button
        space=tk.Button(self, text='space', command=lambda key=' ': self.write(key))
        space.grid(row=5, column=0, columnspan=8, sticky='nesw')

    def write(self, key):
        """This method handles button-presses in the GUI keyboard."""
        self.textbox.insert(tk.END, key)

    def write_evt(self, event):
        """This method handles key-presses from the physical keyboard."""
        if event.keysym in ['comma', 'quoteright']:
            self.textbox.insert(tk.INSERT, IPAKB.kb_map["<" + event.keysym + ">"])
        elif event.keysym in IPAKB.kb_map:
            self.textbox.insert(tk.INSERT, IPAKB.kb_map[event.keysym])
        elif event.keysym=="Return":
            self.on_enter(self.textbox.get("1.0", 'end-1c'))
        elif event.keysym in ["space", "backspace"]:
            return
        return "break"

