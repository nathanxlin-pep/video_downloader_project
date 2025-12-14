import tkinter as tk
import os
# config variables
# these are the settings for the downloader.
# strinvariables are changable by tkinter modules
# these will be accessed in main

audio_format_var = None
video_format_var = None
video_quality_var = None


def configinit():
    global audio_format_var, video_format_var, video_quality_var
    audio_format_var = tk.StringVar(value='mp3')
    video_format_var = tk.StringVar(value='mp4')
    video_quality_var = tk.StringVar(value='1080')

def open_audio_config():
    top = tk.Toplevel()
    top.geometry('400x600')
    top.title('Audio Config')
    title = tk.Label(top, text='Format:')
    title.pack(pady=5)


    mp3 = tk.Radiobutton(top, text='mp3', variable=audio_format_var, value='mp3')
    mp3.pack(anchor='w', padx=20, pady=20)

    aac = tk.Radiobutton(top, text='aac', variable=audio_format_var, value='aac')
    aac.pack(anchor='w', padx=20, pady=20)

    wav = tk.Radiobutton(top, text='wav', variable=audio_format_var, value='wav')
    wav.pack(anchor='w', padx=20, pady=20)

    m4a = tk.Radiobutton(top, text='m4a', variable=audio_format_var, value='m4a')
    m4a.pack(anchor='w', padx=20, pady=20)

    close = tk.Button(top, text='Save and Close', command=top.destroy)
    close.pack(anchor='n', pady = 150)


def open_video_config():
    top = tk.Toplevel()
    top.title('Video Config')
    top.geometry('400x600')
    title = tk.Label(top, text='Format:')
    title.pack(pady=5)


    mp4 = tk.Radiobutton(top, text='mp4', variable=video_format_var, value='mp4')
    mp4.pack(anchor='w', padx=20)

    mkv = tk.Radiobutton(top, text='mkv', variable=video_format_var, value='mkv')
    mkv.pack(anchor='w', padx=20)

    webm = tk.Radiobutton(top, text='webm', variable=video_format_var, value='webm')
    webm.pack(anchor='w', padx=20)

    avi = tk.Radiobutton(top, text='avi', variable=video_format_var, value='avi')
    avi.pack(anchor='w', padx=20)




    qualityTitle = tk.Label(top, text='Quality:')
    qualityTitle.pack(pady=5)

    best = tk.Radiobutton(top, text='best', variable=video_quality_var, value='best')
    best.pack(anchor='w', padx=20)

    qual1 = tk.Radiobutton(top, text='2160', variable=video_quality_var, value='2160')
    qual1.pack(anchor='w', padx=20)

    qual2 = tk.Radiobutton(top, text='1080', variable=video_quality_var, value='1080')
    qual2.pack(anchor='w', padx=20)

    qual3 = tk.Radiobutton(top, text='720', variable=video_quality_var, value='720')
    qual3.pack(anchor='w', padx=20)

    qual4 = tk.Radiobutton(top, text='480', variable=video_quality_var, value='480')
    qual4.pack(anchor='w', padx=20)

    close = tk.Button(top, text='Save and Close', command=top.destroy)
    close.pack(anchor='n', pady=150)