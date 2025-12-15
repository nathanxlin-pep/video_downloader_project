#main.py
#this program is a video and audio downloader with a gui
#the user pastes links into a text box and selects a download folder from a folder tree
#the user can choose between video or audio mode, and configure format and quality settings
#when the user clicks download, the program downloads the links in the background using threading
#while downloading, the program disables all important butttons to prevent inconsistencies in downloading.
#failed downloads are saved to a file so the user can load them back in and retry them later
#the program logs download progress and errors to a log box at the bottom




#import os to get the directory the program is in
import os
#import other stuff
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import config
import downloader
import folder


def main():
    # ---- functions ------------------------------------------------------'
    # this function logs a message to the log text widget
    # it takes a message as a parameter
    def log(msg):
        # .config configures a widget
        # state=tk.NORMAL makes the text widget editable
        # log_text is disabled by default
        log_text.config(state=tk.NORMAL)
        # .insert inserts text into a text widget at a position
        # 'end' is the end of the text widget
        # we add a newline to the end of the message
        log_text.insert('end', msg + '\n')
        # .see scrolls the text widget to a position
        # this makes sure the user can see the new message
        log_text.see('end')
        #state=tk.DISABLED makes the text widget read only
        log_text.config(state=tk.DISABLED)
        #theoretically the user can edit the text in 0.02 seconds

    # this function updates the scroll region of the folder canvas
    # https://stackoverflow.com/questions/16188420/tkinter-scrollbar-for-frame

    def update_scroll(e):
        # scrollregion sets the scrollable area of the canvas
        # .bbox gets the bounding box of all the widgets in the canvas
        folder_canvas.config(scrollregion=folder_canvas.bbox('all'))

    # this function disables the buttons
    # it prevents the user from messing with the settings while downloading
    def disable_buttons():
        # create a list of buttons to disable
        # tk objects can be referenced in lists
        buttons = [video_opt_button, audio_opt_button, download_button, load_failed_links_button, clear_failed_links_button]
        #iterate over the buttons
        for i in buttons:
            # .config configures a widget
            # state=tk.DISABLED makes the button unclickable
            i.config(state=tk.DISABLED)
        # .entryconfig changes parameters in a menubar
        # this disables the config menu
        menubar.entryconfig("Config", state=tk.DISABLED)


    # this function enables the buttons
    # it allows the user to use the buttons after downloading
    def enable_buttons():
        buttons = [video_opt_button, audio_opt_button, download_button, load_failed_links_button, clear_failed_links_button]
        for i in buttons:
            i.config(state=tk.NORMAL)
        # state=tk.NORMAL makes the button clickable
        # it's referencing a var in tkinter called NORMAL with a value of normal
        menubar.entryconfig("Config", state=tk.NORMAL)


    # this function refreshes the folder tree
    # it destroys all the widgets in the tree and recreates them
    def refresh_folders():
        # .winfo_children gets all the widgets in a parent widget
        for widget in tree_inner.winfo_children():
            widget.destroy()
        # update the folders
        folder.update_folders(program_folder, tree_inner, selected_folder_var, root, log)

    # this function creates a new folder in the program folder
    # it prompts the user for a folder name and creates the folder
    def create_new_folder():
        # simpledialog.askstring prompts the user for a string input
        folder_name = simpledialog.askstring("New Folder", "Enter folder name:")
        if folder_name:
            # create the folder ni the program folder
            folder.create_folder(folder_name, program_folder, log)
            # refresh the folder tree to show the new folder
            refresh_folders()








    # ---------- global variables -------------------------------------------------------------
    # tk.Tk creates the root window
    # the root window is the main window of the program
    root = tk.Tk()
    root.geometry('1200x600')
    root.title('Downloader')

    #root.resizable makes it so the user can not resize the window in a cardinal direction
    #in this case, the user can not resize the window at all.
    #style choice
    root.resizable(False, False)
    root.configure(bg='#2d2d2d')

    #make the stringvariables AFTER the root window has been established.
    #strinvars can not exist without a root window i guess
    config.configinit()

    mode_var = tk.StringVar(value='Video')

    # program internal vars
    # we start off with a default download location of the program folder.
    # os.getcwd returns where in the computer the folder housing the program is stored
    selected_folder_var = tk.StringVar(value=os.getcwd())

    #get the folder the program is in in order to use in updating the folder tree
    #it is seperate because we want a constant.
    program_folder = os.getcwd()

    # ---- layout frames -------------------------------------------------------
    mainframe = tk.Frame(root, bg='#2d2d2d')#bg makes the background a hex color
    mainframe.pack(fill='both', expand=True)#expand allows the frame to expand to fit when packed.
                                            #think of it as a balloon in a box

    # left side (controls)
    entryframe = tk.Frame(mainframe, width=400, padx=10, pady=10, bg='#2d2d2d')
    entryframe.pack(side='left', fill='y', expand=False)
    entryframe.pack_propagate(False)

    # right Side (Folders) - Takes remaining space
    folderframe = tk.Frame(mainframe, bd=2, relief='sunken', bg='#2d2d2d')
    folderframe.pack(side='right', fill='both', expand=True, padx=10, pady=10)

    # ---- GUI ----------------------------------------------------

    # 1. Links (Top Left)
    link_label = tk.Label(entryframe, text='Links (one per line):', font=('Arial', 10, 'bold'), bg='#2d2d2d', fg='#dfdfdf')
    #anchor makes the label stick to the west side of the screen, and expand from there.
    link_label.pack(anchor='w')


    link_entry = tk.Text(entryframe, height=8, bd=2, relief='groove', bg='#3c3c3c', fg='#dfdfdf', insertbackground='#dfdfdf')
    link_entry.pack(fill='x', pady=(0, 10))

    # 2. Settings (Middle Left)
    ctrl_box = tk.LabelFrame(entryframe, text='Settings', padx=5, pady=5, bg='#2d2d2d', fg='#dfdfdf')
    ctrl_box.pack(fill='x', pady=5)

    #3. Settings menubar
    #establish menubar
    menubar = tk.Menu(root)
    root.config(menu=menubar)

    #tearoff is a boolean value represented by 1 or 0 that allows the menu to be torn off the screen
    #into a seperate window. this is disabled by 0
    config_menu = tk.Menu(menubar, tearoff=0)
    config_menu.add_command(label='Video Options', command=config.open_video_config)
    config_menu.add_separator()
    config_menu.add_command(label='Audio Options', command=config.open_audio_config)
    menubar.add_cascade(label='Config', menu=config_menu)


    #Create a area for the buttons
    button_label = tk.Label(ctrl_box, text='Mode:', bg='#2d2d2d', fg='#dfdfdf')
    #everything is anchored to the west here in order to make everything consistent
    #these are all in the entryframe.
    button_label.pack(anchor='w')
    video_opt_button = tk.Radiobutton(ctrl_box, text='Video', variable=mode_var, value='Video', bg='#2d2d2d', fg='#dfdfdf', selectcolor='#505050', command=lambda: config_menu.entryconfig('Video Options', state=tk.NORMAL))
    video_opt_button.pack(anchor='w', padx=10)
    audio_opt_button = tk.Radiobutton(ctrl_box, text='Audio Only', variable=mode_var, value='Audio', bg='#2d2d2d', fg='#dfdfdf', selectcolor='#505050', command=lambda: config_menu.entryconfig('Video Options', state=tk.DISABLED))
    audio_opt_button.pack(anchor='w', padx=10)

    load_failed_links_button = tk.Button(ctrl_box, text='Load Failed Links',
                                         command=lambda: downloader.load_undownloaded_links(link_entry, log),
                                         bg='#404040', fg='#ffffff')
    load_failed_links_button.pack(fill='x', pady=5)

    download_button = tk.Button(ctrl_box, text='Download', height=2, width=3,
                               command=lambda: downloader.download(
                                   link_entry, selected_folder_var, mode_var,
                                   config.video_format_var, config.video_quality_var, config.audio_format_var,
                                   log, disable_buttons, enable_buttons
                               ), bg='#404040', fg='#ffffff')
    download_button.pack(fill='x', pady=5)

    clear_failed_links_button = tk.Button(ctrl_box, text='Clear Failed Links',
                                         command=lambda: downloader.clear_undownloaded_links(log),
                                         bg='#404040', fg='#ffffff')
    clear_failed_links_button.pack(fill='x', pady=5)

    # 4. Log (Bottom Left)
    logframe = tk.Frame(entryframe, bg='#2d2d2d')
    log_label = tk.Label(entryframe, text='Log:', font=('Arial', 10, 'bold'), bg='#2d2d2d', fg='#dfdfdf')
    log_label.pack(anchor='w')

    log_scroll = tk.Scrollbar(logframe, bg='#404040')
    log_scroll.pack(side='right', fill='y')
    log_text = tk.Text(logframe, height=8, bd=2, relief='groove', bg='#3c3c3c', fg='#dfdfdf', insertbackground='#dfdfdf', yscrollcommand=log_scroll.set, state=tk.DISABLED)
    log_text.pack(fill='both', expand=True)
    log_scroll.config(command=log_text.yview)
    logframe.pack(fill='both', expand=True)

    # 5. Folder Tree (Right Side)
    folder_canvas = tk.Canvas(folderframe, bg='#2d2d2d')
    folder_scroll = tk.Scrollbar(folderframe, orient='vertical', command=folder_canvas.yview, bg='#404040')
    folder_canvas.config(yscrollcommand=folder_scroll.set)

    folder_scroll.pack(side='right', fill='y')
    folder_canvas.pack(side='left', fill='both', expand=True)

    tree_inner = tk.Frame(folder_canvas, bg='#2d2d2d')
    canvas_win_id = folder_canvas.create_window((0, 0), window=tree_inner, anchor='nw')



    # Add create folder button at the top of the folder frame
    folder_controls = tk.Frame(folderframe, bg='#2d2d2d')
    folder_controls.pack(side='top', fill='x', padx=5, pady=5)

    plus_icon = tk.PhotoImage(file='plus_sign.png')
    create_folder_button = tk.Button(folder_controls, image=plus_icon, command=create_new_folder, bg='#404040')
    create_folder_button.image = plus_icon
    create_folder_button.pack(side='left')

    tree_inner.bind('<Configure>', update_scroll)

    # Populate the folder tree
    refresh_folders()

    log('Ready.')
    root.mainloop()

main()