import os
import tkinter as tk
from tkinter import simpledialog


# program internal vars
program_folder = os.getcwd()

#this function lists the directory paths of folders in a directory
def list_subfolders(directory_path, log_func):
   subfolders = []
   #try except tries a function. in case of an error executing the code, another function is executed

   try:
      with os.scandir(directory_path) as entries: #scandir
         for entry in entries:
            if entry.is_dir() and entry.name not in ['__pycache__', 'venv', '.idea', '.venv', 'assets', 'stars.png', 'stars']:
               subfolders.append([entry.name, entry.path])
   except Exception as e:
      #you can use a function as a parameter. we will treat log_func as a parameter. log_func will be a
      #parameter in one function, which will be used in another function with log_func as a parameter.
      #this continues on until we reach main where we use the actual log function instead of parameters from the parent function
      log_func("Error listing subfolders: " + str(e))
   #return the list to be accessible to other functions
   return subfolders


def list_contents(directory_path, log_func):
   items = []
   try:
      with os.scandir(directory_path) as entries:
         for entry in entries:
            if not entry.is_dir():
               items.append([entry.name, entry.path])
   except Exception as e:
      log_func("Error listing contents: " + str(e))
   return items


def load_universal_widget(parent, name, extension):

   row = tk.Frame(parent)
   row.pack(fill="x", anchor="n", pady=2)

   lbl = tk.Label(row, text=name + extension)
   lbl.pack(side="left")

def create_new_folder(log_func, parent, directory, root, selected_folder_var):
   folder_name = simpledialog.askstring("New Folder", "Enter folder name:")
   if folder_name:
      create_folder(folder_name, directory, log_func)
      # Just add the new folder widget to the existing list
      new_folder_path = os.path.join(directory, folder_name)
      load_folder_widget(parent, folder_name, new_folder_path, selected_folder_var, root, log_func)

def load_folder_widget(parent, name, directory, selected_folder_var, root, log_func, extension=""):
   try:
      if os.path.isdir(directory):
         def expand():
            top = tk.Toplevel(root)
            top.geometry('400x600')
            top.title('Folder:' + name)

            new_folder = tk.Button(top, text='create new folder', command=lambda: create_new_folder(log_func, top, directory, root, selected_folder_var))
            new_folder.pack(side="right")

            folders = list_subfolders(directory, log_func)
            items = list_contents(directory, log_func)

            for folder_name, folder_path in folders:
               load_folder_widget(top, folder_name, folder_path, selected_folder_var, root, log_func)

            for item_name, item_path in items:
               item_ext = os.path.splitext(item_name)[1]
               load_universal_widget(top, os.path.splitext(item_name)[0], item_ext)


         row = tk.Frame(parent)
         row.pack(fill="x", anchor="w", pady=2)

         lbl = tk.Label(row, text=name)
         lbl.pack(side="left")

         rb = tk.Radiobutton(row, variable=selected_folder_var, value=directory)
         rb.pack(side="left", padx=5)

         arrow_btn = tk.Button(row, text="►", width=2, command=expand)
         arrow_btn.pack(side="left", padx=5)
      else:
         row = tk.Frame(parent)
         row.pack(fill="x", anchor="n", pady=2)

         lbl = tk.Label(row, text=name + extension)
         lbl.pack(side="left")

   except Exception as e:
      log_func('Error creating file widget: ' + str(e))

def create_folder(name, path, log_func):
   try:
      full_path = os.path.join(path, name)
      os.makedirs(full_path)
      log_func("Folder created: " + full_path)
   except Exception as e:
      log_func("Error creating folder: " + str(e))


def update_folders(directory, parent, selected_folder_var, root, log_func):
   folders = list_subfolders(directory, log_func)
   for folder_name, folder_path in folders:
      load_folder_widget(parent, folder_name, folder_path, selected_folder_var, root, log_func)