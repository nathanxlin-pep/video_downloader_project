
#folder.py
#this module manages the folder tree display and folder operations
#it scans directories and creates widgets for each folder with a radiobutton to select it and a button to expand it
#when the user expands a folder, it opens a new window showing the subfolders and files inside
#the user can create new folders by clicking a button and entering a folder name
#it filters out system folders like __pycache__ and .git so they don't clutter the display




import os
import tkinter as tk
from tkinter import simpledialog

'''
this module has a ton of refrencing
we create paramaters that represent actual objects in main
the parameters are first filled in with parameters from the parent function and so on
when we get to main, where the function is referenced, actual variables are used, 
which then trickle down through the parameter referencing.
'''




# program internal vars
# os.getcwd gets the current folder the program is in
program_folder = os.getcwd()

#this function lists the directory paths of folders in a directory
#it takes a directory path and a log function as parameters
#it returns a list of lists, where each list contains the folder name and path
def list_subfolders(directory_path, log_func):
   #create a empty list to store the subfolders
   # lists store a number of values in a single referencable variable
   # the data inside can be accessed by indexes, from 0 representing the 1st element onwaards
   subfolders = []
   #try except tries a function. in case of an error executing the code, another function is executed
   try:
      # os.scandir scans a directory and returns an list of subdirectorypaths
      # with as assigns the result to a variable, entries
      # it automatically handles the opening and closing of the directory
      with os.scandir(directory_path) as entries: #scandir
         #for loops take a var, and assign it to a element in another variable
         #it then executes code for each time the varible is reassigned.
         for entry in entries:
            #entry.is_dir checks if the entry is a directory
            #entry.name gets the name of the entry
            #we check if the entry is a directory and if the name is not in the exclusion list
            #the exclusion list contains folders we dont want to display
            if entry.is_dir() and entry.name not in ['__pycache__', 'venv', '.idea', '.venv', 'assets', 'stars.png', 'stars', '.git']:
               # append the folder name and path to the subfolders list
               # entry.path gets the full path of the entry
               subfolders.append([entry.name, entry.path])
   except Exception as e:
      #you can use a function as a parameter. we will treat log_func as a parameter. log_func will be a
      #parameter in one function, which will be used in another function with log_func as a parameter.
      #this continues on until we reach main where we use the actual log function instead of parameters from the parent function
      log_func("Error listing subfolders: " + str(e))
   #return the list to be accessible to other functions
   return subfolders


#this function lists the directory paths of files in a directory
#it takes a directory path and a log function as parameters
#it returns a list of lists, where each list contains the file name and path
def list_contents(directory_path, log_func):
   #create a empty list to store the items
   items = []
   try:
      # os.scandir explained before
      # with as explained before
      with os.scandir(directory_path) as entries:
         for entry in entries:
            # if the entry is not a directory, its a file
            # computing power is cheap so i just copypasted the old forbidden list over
            if not entry.is_dir() and entry.name not in ['__pycache__', 'venv', '.idea', '.venv', 'assets', 'stars.png', 'stars', '.git']:
               items.append([entry.name, entry.path])
   except Exception as e:
      log_func("Error listing contents: " + str(e))
      # return the list to be accessible to other functions
   return items


#this function creates a widget for a file
#it takes a parent widget, the file name, and the file extension as parameters
#it creates a frame with a label that displays the file name and extension
def load_universal_widget(parent, name, extension):
   # create a frame to hold the label
   # bg sets the background color as a hex code
   row = tk.Frame(parent, bg='#2d2d2d')
   # fill="x" makes the widget expand along the x axis only
   # anchor="n" sticks the widget to the north side
   # pady specifies the minimum distance the widget can be from another in the y direction
   row.pack(fill="x", anchor="n", pady=2)

   # create a label with the file name and extension
   # fg sets the foreground color, which is the text color
   lbl = tk.Label(row, text=name + extension, bg='#2d2d2d', fg='#dfdfdf')
   # pack the label to the left side of the frame
   lbl.pack(side="left")


#this function creates a new folder file and a new folder widget in the directory and the folder viewer.
#it takes the log function, parent widget, directory path, root window, and selected folder variable as parameters
#the parameters will be continually refrenced by higher and higher functions until actual objects are used in main
#it prompts the user for a folder name and creates the folder
def create_new_folder(log_func, parent, directory, root, selected_folder_var):
   #simpledialog.askstring prompts the user for a string input
   #it returns the string the user entered
   folder_name = simpledialog.askstring("New Folder", "Enter folder name:")

   #detect empty prompt
   if folder_name:
      # create the folder
      create_folder(folder_name, directory, log_func)
      # Just add the new folder widget to the existing list
      # os.path.join joins the directory path and folder name into a full path string
      new_folder_path = os.path.join(directory, folder_name)
      #load the widget for the new folder
      load_folder_widget(parent, folder_name, new_folder_path, selected_folder_var, root, log_func)


#this function creates a widget for a folder or file
#it takes the parent widget, name, directory path, selected folder variable, root window, and log function as parameters
#extension is a optional parameter that defaults to a empty string
#it creates a frame with a label, radiobutton, and expand button for folders
#for files, it creates a frame with just a label
def load_folder_widget(parent, name, directory, selected_folder_var, root, log_func, extension=""):
   #try except explained before
   try:
      # os.path.isdir checks if the path is a directory
      if os.path.isdir(directory):
         # this function expands the folder and shows its contents in a new window
         # we define it inside load_folder_widget so it can access the variables
         def expand():
            # tk.Toplevel creates a new window
            # it takes the root window as a parameter
            # taking the root window as a parameter cloees the top when root is closed
            # prevents osu window closing
            top = tk.Toplevel(root)
            top.geometry('400x600')
            top.title('Folder:' + name)
            # .configure changes parameters of a widget
            # bg is the background color parameter
            top.configure(bg='#2d2d2d')

            # create a button to create a new folder
            # command is the function to run when the button is clicked
            # lambda allows us to pass parameters to the function
            new_folder = tk.Button(top, text='create new folder', command=lambda: create_new_folder(log_func, top, directory, root, selected_folder_var), bg='#404040', fg='#ffffff')
            new_folder.pack(side="right")

            # get the subfolders and files in the directory with previous functions
            folders = list_subfolders(directory, log_func)
            items = list_contents(directory, log_func)

            # iterate over the folders and create a widget for each
            # 2 variables over a 2d list makes each variable the first or second element in each constituent list
            for folder_name, folder_path in folders:
               load_folder_widget(top, folder_name, folder_path, selected_folder_var, root, log_func)

            # iterate over the files and create a widget for each
            for item_name, item_path in items:
               # os.path.splitext splits the file name and extension strings
               # [1] gets the extension
               item_ext = os.path.splitext(item_name)[1]
               # [0] gets the file name without the extension
               load_universal_widget(top, os.path.splitext(item_name)[0], item_ext)

         # create a frame to hold the label, radiobutton, and expand button
         row = tk.Frame(parent, bg='#2d2d2d')
         row.pack(fill="x", anchor="w", pady=2)

         #create a label with the folder name
         lbl = tk.Label(row, text=name, bg='#2d2d2d', fg='#dfdfdf')
         lbl.pack(side="left")

         # create a radiobutton to select the folder
         # variable is the stringvar to store the selected folder
         # value is the value to set the stringvar to when the radiobutton is selected
         # selectcolor is the color of the radiobutton when selected
         rb = tk.Radiobutton(row, variable=selected_folder_var, value=directory, bg='#2d2d2d', fg='#dfdfdf', selectcolor='#505050')
         rb.pack(side="left", padx=5)

         arrow_btn = tk.Button(row, text="►", width=2, command=expand, bg='#404040', fg='#ffffff')
         arrow_btn.pack(side="left", padx=5)
      else:
         # if the path is not a directory, its a file
         # create a frame with just a label
         row = tk.Frame(parent, bg='#2d2d2d')
         row.pack(fill="x", anchor="n", pady=2)

         lbl = tk.Label(row, text=name + extension, bg='#2d2d2d', fg='#dfdfdf')
         lbl.pack(side="left")

   except Exception as e:
      # log the error
      log_func('Error creating file widget: ' + str(e))


#this function creates a folder in the directory
#it takes the folder name, directory path, and log function as parameters
def create_folder(name, path, log_func):
   try:
      # os.path.join joins the directory path and folder name into a full path
      full_path = os.path.join(path, name)
      #os.makedirs makes the folder in the directory
      os.makedirs(full_path)
      # log the success
      log_func("Folder created: " + full_path)
   except Exception as e:
      # log the error
      log_func("Error creating folder: " + str(e))

#this function updates the folders in the parent widget
#it takes the directory path, parent widget, selected folder variable, root window, and log function as parameters
#it lists the subfolders and creates a widget for each
def update_folders(directory, parent, selected_folder_var, root, log_func):
   # get the subfolders in the directory
   folders = list_subfolders(directory, log_func)
   #iterate over the folders and create a widget for each.
   for folder_name, folder_path in folders:
      load_folder_widget(parent, folder_name, folder_path, selected_folder_var, root, log_func)