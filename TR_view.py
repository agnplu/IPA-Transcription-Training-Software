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



install_message = """For the program to run you must install the following: 
                \n\n nltk module, eng_to_ipa module, gTTs module
                \n\nHave you installed them?"""
initial_message = """Welcome to IPA Transcription Training Software! 
                \n Go to File > Instructions to learn how to use the software"""
reset_message = "Your training is over. \nChoose new settings and open a new file."


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
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Open", command=self.open_file)
        menubar.add_cascade(label="File", menu=filemenu)
        
        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Contact", command=self.open_file)
        helpmenu.add_command(label="About", command=self.open_file)
        menubar.add_cascade(label="Help", menu=helpmenu)
        
        self.root.config(menu=menubar)
        
        self.info_label = tk.Label(self.root, text="Currently open: \nWord count: \nType-to-token ratio:", justify=tk.LEFT, anchor="w", padx=15, pady=10, bg="SlateGray3")
        self.info_label.grid(row=0, column=0, sticky="news", padx=4, pady=(4,0))

        
        self.cfgp = ConfigPanel(self.root, {"Nouns":"N", "Verbs":"V", "Adjectives":"ADJ", "Adverbs":"ADV"}, self.on_save)
        self.cfgp.grid(row=1, column=0, rowspan=2, sticky='news', padx=4, pady=4)
        self.cfg = None
        self.next_pressed = 0
        
        self.btn_play = tk.Button(self.root, text="Play word", font=30, bg="gray75", command=self.on_play)
        self.btn_play.grid(row=0, column=1, sticky='news')
        self.btn_play.grid_remove()
       
        self.label = tk.Label(self.root, text=initial_message, font=30, bg="SlateGray3", wraplength=400)
        self.label.grid(row=0, column=1, sticky='news', padx=(0,4), pady=(4,0))
        
        
        self.ipakb = IPAKB(self.root, self.on_check_press)
        self.ipakb.grid(row=1, column=1, sticky='news')
        
        self.btn_frame = tk.Frame(self.root)
        self.btn_frame.grid(row=2, column=1, sticky='news')
        self.btn_frame.rowconfigure(0, weight=1)
        self.btn_frame.columnconfigure(0, weight=1)
        self.btn_frame.columnconfigure(1, weight=1)
        
        self.button_check = tk.Button(self.btn_frame, text="Check", command=lambda: self.on_check_press(self.ipakb.textbox.get("1.0", 'end-1c')))
        self.button_check.grid(row=0, column=0, sticky='news')
        #self.button_correct = tk.Button(self.btn_frame, text="Show Correct", command=self.on_correct_press)
        #self.button_correct.grid(row=0, column=1, sticky='news')
    
        self.button_next = tk.Button(self.btn_frame, text="Start", command=self.on_next_press)
        self.button_next.grid(row=0, column=1, sticky='news')
        
        self.button_check["state"] = tk.DISABLED
        self.button_next["state"] = tk.DISABLED

        self.open_window()
        self.root.mainloop() 
        
    def on_save(self, cfg):
        self.cfg = cfg

        self.cfgp.btn_save["state"] = tk.DISABLED
        
        if self.cfg.audio:
            self.btn_play.grid()
            self.label.grid_remove()
        else:
            self.label.grid()
            self.btn_play.grid_remove()
        
        print(self.cfg.pos_list)
        print(self.cfg.audio)
        print(self.cfg.word_count)
    
 
    def open_website(self):
        urls = ["https://www.nltk.org/install.html", "https://pypi.org/project/eng-to-ipa/", "https://pypi.org/project/gTTS/"]
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
        self.button_next["state"] = tk.NORMAL
        self.button_check["state"] = tk.NORMAL
        
        for k in self.transcription:
            self.active_word = k
            break
        self.button_next.configure(bg = "SlateGray3")

        self.info_label.configure(text= "Currently open: {} \nWord count: {} \nType-to-token ratio: {}".format(file_name, 5, 5))
        

    def reset_data(self):
        self.button_next["state"] = tk.DISABLED
        self.button_next.configure(text="Start")
        self.button_check["state"] = tk.DISABLED
        self.cfgp.btn_save["state"] = tk.NORMAL
        self.label.config(text=reset_message)
        self.active_word = None
        self.next_pressed = 0
        self.info_label.configure(text="Currently open: \nWord count: \nType-to-token ratio:")       
        if os.path.exists("word.mp3"):
            os.remove("word.mp3")
        
        
    def on_play(self):
        if not os.path.exists("word.mp3"):
            tts = gTTS(text = self.active_word[0], lang = 'en', slow = False)
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
        self.label.config(text=self.active_word)
        self.root.configure(background="SteelBlue4")
        self.button_next.configure(text="Next")
        self.button_next.configure(bg='SystemButtonFace')
        
        
    def on_correct_press(self):
        pass
        
            
    def on_check_press(self, answer):
        correct = self.transcription[self.active_word]
        print("ANSWER: ", answer)
        print("CORRECT: ", correct)
        print(answer in correct)
        if answer in correct:
            self.root.configure(background="green")
        else:
            self.root.configure(background="red")            


View()


"""
        self.correct_popup=tk.Button(self.label, text="Show correct", bg="LightSkyBlue3", fg="white")
        self.correct_popup.pack(anchor=tk.E, padx=10, pady=10)
        self.correct_popup.bind("<Enter>", self.show_correct)
        self.correct_popup.bind("<Leave>", self.hide_correct)
        
        self.correct_label=tk.Label(self.label, bg="gray97", fg="gray97", text="", padx=10, pady=10, width=60, wraplength=320)
        self.correct_label.pack(padx=10, pady=(0,5))
        
    def show_correct(self, event):
        self.correct_label.configure(bg="white", fg="gray55", borderwidth=1, relief="groove")

    def hide_correct(self, event):
        self.correct_label.configure(bg="gray97", fg="gray97", borderwidth=0)
        
        
        
        """
        
        
        