#config.py
#this module manages the configuration settings for video and audio downloads
#it stores the user's preferences for format and quality in stringvars that other modules can access
#when the user opens a config window, they can select their preferred format and quality using radiobuttons
#the settings are saved when the user closes the config window
#these settings are passed to yt-dlp when downloading



import tkinter as tk
import os

# config variables
# these are the settings for the downloader.
# strinvariables are changable by tkinter modules
# these will be accessed in main

audio_format_var = None
video_format_var = None
video_quality_var = None

#this function creates the stringvars with default values
#this needs to be called after the root window is created in main
# stringvars need a root window to exist
def configinit():
    # global allows us to modify variables outside the function scope
    global audio_format_var, video_format_var, video_quality_var
    audio_format_var = tk.StringVar(value='mp3')
    video_format_var = tk.StringVar(value='mp4')
    video_quality_var = tk.StringVar(value='1080')

#this function opens the audio config window
#it creates a new window with radiobuttons for selecting audio format
#options are automatically saved
#the save and close button is for placebo
def open_audio_config():
    top = tk.Toplevel()
    top.geometry('400x600')
    top.title('Audio Config')
    top.configure(bg='#2d2d2d')

    title = tk.Label(top, text='Format:', bg='#2d2d2d', fg='#dfdfdf')
    title.pack(pady=5)

    # create radiobuttons for each audio format
    # variable sets the stringvar to change when the radiobutton is selected
    # value sets the value to set the stringvar to when the radiobutton is selected

    mp3 = tk.Radiobutton(top, text='mp3', variable=audio_format_var, value='mp3', bg='#2d2d2d', fg='#dfdfdf')
    mp3.pack(anchor='w', padx=20, pady=20)

    aac = tk.Radiobutton(top, text='aac', variable=audio_format_var, value='aac', bg='#2d2d2d', fg='#dfdfdf')
    aac.pack(anchor='w', padx=20, pady=20)

    wav = tk.Radiobutton(top, text='wav', variable=audio_format_var, value='wav', bg='#2d2d2d', fg='#dfdfdf')
    wav.pack(anchor='w', padx=20, pady=20)

    m4a = tk.Radiobutton(top, text='m4a', variable=audio_format_var, value='m4a', bg='#2d2d2d', fg='#dfdfdf')
    m4a.pack(anchor='w', padx=20, pady=20)

    # create a button to close the window
    # .destroy destroys the window
    close = tk.Button(top, text='Save and Close', command=top.destroy, bg='#404040', fg='#ffffff')
    close.pack(anchor='n', pady=150)


#this function opens the video config window
#it creates a new window with radiobuttons for selecting video format and quality
#when the user closes the window, the settings are automatically saved in the stringvars
def open_video_config():
    top = tk.Toplevel()
    top.title('Video Config')
    top.geometry('400x600')
    top.configure(bg='#2d2d2d')



    title = tk.Label(top, text='Format:', bg='#2d2d2d', fg='#dfdfdf')
    title.pack(pady=5)

    # create radiobuttons for each video format
    # variable sets the stringvar to change when the radiobutton is selected
    # value sets the value to set the stringvar to when the radiobutton is selected
    mp4 = tk.Radiobutton(top, text='mp4', variable=video_format_var, value='mp4', bg='#2d2d2d', fg='#dfdfdf')
    mp4.pack(anchor='w', padx=20)

    mkv = tk.Radiobutton(top, text='mkv', variable=video_format_var, value='mkv', bg='#2d2d2d', fg='#dfdfdf')
    mkv.pack(anchor='w', padx=20)

    webm = tk.Radiobutton(top, text='webm', variable=video_format_var, value='webm', bg='#2d2d2d', fg='#dfdfdf')
    webm.pack(anchor='w', padx=20)

    avi = tk.Radiobutton(top, text='avi', variable=video_format_var, value='avi', bg='#2d2d2d', fg='#dfdfdf')
    avi.pack(anchor='w', padx=20)

    qualityTitle = tk.Label(top, text='Quality:', bg='#2d2d2d', fg='#dfdfdf')
    qualityTitle.pack(pady=5)




    # create radiobuttons for each video quality
    best = tk.Radiobutton(top, text='best', variable=video_quality_var, value='best', bg='#2d2d2d', fg='#dfdfdf')
    best.pack(anchor='w', padx=20)

    qual1 = tk.Radiobutton(top, text='2160', variable=video_quality_var, value='2160', bg='#2d2d2d', fg='#dfdfdf')
    qual1.pack(anchor='w', padx=20)

    qual2 = tk.Radiobutton(top, text='1080', variable=video_quality_var, value='1080', bg='#2d2d2d', fg='#dfdfdf')
    qual2.pack(anchor='w', padx=20)

    qual3 = tk.Radiobutton(top, text='720', variable=video_quality_var, value='720', bg='#2d2d2d', fg='#dfdfdf')
    qual3.pack(anchor='w', padx=20)

    qual4 = tk.Radiobutton(top, text='480', variable=video_quality_var, value='480', bg='#2d2d2d', fg='#dfdfdf')
    qual4.pack(anchor='w', padx=20)

    close = tk.Button(top, text='Save and Close', command=top.destroy, bg='#404040', fg='#ffffff')
    close.pack(anchor='n', pady=150)