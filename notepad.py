#!/usr/bin/env python3
import tkinter
from tkinter import Menu
from tkinter import filedialog
from tkinter import ttk
from tkinter import font
import os

#root window
root = tkinter.Tk()
root.title("Notepad")
root.geometry("800x600")


#create a text input 
text = tkinter.Text(root,highlightthickness=0, bd=0,padx=5,pady=5,font=(8), undo=True, autoseparators=True, maxundo=-1)
text.pack(expand=True, fill=tkinter.BOTH)


#create a menubar
menubar = Menu(root)
root.config(menu=menubar)

#creating a menu
file_menu = Menu(menubar, tearoff=False, background="silver")
edit_menu = Menu(menubar, tearoff=False,background="silver")
preferences_menu = Menu(menubar, tearoff=False, background="silver")
help_menu = Menu(menubar,tearoff=False, background="silver")
#sub_menu menu
sub_menu = Menu(preferences_menu, tearoff=False,background="silver")
sub_menu2 = Menu(preferences_menu, tearoff=False)
sub_menu3 = Menu(preferences_menu, tearoff=False,background="silver") 
sub_menu4 = Menu(preferences_menu, tearoff=False, background="silver")

#addding menu menu options to the menubar
menubar.add_cascade(label="File",menu=file_menu)
menubar.add_cascade(label="Edit",menu=edit_menu)
menubar.add_cascade(label="Preferences",menu=preferences_menu)
menubar.add_cascade(label="Help", menu=help_menu)

#adding sub menu
preferences_menu.add_cascade(label="Font-size", menu=sub_menu)
preferences_menu.add_cascade(label="Background color", menu=sub_menu2)
preferences_menu.add_cascade(label="Text color", menu=sub_menu3)
preferences_menu.add_cascade(label="Weight", menu=sub_menu4)

 
#functions for menu items

current_saving = ""

def save_file(event=None):
    global current_saving
    if current_saving:
        with open(current_saving,"w") as f:
            f.write(text.get(1.0, tkinter.END))

    

def open_file(event=None):
    global current_saving
    file_path = filedialog.askopenfilename(title="Select File")
    if file_path:
        current_saving = file_path
        with open(file_path,"r") as f:
            content = f.read()
            text.delete(1.0,tkinter.END)
            text.insert(tkinter.END,content)
        root.title(os.path.basename(file_path))    
def save_as_file(event=None):
    file_path = filedialog.asksaveasfilename(title="Select File", defaultextension=".txt")
    if file_path:
        with open(file_path,"w") as f:
            f.write(text.get(1.0, tkinter.END))

def new(event=None):
    global current_saving
    file_path = filedialog.asksaveasfilename(title="Create new File", defaultextension=".txt")
    if file_path:
        current_saving = file_path
        root.title(os.path.basename(file_path))

def new_window(event=None):
    os.system(f"python3 {os.path.basename(__file__)}")


def close_file(event=None):
    global current_saving
    current_saving = ""
    root.title("Notepad")
    text.delete(1.0,tkinter.END)

#Functions for Edit menu


def cut(event=None):
    text.event_generate("<<Cut>>")

def copy(event=None):
    selected_text = text.selection_get()
    root.clipboard_clear() 
    root.clipboard_append(selected_text) 

def paste(event=None):
    text.event_generate("<<Paste>>")


def select_all(event=None):
    text.tag_add(tkinter.SEL, "1.0", tkinter.END)
    text.mark_set(tkinter.INSERT, "1.0")
    text.see(tkinter.INSERT)

def find_text(event=None):
    #new window
    new_window = tkinter.Toplevel(root)
    new_window.title("Find and Replace")
    new_window.geometry("300x200")  

    #lines for find mode
    tkinter.Label(new_window, text="Type text to find").pack()

    name_entry = ttk.Entry(new_window)
    name_entry.pack()

    find_button = tkinter.Button(new_window, text='Find', command=lambda: find(name_entry))
    find_button.pack(pady=5)

    #lines for replace mode
    tkinter.Label(new_window, text="Type text to replace with").pack()
    replace_entry = ttk.Entry(new_window)
    replace_entry.pack()
    
    replace_button = tkinter.Button(new_window, text="Replace", command=lambda:replace(name_entry,replace_entry))
    replace_button.pack(pady=5)

    new_window.protocol("WM_DELETE_WINDOW", lambda:close_function(new_window))


def find(name_entry): 
    
    # remove tag 'found' from index 1 to END 
    text.tag_remove('found', '1.0', tkinter.END) 
    
    # returns to widget currently in focus 
    s = name_entry.get()
    
    if (s): 
        idx = '1.0'
        while 1: 
            # searches for desired string from index 1 
            idx = text.search(s, idx, nocase = 1, 
                            stopindex = tkinter.END)
            
            if not idx: break
            
            # last index sum of current index and 
            # length of text 
            lastidx = '% s+% dc' % (idx, len(s))
            

            # overwrite 'Found' at idx 
            text.tag_add('found', idx, lastidx) 
            idx = lastidx 

        # mark located string as red
        
        text.tag_config('found', foreground ='red')
    name_entry.focus_set()


def replace(name_entry,replace_entry):

    # remove tag 'found' from index 1 to END
    text.tag_remove('found', '1.0', tkinter.END)

    # returns to widget currently in focus
    s = name_entry.get()
    r = replace_entry.get()

    if (s and r):
        idx = '1.0'
        while 1:
            # searches for desired string from index 1
            idx = text.search(s, idx, nocase = 1,
                            stopindex =tkinter.END)
            if not idx: break

            # last index sum of current index and
            # length of text
            lastidx = '% s+% dc' % (idx, len(s))

            text.delete(idx, lastidx)
            text.insert(idx, r)

            lastidx = '% s+% dc' % (idx, len(r))

            # overwrite 'Found' at idx
            text.tag_add('found', idx, lastidx)
            idx = lastidx

        # mark located string as red
        text.tag_config('found', foreground ='green', background = 'yellow')
    name_entry.focus_set()

def close_function(new_window):
    if (text.tag_remove("found", 1.0, tkinter.END)): 
        pass

    new_window.destroy()

def undo_action():
    try:
        text.edit_undo()
    except:
        pass
def redo_action():
    try:
        text.edit_redo()
    except:
        pass

   
#submenu functions

def font_size(i):
    current_font= font.Font(font=text["font"])
    current_font.configure(size=i)
    text.configure(font=current_font)

def background_color(color):
    text.configure(bg=color)

def text_color(color):
    text.configure(fg=color)

def font_weight(font_weight,text):
    current_font = font.Font(font=text["font"])
    current_font.configure(weight=font_weight)
    text.configure(font=current_font)

#Help menu functions

def keyboard_shortcuts():
    new_window = tkinter.Toplevel(root)
    new_window.title("Keyboard Shortcuts")
    new_window.geometry("500x400")

    tkinter.Label(new_window, text="New  -   Ctrl+N", font=("Arial", 14), anchor=tkinter.W, justify=tkinter.LEFT).pack(fill="x")
    tkinter.Label(new_window,text="New window   -   Ctrl+Shift+N", font=("Arial", 14), anchor=tkinter.W, justify=tkinter.LEFT).pack(fill="x")
    tkinter.Label(new_window,text="Open   -   Ctrl+O", font=("Arial", 14), anchor=tkinter.W, justify=tkinter.LEFT).pack(fill="x")
    tkinter.Label(new_window,text="Save   -   Ctrl+S", font=("Arial", 14), anchor=tkinter.W, justify=tkinter.LEFT).pack(fill="x")
    tkinter.Label(new_window,text="Save as   -   Ctrl+Shift=S", font=("Arial", 14), anchor=tkinter.W, justify=tkinter.LEFT).pack(fill="x")
    tkinter.Label(new_window,text="-------------------------", font=("Arial", 14), anchor=tkinter.W, justify=tkinter.LEFT).pack(fill="x")
    tkinter.Label(new_window,text="Undo   -   Ctrl+Z", font=("Arial", 14), anchor=tkinter.W, justify=tkinter.LEFT).pack(fill="x")
    tkinter.Label(new_window,text="Redo   -   Ctrl+Shift+Z", font=("Arial", 14), anchor=tkinter.W, justify=tkinter.LEFT).pack(fill="x")
    tkinter.Label(new_window,text="Cut   -   Ctrl+X", font=("Arial", 14), anchor=tkinter.W, justify=tkinter.LEFT).pack(fill="x")
    tkinter.Label(new_window,text="Copy   -   Ctrl+C", font=("Arial", 14), anchor=tkinter.W, justify=tkinter.LEFT).pack(fill="x")
    tkinter.Label(new_window,text="Paste   -   Ctrl+V", font=("Arial", 14), anchor=tkinter.W, justify=tkinter.LEFT).pack(fill="x")
    tkinter.Label(new_window,text="Select All   -   Ctrl+A", font=("Arial", 14), anchor=tkinter.W, justify=tkinter.LEFT).pack(fill="x")
    tkinter.Label(new_window,text="Find and Replace    -   Ctrl+F", font=("Arial", 14), anchor=tkinter.W, justify=tkinter.LEFT).pack(fill="x")



#add File menu items
file_menu.add_command(label="New            Ctrl+N", command=new)
file_menu.add_command(label="New window     Ctrl+Shift+N", command=new_window)
file_menu.add_command(label="Open           Ctrl+O",command=open_file)
file_menu.add_command(label="Save           Ctrl+S", command=lambda:save_file(current_saving))
file_menu.add_command(label="Save as        Ctrl+Shift+S",command=save_as_file)
file_menu.add_command(label="Close", command=close_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=lambda:root.destroy())

#add Edit menu items
edit_menu.add_command(label="Undo       Ctrl+Z", command=undo_action)
edit_menu.add_command(label="Redo        Ctrl+Shift+Z", command=redo_action)
edit_menu.add_separator()
edit_menu.add_command(label="Cut        Ctrl+X", command=cut)
edit_menu.add_command(label="Copy       Ctrl+C", command=copy)
edit_menu.add_command(label="Paste      Ctrl+V", command=paste)
edit_menu.add_separator()
edit_menu.add_command(label="Select All     Ctrl+A", command=select_all)
edit_menu.add_separator()
edit_menu.add_command(label="Find and Replace       Ctrl+F",command=find_text)

#add items to submenu Font-size
sub_menu.add_command(label="8", command=lambda:font_size(8))
sub_menu.add_command(label="9", command=lambda:font_size(9)) 
sub_menu.add_command(label="10", command=lambda:font_size(10))
sub_menu.add_command(label="11", command=lambda:font_size(11))
sub_menu.add_command(label="12", command=lambda:font_size(12))
sub_menu.add_command(label="14", command=lambda:font_size(14))
sub_menu.add_command(label="16", command=lambda:font_size(16))
sub_menu.add_command(label="18", command=lambda:font_size(18))
sub_menu.add_command(label="20", command=lambda:font_size(20))
sub_menu.add_command(label="22", command=lambda:font_size(22))
sub_menu.add_command(label="24", command=lambda:font_size(24))
sub_menu.add_command(label="26", command=lambda:font_size(26))
sub_menu.add_command(label="28", command=lambda:font_size(28))
sub_menu.add_command(label="36", command=lambda:font_size(36))
sub_menu.add_command(label="48", command=lambda:font_size(48))
sub_menu.add_command(label="72", command=lambda:font_size(72))


#add items to submenu background color
sub_menu2.add_command(label="black", command=lambda:background_color("black"), background="black")
sub_menu2.add_command(label="white", command=lambda:background_color("white"), background="white")
sub_menu2.add_command(label="red", command=lambda:background_color("red"), background="red")
sub_menu2.add_command(label="blue", command=lambda:background_color("blue"), background="blue")
sub_menu2.add_command(label="green", command=lambda:background_color("green"), background="green")
sub_menu2.add_command(label="yellow", command=lambda:background_color("yellow"), background="yellow")
sub_menu2.add_command(label="purple", command=lambda:background_color("purple"), background="purple")
sub_menu2.add_command(label="gray", command=lambda:background_color("gray"), background="gray")
sub_menu2.add_command(label="aqua", command=lambda:background_color("aqua"), background="aqua")
sub_menu2.add_command(label="lime", command=lambda:background_color("lime"), background="lime")
sub_menu2.add_command(label="navy", command=lambda:background_color("navy"), background="navy")
sub_menu2.add_command(label="ping", command=lambda:background_color("pink"), background="pink")
sub_menu2.add_command(label="orange", command=lambda:background_color("orange"), background="orange")
sub_menu2.add_command(label="gold", command=lambda:background_color("gold"), background="gold")
sub_menu2.add_command(label="indigo", command=lambda:background_color("indigo"), background="indigo")
sub_menu2.add_command(label="maroon", command=lambda:background_color("maroon"), background="maroon")

#add items to submenu Text color

sub_menu3.add_command(label="black", command=lambda:text_color("black"), foreground="black")
sub_menu3.add_command(label="white", command=lambda:text_color("white"), foreground="white")
sub_menu3.add_command(label="red", command=lambda:text_color("red"), foreground="red")
sub_menu3.add_command(label="blue", command=lambda:text_color("blue"), foreground="blue")
sub_menu3.add_command(label="green", command=lambda:text_color("green"), foreground="green")
sub_menu3.add_command(label="yellow", command=lambda:text_color("yellow"), foreground="yellow")
sub_menu3.add_command(label="purple", command=lambda:text_color("purple"), foreground="purple")
sub_menu3.add_command(label="gray", command=lambda:text_color("gray"), foreground="gray")
sub_menu3.add_command(label="aqua", command=lambda:text_color("aqua"), foreground="aqua")
sub_menu3.add_command(label="lime", command=lambda:text_color("lime"), foreground="lime")
sub_menu3.add_command(label="navy", command=lambda:text_color("navy"), foreground="navy")
sub_menu3.add_command(label="ping", command=lambda:text_color("pink"), foreground="pink")
sub_menu3.add_command(label="orange", command=lambda:text_color("orange"), foreground="orange")
sub_menu3.add_command(label="gold", command=lambda:text_color("gold"), foreground="gold")
sub_menu3.add_command(label="indigo", command=lambda:text_color("indigo"), foreground="indigo")
sub_menu3.add_command(label="maroon", command=lambda:text_color("maroon"), foreground="maroon")

#add items to submenu Weight

sub_menu4.add_command(label="bold", command=lambda:font_weight("bold", text))
sub_menu4.add_command(label="normal", command=lambda:font_weight("normal",text))

#add Help menu items

help_menu.add_command(label="Keyboard Shortcuts",command=keyboard_shortcuts)
help_menu.add_command(label="Thanks for using this :)")

#key binding
root.bind("<Control-n>", new)
root.bind("<Control-Shift-N>",new_window)
root.bind("<Control-o>",open_file)
root.bind("<Control-s>",save_file)
root.bind("<Control-Shift-S>", save_as_file)
root.bind("<Control-a>",select_all)
root.bind("<Control-f>", find_text)

root.mainloop()

