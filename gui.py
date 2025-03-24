import tkinter as tk
from tkinter import filedialog
from tkinter.scrolledtext import ScrolledText
import sys
import os
import subprocess
import json
import threading

class RedirectText:
    def __init__(self, widget):
        self.widget = widget

    def write(self, string):
        self.widget.config(state=tk.NORMAL)
        self.widget.insert(tk.END, string)
        self.widget.see(tk.END)
        self.widget.config(state=tk.DISABLED)

    def flush(self):
        pass

def set_transparency(value):
    root.attributes("-alpha", int(value) / 100)

def toggle_lock():
    global is_locked
    is_locked = not is_locked
    if is_locked:
        lock_button.config(text="𝑳𝒐𝒄𝒌𝒆𝒅")
        root.attributes("-topmost", True)
    else:
        lock_button.config(text="𝑼𝒏𝒍𝒐𝒄𝒌𝒆𝒅")
        root.attributes("-topmost", False)

def start_process():
    print("Starting main.py...")
    global process
    process = subprocess.Popen(
        ["python", "main.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    def read_process_output(proc):
        for line in proc.stdout:
            print(line, end="")
        for line in proc.stderr:
            print(line, end="")

    threading.Thread(target=read_process_output, args=(process,), daemon=True).start()

def stop_process():
    print("Stopping all processes...")
    try:
        if process:
            process.terminate()
            print("Process stopped!")
    except NameError:
        print("No process is running.")

def clear_terminal():
    log_text.config(state=tk.NORMAL)
    log_text.delete("1.0", tk.END)
    log_text.config(state=tk.DISABLED)
    print("Terminal cleared!")

def open_directory():
    print("Opened project directory!")
    project_dir = os.path.dirname(os.path.abspath(__file__))
    os.startfile(project_dir)

def check_for_updates():
    print("Checking for updates...")

def on_hover(button):
    button.config(bg="black", fg="red")

def on_leave(button):
    button.config(bg="darkred", fg="black")

def set_token():
    print("Open Account Token Config...")
    def save_token():
        token = token_entry.get()
        if token:
            print(f"Token set to: {token}")
            with open("config/config.json", "r") as config_file:
                config = json.load(config_file)
            config["token"] = token
            with open("config/config.json", "w") as config_file:
                json.dump(config, config_file, indent=4)
            token_window.destroy()
        else:
            print("No token entered.")

    token_window = tk.Toplevel(root)
    token_window.title("𝕊𝕖𝕥 𝔻𝕚𝕤𝕔𝕠𝕣𝕕 𝔸𝕔𝕔 𝕋𝕠𝕜𝕖𝕟")
    token_window.geometry("300x150")
    token_window.resizable(False, False)
    token_window.configure(bg="red")
    token_window.iconphoto(False, tk.PhotoImage(file="img/logo.png"))

    token_label = tk.Label(token_window, text="𝔼𝕟𝕥𝕖𝕣 𝕐𝕠𝕦𝕣 𝔻𝕚𝕤𝕔𝕠𝕣𝕕 𝔸𝕔𝕔𝕠𝕦𝕟𝕥 𝕋𝕠𝕜𝕖𝕟", fg="black", bg="red", font=("Arial", 13))
    token_label.pack(pady=10)

    token_entry = tk.Entry(token_window, fg="black", bg="darkred", font=("Arial", 12))
    token_entry.pack(pady=10)

    set_button = tk.Button(token_window, text="𝕊𝕖𝕥 𝕋𝕠𝕜𝕖𝕟", bg="darkred", fg="black", font=("Arial", 13), relief="ridge", bd=2, command=save_token)
    set_button.pack(pady=10)
    set_button.bind("<Enter>", lambda event: on_hover(set_button))
    set_button.bind("<Leave>", lambda event: on_leave(set_button))

    print("Set token config opened!")

def set_prefix():
    print("Open Prefix Config...")

    def save_prefix():
        prefix = prefix_entry.get()
        if len(prefix) == 1:
            print(f"Prefix set to: {prefix}")
            with open("config/config.json", "r") as config_file:
                config = json.load(config_file)
            config["prefix"] = prefix
            with open("config/config.json", "w") as config_file:
                json.dump(config, config_file, indent=4)
            prefix_window.destroy()
        else:
            print("Invalid prefix! Only one character allowed.")

    prefix_window = tk.Toplevel(root)
    prefix_window.title("𝕊𝕖𝕥 𝕊𝕖𝕝𝕗𝕓𝕠𝕥 𝕡𝕣𝕖𝕗𝕚𝕩")
    prefix_window.geometry("300x150")
    prefix_window.resizable(False, False)
    prefix_window.configure(bg="red")
    prefix_window.iconphoto(False, tk.PhotoImage(file="img/logo.png"))

    prefix_label = tk.Label(prefix_window, text="𝔼𝕟𝕥𝕖𝕣 𝕠𝕟𝕖 𝕔𝕙𝕒𝕣𝕒𝕔𝕥𝕖𝕣 𝕡𝕣𝕖𝕗𝕚𝕩", fg="black", bg="red", font=("Arial", 13))
    prefix_label.pack(pady=10)

    prefix_entry = tk.Entry(prefix_window, fg="black", bg="darkred", font=("Arial", 12), justify="center")
    prefix_entry.pack(pady=10)

    set_button = tk.Button(prefix_window, text="𝕊𝕖𝕥 𝕡𝕣𝕖𝕗𝕚𝕩", bg="darkred", fg="black", font=("Arial", 13), relief="ridge", bd=2, command=save_prefix)
    set_button.pack(pady=10)
    set_button.bind("<Enter>", lambda event: on_hover(set_button))
    set_button.bind("<Leave>", lambda event: on_leave(set_button))

    print("Set prefix config opened!")

root = tk.Tk()
root.title("𝔻𝕣𝕚𝕚𝕫𝕫𝕪𝕪𝕤 𝔻𝕚𝕤𝕔𝕠𝕣𝕕 𝕊𝕖𝕝𝕗𝕓𝕠𝕥 𝕍𝟙.𝟝.𝟘")
root.geometry("620x400")
root.resizable(False, False)
root.configure(bg="red")
root.attributes("-alpha", 0.95)
root.iconphoto(False, tk.PhotoImage(file="img/logo.png"))

log_text = ScrolledText(root, bg="darkred", fg="black", font=("Arial", 10), wrap=tk.WORD)
log_text.place(x=60, y=50, width=400, height=300)
log_text.config(state=tk.DISABLED, highlightbackground="black", highlightcolor="black")

label_top_right = tk.Label(root, text="𝟮𝟬𝟮𝟱", fg="black", bg="red", font=("Arial", 17))
label_top_right.place(x=570, y=-5)

label_bottom_left = tk.Label(root, text="𝐃𝐞𝐯𝐞𝐥𝐨𝐩𝐞𝐫: .𝒅𝒓𝒊𝒊𝒛𝒛𝒚𝒃 | 𝒎𝒓.𝒅𝒆𝒗𝒊𝒍.𝒄𝟏𝟑𝟕", fg="black", bg="red", font=("Arial", 14))
label_bottom_left.place(x=0, y=373)

transparency_slider = tk.Scale(root, from_=100, to=20, orient=tk.VERTICAL, bg="darkred", fg="black", font=("Arial", 10), command=set_transparency, highlightbackground="black", highlightcolor="black", troughcolor="black")
transparency_slider.set(95)
transparency_slider.place(x=5, y=50, height=300)

update_button = tk.Button(root, text="𝗖𝗵𝗲𝗰𝗸 𝗳𝗼𝗿 𝗨𝗽𝗱𝗮𝘁𝗲𝘀", bg="darkred", fg="black", font=("Arial", 13), relief="ridge", bd=2, command=check_for_updates)
update_button.place(x=10, y=10, width=125, height=30)
update_button.bind("<Enter>", lambda event: on_hover(update_button))
update_button.bind("<Leave>", lambda event: on_leave(update_button))

is_locked = False
lock_button = tk.Button(root, text="𝕃𝕠𝕔𝕜", bg="darkred", fg="black", font=("Arial", 13), relief="ridge", bd=2, command=toggle_lock)
lock_button.place(x=140, y=10, width=80, height=30)
lock_button.bind("<Enter>", lambda event: on_hover(lock_button))
lock_button.bind("<Leave>", lambda event: on_leave(lock_button))

clear_button = tk.Button(root, text="𝗖𝗹𝗲𝗮𝗿 𝗧𝗲𝗿𝗺𝗶𝗻𝗮𝗹", bg="darkred", fg="black", font=("Arial", 13), relief="ridge", bd=2, command=clear_terminal)
clear_button.place(x=325, y=353, width=115, height=25)
clear_button.bind("<Enter>", lambda event: on_hover(clear_button))
clear_button.bind("<Leave>", lambda event: on_leave(clear_button))

start_button = tk.Button(root, text="𝕊𝕥𝕒𝕣𝕥 𝕊𝕖𝕝𝕗𝕓𝕠𝕥", bg="darkred", fg="black", font=("Arial", 13), relief="ridge", bd=2, command=start_process)
start_button.place(x=480, y=80, width=120, height=30)
start_button.bind("<Enter>", lambda event: on_hover(start_button))
start_button.bind("<Leave>", lambda event: on_leave(start_button))

stop_button = tk.Button(root, text="𝕊𝕥𝕠𝕡 𝕊𝕖𝕝𝕗𝕓𝕠𝕥", bg="darkred", fg="black", font=("Arial", 13), relief="ridge", bd=2, command=stop_process)
stop_button.place(x=480, y=120, width=120, height=30)
stop_button.bind("<Enter>", lambda event: on_hover(stop_button))
stop_button.bind("<Leave>", lambda event: on_leave(stop_button))

open_directory_button = tk.Button(root, text="𝕆𝕡𝕖𝕟 𝔻𝕚𝕣𝕖𝕔𝕥𝕠𝕣𝕪", bg="darkred", fg="black", font=("Arial", 13), relief="ridge", bd=2, command=open_directory)
open_directory_button.place(x=480, y=160, width=120, height=30)
open_directory_button.bind("<Enter>", lambda event: on_hover(open_directory_button))
open_directory_button.bind("<Leave>", lambda event: on_leave(open_directory_button))

set_prefix_button = tk.Button(root, text="𝗦𝗲𝘁 𝗣𝗿𝗲𝗳𝗶𝘅", bg="darkred", fg="black", font=("Arial", 13), relief="ridge", bd=2, command=set_prefix)
set_prefix_button.place(x=480, y=235, width=120, height=30)
set_prefix_button.bind("<Enter>", lambda event: on_hover(set_prefix_button))
set_prefix_button.bind("<Leave>", lambda event: on_leave(set_prefix_button))

set_token_button = tk.Button(root, text="𝔸𝕔𝕔 𝕋𝕠𝕜𝕖𝕟", bg="darkred", fg="black", font=("Arial", 13), relief="ridge", bd=2, command=set_token)
set_token_button.place(x=480, y=275, width=120, height=30)
set_token_button.bind("<Enter>", lambda event: on_hover(set_token_button))
set_token_button.bind("<Leave>", lambda event: on_leave(set_token_button))

log_button = tk.Button(root, text="𝕃𝕠𝕘", bg="darkred", fg="black", font=("Arial", 13), relief="ridge", bd=2)
log_button.place(x=480, y=315, width=120, height=30)
log_button.bind("<Enter>", lambda event: on_hover(log_button))
log_button.bind("<Leave>", lambda event: on_leave(log_button))

main_button_label = tk.Label(root, text="𝕊𝕖𝕝𝕗𝕓𝕠𝕥 𝔸𝕔𝕥𝕚𝕠𝕟𝕤", fg="black", bg="red", font=("Arial", 14))
main_button_label.place(x=475, y=50)

config_button_label = tk.Label(root, text="𝕊𝕖𝕝𝕗𝕓𝕠𝕥 𝕊𝕖𝕥𝕥𝕚𝕟𝕘𝕤", fg="black", bg="red", font=("Arial", 14))
config_button_label.place(x=475, y=202)

separator = tk.Frame(root, bg='darkred', height=2)
separator.place(relx=0.75, rely=0.13, anchor='nw', width=150)

separator = tk.Frame(root, bg='darkred', height=2)
separator.place(relx=0.75, rely=0.48, anchor='nw', width=150)

separator = tk.Frame(root, bg='darkred', height=2)
separator.place(relx=0.75, rely=0.515, anchor='nw', width=150)

separator = tk.Frame(root, bg='darkred', height=2)
separator.place(relx=0.75, rely=0.87, anchor='nw', width=150)

sys.stdout = RedirectText(log_text)
sys.stderr = RedirectText(log_text)

print("GUI started...\nThe Selbot is now ready to start!")

root.mainloop()