




import os
import threading
import tkinter as tk
root = tk.Tk()
from tkinter import filedialog, messagebox
import config
import downloader


# ---------- global variables -------------------------------------------------------------

root.geometry('1200x600')
root.title('Downloader')

mode_var = tk.StringVar(value='Video')

# program internal vars
# we get the current directory the program is in so that we know where to download
# eg, the program is in documents/program, we want the program to download to that directory, not users/nathanlin/system_files or smthn
program_folder = os.getcwd()

# ---- layout frames -------------------------------------------------------
mainframe = tk.Frame(root).pack()

# left side (controls)
entryframe = tk.Frame(mainframe, width=400, padx=10, pady=10)
entryframe.pack(side='left', fill='y', expand=False)
entryframe.pack_propagate(False)  # forces this frame to stay the same width



# right Side (Folders) - Takes remaining space
folderframe = tk.Frame(mainframe, bd=2, relief='sunken', bg='white')
folderframe.pack(side='right', fill='both', expand=True, padx=10, pady=10)
#fill makes a widget expand to a specified cardinal direction, in this case being x and y.


# ---- GUI ----------------------------------------------------

# 1. Links (Top Left)
link_label = tk.Label(entryframe, text='Links (one per line):', font=('Arial', 10, 'bold'))
link_label.pack(anchor='w')
# Added border and distinct background so you can see it
link_entry = tk.Text(entryframe, height=8, bd=2, relief='groove', bg='#f8f8f8')
link_entry.pack(fill='x', pady=(0, 10))

# 2. Settings (Middle Left)
ctrl_box = tk.LabelFrame(entryframe, text='Settings', padx=5, pady=5)
ctrl_box.pack(fill='x', pady=5)

button_label = tk.Label(ctrl_box, text='Mode:')
button_label.pack(anchor='w')
video_opt_button = tk.Radiobutton(ctrl_box, text='Video', variable=mode_var, value='Video')
video_opt_button.pack(anchor='w', padx=10)
audio_opt_button = tk.Radiobutton(ctrl_box, text='Audio Only', variable=mode_var, value='Audio')
audio_opt_button.pack(anchor='w', padx=10)

config_row = tk.Frame(ctrl_box)
config_row.pack(fill='x', pady=5)
video_config_button = tk.Button(config_row, text='Video Opts', command=config.open_video_config)
video_config_button.pack(side='left', fill='x', expand=True, padx=1)
audio_config_button = tk.Button(config_row, text='Audio Opts', command=config.open_audio_config)
audio_config_button.pack(side='left', fill='x', expand=True, padx=1)

load_failed_links_button = tk.Button(ctrl_box, text='Load Failed Links', command=downloader.load_undownloaded_links)
load_failed_links_button.pack(fill='x', pady=5)

download_button = tk.Button(ctrl_box, text='Download', height=2, width=3, command=downloader.download)
download_button.pack(fill='x', pady=5)

# 4. Log (Bottom Left)
logframe = tk.Frame(entryframe)
tk.Label(entryframe, text='Log:', font=('Arial', 10, 'bold')).pack(anchor='w')

log_scroll = tk.Scrollbar(logframe)
log_scroll.pack(side='right', fill='y')
log_text = tk.Text(logframe, height=8, bd=2, relief='groove', state='normal', bg='#f0f0f0', yscrollcommand = log_scroll.set)
log_text.pack(fill='both', expand=True)
log_text.config(state=tk.DISABLED)
logframe.pack(fill='both')

# 5. Folder Tree (Right Side)
folder_canvas = tk.Canvas(folderframe, bg='white')
folder_scroll = tk.Scrollbar(folderframe, orient='vertical', command=folder_canvas.yview)
folder_canvas.config(yscrollcommand=folder_scroll.set)

folder_scroll.pack(side='right', fill='y')
folder_canvas.pack(side='left', fill='both', expand=True)

tree_inner = tk.Frame(folder_canvas, bg='white')
# This ID is needed to resize the window later
canvas_win_id = folder_canvas.create_window((0, 0), window=tree_inner, anchor='nw')



# ---- logging------------------------------------------------------
def log(msg):
    log_text.insert('end', msg + '\n')
    #tk.see scrolls to a position in a text widget, in this case the bottom of the text widget
    log_text.see('end')



def load_failed():
    try:
        with open('undownloaded.txt', 'r') as f:
            link_entry.delete('1.0', 'end')
            link_entry.insert('1.0', f.read())
    except:
        log('No undownloaded.txt found.')





def update_scroll(e):
    folder_canvas.config(scrollregion=folder_canvas.bbox('all'))


tree_inner.bind('<Configure>', update_scroll)



log('Ready.')
root.mainloop()