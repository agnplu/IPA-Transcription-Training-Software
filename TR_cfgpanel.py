import tkinter as tk


class Configuration:
    def __init__(self):
        self.pos_list = []
        self.audio = False
        self.word_count = 20

    def __str__(self):
        return '\n'.join([str(self.pos_list), str(self.audio), str(self.word_count)])


class LabeledFrame(tk.Frame):
    def __init__(self, root, label, orientation="vertical"):
        super().__init__(root)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        if orientation == "vertical":
            self.grid_rowconfigure(1, weight=2)
        else:
            self.grid_columnconfigure(1, weight=1)

        self.label = tk.Label(self, text=label)
        self.label.grid(column=0, row=0, sticky='news')


class ConfigPanel(tk.Frame):
    def __init__(self, root, pos_map, on_save):
        super().__init__(root)

        self.pos_map = pos_map
        self.custom_on_save = on_save

        # Create a 4 row grid in the root frame
        # One row for each setting, plus a row for the save button.
        self.grid_rowconfigure(0, weight=2)  # setting training method: written / audio
        self.grid_rowconfigure(1, weight=2)  # setting included POS: generic, defined by pos_map
        self.grid_rowconfigure(2, weight=1)  # setting number of words
        self.grid_rowconfigure(3, weight=1)  # save button
        self.grid_columnconfigure(0, weight=1)

        # Create frame to place in the 1st (index 0) row
        method_frame = LabeledFrame(self, "Training method")
        method_frame.grid(row=0, column=0, sticky='news')

        method_action_frame = tk.Frame(method_frame)
        method_action_frame.grid(row=1, column=0, sticky='news')

        method_action_frame.columnconfigure(0, weight=1)
        method_action_frame.columnconfigure(1, weight=1)
        method_action_frame.rowconfigure(0, weight=1)


        self.radio_selection = tk.BooleanVar()
        
        # Create the radio buttons within the method_action_frame side by side
        rb_written = tk.Radiobutton(method_action_frame, text="Text", variable=self.radio_selection, value=False)
        rb_audio = tk.Radiobutton(method_action_frame, text="Audio", variable=self.radio_selection, value=True)
        rb_written.grid(column=0, row=0)
        rb_audio.grid(column=1, row=0)
        # 1st row finished 
        
        # 2nd row - the POS choosing
        pos_frame = LabeledFrame(self, "Included parts of speech")
        pos_frame.grid(row=1, column=0, sticky='news')
        pos_action_frame = tk.Frame(pos_frame)
        pos_action_frame.grid(row=1, column=0, sticky='news')

        self.selected = set()

        pos_count = len(pos_map.keys())
        col_count = 4
        for i in range(col_count):
            pos_action_frame.grid_columnconfigure(i, weight=1)

        cur_row = 0
        cur_col = 0
        pos_action_frame.grid_rowconfigure(cur_row, weight=1)
        for pos in pos_map.keys():
            lab_frame = LabeledFrame(pos_action_frame, label=pos)
            lab_frame.grid(column=cur_col, row=cur_row)

            pos_cb = tk.Checkbutton(lab_frame, variable=tk.IntVar(), onvalue=1,
                                    offvalue=0, command=lambda x=pos: self.on_checkbox(pos_map[x]))
            pos_cb.grid(row=1, column=0)

            cur_col += 1
            if cur_col == col_count:
                cur_col = 0
                cur_row += 1
                pos_action_frame.grid_rowconfigure(cur_row, weight=1)

        # the number of words
        count_frame = LabeledFrame(self, "Number of words", orientation="horizontal")
        count_frame.grid(row=2, column=0, sticky='news')
        self.word_count = tk.Entry(count_frame)
        self.word_count.grid(column=1, row=0)

        # the save button
        self.btn_save = tk.Button(self, text="Save settings", command=self.on_save, bg="SlateGray3")
        self.btn_save.grid(row=3, column=0, sticky='news')

    def on_save(self):
        c = Configuration()
        c.pos_list = list(self.selected)
        c.word_count = int(self.word_count.get())
        c.audio = self.radio_selection.get()
        self.custom_on_save(c)
        self.btn_save.configure(bg="SystemButtonFace")

    def on_checkbox(self, key):
        if key in self.selected:
            self.selected.remove(key)
        else:
            self.selected.add(key)



class Main:
    def __init__(self):
        self.root = tk.Tk()
        self.root.wm_title('Test ConfigPanel')

        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)

        cfgp = ConfigPanel(self.root, {"POS":"P"}, lambda c: print(c))
        cfgp.grid(row=0, column=0)

        self.root.mainloop()

# POS = {"Nouns": "N", "Verbs": "V", "Adjectives": "ADJ", "Adverbs": "ADV",
#        "Particles": "PA", "Articles": "AR", "Barnacles": "BA", "Chronicles": "CH"}
