import os
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog



# Now import other modules
import config
import downloader
import folder

# ---------- global variables -------------------------------------------------------------
def main():
    root = tk.Tk()
    root.geometry('1200x600')
    root.title('Downloader')
    root.resizable(False, False)
    config.configinit()

    mode_var = tk.StringVar(value='Video')

    # program internal vars
    # we get the current directory the program is in so that we know where to download
    # eg, the program is in documents/program, we want the program to download to that directory, not users/nathanlin/system_files or smthn
    selected_folder_var = tk.StringVar(value=os.getcwd())

    # program internal vars
    program_folder = os.getcwd()


    # ---- layout frames -------------------------------------------------------
    mainframe = tk.Frame(root)
    mainframe.pack(fill='both', expand=True)


    # left side (controls)
    entryframe = tk.Frame(mainframe, width=400, padx=10, pady=10)
    entryframe.pack(side='left', fill='y', expand=False)
    entryframe.pack_propagate(False)

    # right Side (Folders) - Takes remaining space
    folderframe = tk.Frame(mainframe, bd=2, relief='sunken', bg='white')
    folderframe.pack(side='right', fill='both', expand=True, padx=10, pady=10)






    # ---- GUI ----------------------------------------------------

    # 1. Links (Top Left)
    link_label = tk.Label(entryframe, text='Links (one per line):', font=('Arial', 10, 'bold'))
    link_label.pack(anchor='w')
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



    menubar = tk.Menu(root)
    root.config(menu=menubar)
    config_menu = tk.Menu(menubar, tearoff=0)
    config_menu.add_command(label='Video Options', command=config.open_video_config)
    config_menu.add_separator()
    config_menu.add_command(label='Audio Options', command=config.open_audio_config)
    config_menu.add_cascade(label='Config', menu=config_menu)



    # config_row = tk.Frame(ctrl_box)
    # config_row.pack(fill='x', pady=5)
    # video_config_button = tk.Button(config_row, text='Video Opts', command=config.open_video_config)
    # video_config_button.pack(side='left', fill='x', expand=True, padx=1)
    # audio_config_button = tk.Button(config_row, text='Audio Opts', command=config.open_audio_config)
    # audio_config_button.pack(side='left', fill='x', expand=True, padx=1)

    load_failed_links_button = tk.Button(ctrl_box, text='Load Failed Links',
                                         command=lambda: downloader.load_undownloaded_links(link_entry, log))
    load_failed_links_button.pack(fill='x', pady=5)

    download_button = tk.Button(ctrl_box, text='Download', height=2, width=3,
                               command=lambda: downloader.download(
                                   link_entry, selected_folder_var, mode_var,
                                   config.video_format_var, config.video_quality_var, config.audio_format_var,
                                   log, disable_buttons, enable_buttons
                               ))
    download_button.pack(fill='x', pady=5)

    clear_failed_links_button = tk.Button(ctrl_box, text='Clear Failed Links',
                                         command=lambda: downloader.clear_undownloaded_links(log))
    clear_failed_links_button.pack(fill='x', pady=5)

    # 4. Log (Bottom Left)
    logframe = tk.Frame(entryframe)
    log_label = tk.Label(entryframe, text='Log:', font=('Arial', 10, 'bold'))
    log_label.pack(anchor='w')

    log_scroll = tk.Scrollbar(logframe)
    log_scroll.pack(side='right', fill='y')
    log_text = tk.Text(logframe, height=8, bd=2, relief='groove', bg='#f0f0f0', yscrollcommand=log_scroll.set)
    log_text.pack(fill='both', expand=True)
    log_scroll.config(command=log_text.yview)
    logframe.pack(fill='both', expand=True)

    # credits_label = tk.Label(entryframe, text='Pepducky© 2025-12-12')
    # credits_label.pack()
    #
    # credits_button = tk.Button(entryframe, text='credits', command = credits_module.playcredits)
    # credits_button.pack()
    # 5. Folder Tree (Right Side)
    folder_canvas = tk.Canvas(folderframe, bg='white')
    folder_scroll = tk.Scrollbar(folderframe, orient='vertical', command=folder_canvas.yview)
    folder_canvas.config(yscrollcommand=folder_scroll.set)

    folder_scroll.pack(side='right', fill='y')
    folder_canvas.pack(side='left', fill='both', expand=True)

    tree_inner = tk.Frame(folder_canvas, bg='white')
    canvas_win_id = folder_canvas.create_window((0, 0), window=tree_inner, anchor='nw')

    # ---- logging ------------------------------------------------------
    def log(msg):
        log_text.insert('end', msg + '\n')
        # tk.see scrolls to a position in a text widget, in this case the bottom of the text widget
        log_text.see('end')

    def update_scroll(e):
        folder_canvas.config(scrollregion=folder_canvas.bbox('all'))


    def disable_buttons():
        buttons = [video_opt_button, audio_opt_button, download_button, load_failed_links_button]
        for i in buttons:
            i.config(state=tk.DISABLED)
        menubar.entryconfig("File", state=tk.DISABLED)


    def enable_buttons():
        buttons = [video_opt_button, audio_opt_button, download_button, load_failed_links_button]
        for i in buttons:
            i.config(state=tk.NORMAL)
        menubar.entryconfig("File", state=tk.NORMAL)


    def refresh_folders():
        #destroy all widgets in tree_inner
        for widget in tree_inner.winfo_children():
            widget.destroy()
        folder.update_folders(program_folder, tree_inner, selected_folder_var, root, log)


    def create_new_folder():
        folder_name = simpledialog.askstring("New Folder", "Enter folder name:")
        if folder_name:
            folder.create_folder(folder_name, program_folder, log)
            refresh_folders()


    # Add create folder button at the top of the folder frame
    folder_controls = tk.Frame(folderframe, bg='white')
    folder_controls.pack(side='top', fill='x', padx=5, pady=5)


    plus_icon = tk.PhotoImage(file='plus_sign.png')
    create_folder_button = tk.Button(folder_controls, image=plus_icon, command=create_new_folder)
    create_folder_button.image = plus_icon  # Keep a reference to prevent garbage collection
    create_folder_button.pack(side='left')

    tree_inner.bind('<Configure>', update_scroll)

    # Populate the folder tree
    refresh_folders()

    log('Ready.')
    root.mainloop()

main()