import random
import os
import urllib.request
import tkinter as tk
import tkinter.ttk as ttk
import datetime
import requests
import requests
import numpy as np
import imageio
import threading
import time
import queue
from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image



############################# Manual Configuration ###############################
class EntryPlus(ttk.Entry):
    def __init__(self, parent):
        ttk.Entry.__init__(self, parent)
        _rc_menu_install(self)
        # overwrite default class binding so we don't need to return "break"
        self.bind_class("Entry", "<Control-a>", self.event_select_all)
        self.bind("<Button-3><ButtonRelease-3>", self.show_menu)
        self.configure(width=70)

    def event_select_all(self):
        self.focus_force()
        self.selection_range(0, tk.END)

    def show_menu(self, e):
        self.tk.call("tk_popup", self.menu, e.x_root, e.y_root)

def _rc_menu_install(w):
    w.menu = tk.Menu(w, tearoff=0)
    w.menu.add_command(label="Cut")
    w.menu.add_command(label="Copy")
    w.menu.add_command(label="Paste")
    w.menu.add_separator()
    w.menu.add_command(label="Select all")

    w.menu.entryconfigure("Cut", command=lambda: w.focus_force() or w.event_generate("<<Cut>>"))
    w.menu.entryconfigure("Copy", command=lambda: w.focus_force() or w.event_generate("<<Copy>>"))
    w.menu.entryconfigure("Paste", command=lambda: w.focus_force() or w.event_generate("<<Paste>>"))
    w.menu.entryconfigure("Select all", command=w.event_select_all)

class AppURLopener(urllib.request.FancyURLopener):
    version = "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.69 Safari/537.36"
urllib._urlopener = AppURLopener()

###################### START OF INTERFACE #################################
class image_downloader(tk.Frame):

    def __init__(self, parent):

        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.initialize_user_interface()

    def initialize_user_interface(self):

        self.parent.title("Image Download Manager")
        self.parent.geometry("1100x650")
        canvas = Canvas(self.parent, width=255, height=185, background="lavender")
        canvas.create_rectangle(0, 0, 255, 255, outline="Gray", fill="Gray")
        canvas.place(x=450,y=430)

        self.parent.config(background="lavender")

        # Define the different GUI widgets
        self.IDM_label = tk.Label(self.parent, text="Image Download Manager", background="lavender")
        self.IDM_label.config(font=('helvetica', 16))

        self.link_label = tk.Label(self.parent, text="Please enter an image address link:", background="lavender")
        self.link_label.config(font=('helvetica', 12))

        self.link_entry = EntryPlus(self.parent)

        self.scan_label = tk.Label(self.parent, text="Please select an image to analyse:", background="lavender")
        self.scan_label.config(font=('helvetica', 12))

        self.IDM_label.place(x=450, y= 30)
        self.link_label.place(x=450, y= 65)
        self.link_entry.place(x=350, y= 100)
        self.scan_label.place(x=450, y=400)

        self.download_button = tk.Button(self.parent, text="Download",command=self.do_this_thread)
        self.download_button.place(x=800, y=95)


        self.openImg_button = tk.Button(self.parent, text="Open", command=self.open_img_thread)
        self.openImg_button.place(x=720, y=430)
        self.scanImg_button = tk.Button(self.parent, text="Scan", command=self.runthiscommand_thread)
        self.scanImg_button.place(x=770, y=430)
        # Set the treeview
        self.tree = ttk.Treeview(self.parent,columns=('img_add', 'size', 'date_dl', 'status'))
        self.tree.heading('#0', text='No.')
        self.tree.heading('img_add', text='Image address')
        self.tree.heading('size', text='Size')
        self.tree.heading('date_dl', text='Date Downloaded')
        self.tree.heading('status', text='Status')
        self.tree.column('#0', width=40, anchor= "center")
        self.tree.column('img_add', width=500, anchor= "center")
        self.tree.column('size', width=200, anchor= "center")
        self.tree.column('date_dl', width=150, anchor= "center")
        self.tree.column('status', width=100, anchor= "center")
        self.tree.place(x= 60, y= 150)
        self.treeview = self.tree
        # Initialize the counter
        self.i = 1

############################## END OF INTERFACE ######################################

    def firstComm(self):
        self.first = os.system("cmd /k C:\\WINDOWS\\system32\\cmd.exe")

    def runthiscommand_thread(self):
        self.runcommand = threading.Thread(target=self.firstComm)
        self.runcommand.start()

    def openfn(self):
        self.filename = filedialog.askopenfilename(title='open')
        return self.filename

    def open_img(self):
        self.x = self.openfn()
        self.img = Image.open(self.x)
        self.img = self.img.resize((200, 150), Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(self.img)
        self.panel = Label(self.parent, image=self.img)
        self.panel.image = self.img
        self.panel.place(x=477,y=450)

    def open_img_thread(self):
        self.open_img_thread = threading.Thread(target=self.open_img)
        self.open_img_thread.start()

    def download_image(self):

        self.url = self.link_entry.get()
        self.name = random.randrange (1,100)
        self.path = "C:\\Users\\user pc\\Desktop\\FYP images\\"
        self.fullfilename = str(self.name) + ".png"
        self.size = requests.get(self.url, stream=True)
        urllib._urlopener.retrieve(self.url, self.path+self.fullfilename)

    def do_this(self):
        self.download_image()
        self.insert_data()

    def do_this_thread(self):
        self.thread_do_this = threading.Thread(target= self.do_this)
        self.thread_do_this.start()

    def insert_data(self):
        """
        Insertion method.
        """
        self.status = "not scanned"
        self.treeview.insert('', 'end', text=str(self.i),values=(self.link_entry.get(), self.size.headers['Content-length'],
                                                                 str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                                                                 self.status))
        # Increment counter
        self.i = self.i + 1

########################## END OF DOWNLOAD, INSERT, OPEN AND SCAN FUNCTION #####################################


def main():
    root=tk.Tk()
    d=image_downloader(root)
    root.mainloop()

if __name__=="__main__":
    main()