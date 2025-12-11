import os
import tkinter as tk
from tkinter import simpledialog, messagebox
from main import log

selected_folder_var = tk.StringVar(value=os.getcwd())
global root
def list_subfolders(directory_path):
    subfolders = []
    try:
        with os.scandir(directory_path) as entries:
            for entry in entries:
                if entry.is_dir():
                    subfolders.append([entry.name, entry.path])
    except Exception as e:
        log("Error listing subfolders: " +  e)
    return subfolders


def list_contents(directory_path):
    items = []
    try:
        with os.scandir(directory_path) as entries:
            for entry in entries:
                if not entry.is_dir():
                    items.append([entry.name, entry.path])
    except Exception as e:
        log("Error listing contents:" + e)
    return items


def create_universal_widget(parent, name, path):
    row = tk.Frame(parent)
    row.pack(fill="x", anchor="w", pady=2)

    lbl = tk.Label(row, text=name).pack(side="left")
    lbl.pack()



def create_folder_widget(parent, name, path):
    row = tk.Frame(parent)
    row.pack(fill="x", anchor="w", pady=2)

    rb = tk.Radiobutton(row, variable=selected_folder_var, value=path)
    rb.pack(side="right", padx=5)

    lbl = tk.Label(row, text=name).pack(side="left")
    lbl.pack()

    arrow_btn = tk.Button(row, text="▶", width=2)
    arrow_btn.pack(side="right", padx=5)


    expanded = False

    def expand():
        nonlocal path
        global expanded
        if not expanded:
            top = tk.Toplevel(root)
            top.geometry('900x600')

            expanded= True
            folders = list_subfolders(path)
            items = list_contents(path)
            for name, path in folders:
                create_folder_widget(top, name, path)
            for name, path in items:
                create_universal_widget(top, name, path)





    arrow_btn.config(command=expand)


