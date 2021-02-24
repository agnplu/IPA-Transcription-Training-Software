import tkinter as tk
from TR_ipakb import IPAKB
from TR_model import Text
from TR_cfgpanel import ConfigPanel
import random
from tkinter import filedialog
from gtts import gTTS
from playsound import playsound
import os
import webbrowser



install_message =       """For the program to run you must install the following: 
                        \n\nnltk module, eng_to_ipa module, gTTs module, playsound module
                        \n\nHave you installed them?"""
initial_message =       """Welcome to the IPA Transcription Training Software! 
                        \n\nFirst, choose your preferred type of training and press SAVE SETTINGS"""
open_file_message =     "Now open a file by pressing the OPEN FILE button"
start_message =         """Press START to begin your training.
                        \nThe software checks American English pronunciation only.
                        \nDon't forget about the primary and secondary stress in multisyllabic words."""
reset_message =         "Your training is over. \nChoose new settings and open a new file."
nltk_information =      """Natural Language Toolkit (NLTK)
                        \nA free, open source, platform for building Python programs to work with human language data. It provides a range of interfaces such as text processing libraries for classification, tokenization, stemming, tagging, parsing, and semantic reasoning. Its implementation to a Python program allows for working with corpora, categorizing text, and analyzing its linguistic structures.
                        \n------------------------------------------------------------------------------------------------------------
                        \neng-to-ipa
                        \nThis module utilizes the Carnegie-Mellon University Pronouncing Dictionary to convert English text into the International Phonetic Alphabet.
                        \n------------------------------------------------------------------------------------------------------------
                        \nGoogle Text-to-Speech (gTTs)
                        \nThis Python library interfaces with Google Translate's text-to-speech API to convert a string into an audio file."""
contact_information=    "My name is Agnieszka Pludra and I am a third year student of English Linguistics at Adam Mickiewicz University in Poznań, Poland. \nIf you have any questions or suggestions, send me an email!"
instruction_information= """Follow these simple steps to begin your practice:
                        \n\n1. Choose preferred settings and click SAVE SETTINGS
                        \n2. Open a txt file by clicking OPEN FILE
                        \n3. When ready, press START
                        \n4. Transcribe the word you see/hear using the IPA keyboard
                        \n5. Press CHECK to verify your transcription
                        \n6. Press NEXT to display the next word
                        \n7. When the training is over, repeat the procedure starting from point 1
                        \nHave fun!"""

class View:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("800x600+200+50")
        self.root.title("IPA Transcription Training Software")
        self.root.configure(background="SteelBlue4")

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=2)
        self.root.grid_rowconfigure(2, weight=1)

        self.root.grid_columnconfigure(0, weight=2)
        self.root.grid_columnconfigure(1, weight=3)

        menubar = tk.Menu(self.root)

        helpmenu = tk.Menu(menubar)
        menubar.add_cascade(label="Help", menu=helpmenu)
        helpmenu.add_command(label="Instructions", command=self.instruction_info)
        helpmenu.add_command(label="About the modules", command=self.modules_info)
        helpmenu.add_command(label="Contact the author", command=self.contact_info)
        self.root.config(menu=menubar)

        self.open_frame = tk.Frame(self.root)
        self.open_frame.grid(row=0, sticky='news', padx=4, pady=(4,0))
        self.open_frame.rowconfigure(0, weight=1)
        self.open_frame.rowconfigure(1, weight=1)
        self.open_frame.columnconfigure(0, weight=1)

        self.open_btn = tk.Button(self.open_frame, text="Open file", command=self.open_file)
        self.open_btn.grid(row=0, column=0)
        self.open_btn["state"] = tk.DISABLED
        self.info_label = tk.Label(self.open_frame, text="Currently open: \nWord count: \nType-to-token ratio:", justify=tk.LEFT, anchor="w", padx=15, pady=10)
        self.info_label.grid(row=1, column=0, sticky="news")

        self.cfgp = ConfigPanel(self.root, {"Nouns":"N", "Verbs":"V", "Adjectives":"ADJ", "Adverbs":"ADV", "Conjunctions":"C", "Determiners":"D", "Pronouns":"PRON", "Adpositions":"ADP"}, self.on_save)
        self.cfgp.grid(row=1, column=0, rowspan=2, sticky='news', padx=4, pady=4)
        self.cfg = None
        self.next_pressed = 0

        self.main_frame = tk.Frame(self.root)
        self.main_frame.grid(row=0, column=1, sticky='news')
        self.main_frame.rowconfigure(0, weight=5)
        self.main_frame.rowconfigure(1, weight=1)
        self.main_frame.columnconfigure(0, weight=1)

        self.btn_play = tk.Button(self.main_frame, text="Play", font=30, bg="SlateGray3", command=self.on_play)
        self.btn_play.grid(row=0, column=0, sticky='news')
        self.btn_play.grid_remove()

        self.label=tk.Label(self.main_frame, text=initial_message, bg="SlateGray3", wraplength=400)
        self.label.grid(row=0, column=0, sticky='news')

        self.correct_label=tk.Label(self.main_frame, text="", bg="SlateGray3")
        self.correct_label.grid(row=1, column=0, sticky='news')

        self.ipakb = IPAKB(self.root, self.on_check_press)
        self.ipakb.grid(row=1, column=1, sticky='news')

        self.btn_frame = tk.Frame(self.root)
        self.btn_frame.grid(row=2, column=1, sticky='news')
        self.btn_frame.rowconfigure(0, weight=1)
        self.btn_frame.columnconfigure(0, weight=1)
        self.btn_frame.columnconfigure(1, weight=1)
        self.btn_frame.columnconfigure(2, weight=1)

        self.button_check=tk.Button(self.btn_frame, text="Check", command=lambda: self.on_check_press(self.ipakb.textbox.get("1.0", 'end-1c')))
        self.button_check.grid(row=0, column=0, sticky='news')

        self.button_answer=tk.Button(self.btn_frame, text="Show correct", command=self.on_answer_press)
        self.button_answer.grid(row=0, column=1, sticky='news')

        self.button_next=tk.Button(self.btn_frame, text="Start", command=self.on_next_press)
        self.button_next.grid(row=0, column=2, sticky='news')

        self.button_check["state"] = tk.DISABLED
        self.button_answer["state"] = tk.DISABLED
        self.button_next["state"] = tk.DISABLED

        self.open_window()
        self.root.mainloop()

    def on_save(self, cfg):
        self.cfg = cfg

        self.cfgp.btn_save["state"]=tk.DISABLED
        self.cfgp.btn_save.configure(bg="SystemButtonFace")
        self.open_btn["state"] = tk.NORMAL
        self.label.configure(text=open_file_message)
        self.open_btn.configure(bg="SlateGray3")

        if self.cfg.audio:
            self.btn_play.grid()
            self.btn_play["state"]=tk.DISABLED
            self.label.grid_remove()
        else:
            self.label.grid()
            self.btn_play.grid_remove()


    def open_website(self):
        urls = ["https://www.nltk.org/install.html", "https://pypi.org/project/eng-to-ipa/", "https://pypi.org/project/gTTS/", "https://pypi.org/project/playsound/"]
        for url in urls:
            webbrowser.open_new_tab(url)

    def open_window(self):
        self.root.withdraw()
        top = tk.Toplevel()
        top.geometry("600x250+330+200")
        top.title("Install")
        initial_label = tk.Label(top, text=install_message, padx=20, pady=20)
        initial_label.pack(padx=30, pady=30)
        button_yes = tk.Button(top, bg="SlateGray3", text="Yes, run the program",
                               command=lambda: [top.destroy(), self.root.deiconify()])
        button_yes.place(relx=0.3, rely=0.7)
        button_no = tk.Button(top, bg="SlateGray3", text="No, I will do it now",
                              command=lambda: [self.open_website(), self.root.destroy()])
        button_no.place(relx=0.53, rely=0.7)

    def open_file(self):
        if self.cfg == None or self.next_pressed != 0:
            return

        path = filedialog.askopenfilename(filetypes=[("Text files", ".txt"), ("All files", ".*")])
        file_name = path.split('/')[-1]
        doc = Text(path)
        tokens = doc.filter_tokens(self.cfg.pos_list)
        self.transcription = doc.transcribe(tokens)

        for k in self.transcription:
            self.active_word = k
            break
        self.label.configure(text=start_message)
        self.button_next.configure(bg = "SlateGray3")
        self.info_label.configure(text= "Currently open: {} \nWord count: {} \nType-to-token ratio: {}".format(file_name, 5, 5))
        self.button_next["state"]=tk.NORMAL
        self.button_answer["state"]=tk.NORMAL
        self.button_check["state"]=tk.NORMAL
        self.open_btn["state"]=tk.DISABLED
        self.open_btn.configure(bg="SystemButtonFace")


    def reset_data(self):
        self.button_next["state"]=tk.DISABLED
        self.button_next.configure(text="Start")
        self.button_check["state"]=tk.DISABLED
        self.button_answer["state"]=tk.DISABLED
        self.btn_play["state"] = tk.DISABLED
        self.cfgp.btn_save["state"]=tk.NORMAL
        self.cfgp.btn_save.configure(bg="SlateGray3")
        self.label.config(text=reset_message, font="TkDefaultFont")
        self.correct_label.configure(text="", bg="SlateGray3")
        self.active_word = None
        self.next_pressed = 0
        self.info_label.configure(text="Currently open: \nWord count: \nType-to-token ratio:")
        if os.path.exists("word.mp3"):
            os.remove("word.mp3")

    def on_play(self):
        if not os.path.exists("word.mp3"):
            """
            An unexpected problem arose here:
            when I started designing the software, gTTs allowed for choosing American English by selecting "en-us".
            Recently, however, it has changed, as Google has removed almost all <lang>-<geo> tags that used to work.
            Hence, for now, only British English is available.
            The code will be updated as soon as the choice of American English is brought back.
            """
            tts = gTTS(text = self.active_word[0], lang = "en")
            tts.save('word.mp3')
        playsound('word.mp3')

    def on_next_press(self):
        self.next_pressed += 1
        if self.next_pressed > self.cfg.word_count:
            self.reset_data()
            return
        if os.path.exists("word.mp3"):
            os.remove("word.mp3")

        self.active_word = random.choice(list(self.transcription.keys()))
        self.label.configure(text=self.active_word, font=30)
        self.button_next.configure(text="Next", bg="SystemButtonFace")
        self.correct_label.configure(text="", bg="SlateGray3")
        self.btn_play["state"] = tk.NORMAL

    def on_answer_press(self):
        self.correct_label.configure(text="/ ".join(self.transcription[self.active_word]), bg="azure3", fg="midnight blue")

    def on_check_press(self, answer):
        correct = self.transcription[self.active_word]
        print("ANSWER: ", answer)
        print("CORRECT: ", correct)
        print(answer in correct)
        if answer in correct:
            self.correct_label.configure(text="Correct!", fg="dark green", bg="azure3")
        else:
            self.correct_label.configure(text="Try again!", fg="OrangeRed4", bg="azure3")

    def instruction_info(self):
        top = tk.Toplevel()
        top.title("Instructions")
        top.geometry("600x400+330+200")
        info_label = tk.Label(top, text = instruction_information, font=9, wraplength=550, padx=10, pady=10, justify=tk.LEFT)
        info_label.pack(padx=10, pady=10, fill=tk.BOTH)
        button_close = tk.Button(top, text="Close", command=top.destroy, bg="SlateGray3")
        button_close.pack(padx=10, pady=10)

    def modules_info(self):
        top = tk.Toplevel()
        top.title("About the modules")
        top.geometry("600x550+330+200")
        info_label = tk.Label(top, text=nltk_information, font=9, wraplength=550, padx=10, pady=10)
        info_label.pack(padx=10, pady=10, fill=tk.BOTH)
        button_close = tk.Button(top, text="Close", command=top.destroy, bg="SlateGray3")
        button_close.pack(padx=10, pady=10)

    def contact_info(self):
        top = tk.Toplevel()
        top.title("Contact the author")
        top.geometry("600x250+330+200")
        contact_label = tk.Label(top, text=contact_information, font=10, wraplength=550, padx=10, pady=10)
        contact_label.pack(padx=10, pady=25, fill=tk.BOTH)
        email_label = tk.Label(top, text="agnplu@st.amu.edu.pl", bg="SlateGray3", font=10, pady=10, borderwidth=1, relief="solid")
        email_label.pack(padx=10, pady=(0,15), fill=tk.BOTH)
        button_close = tk.Button(top, text="Close", command=top.destroy, bg="SlateGray3")
        button_close.pack(padx = 10, pady = 20)



View()
        
        
        

        
        
        