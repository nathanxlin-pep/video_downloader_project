#import stuff
import tkinter as tk
from tkinter import messagebox as Mb
import yt_dlp
import threading


#globalize all variables and widgets needed in this module of the program
global link_entry, selected_folder_var, mode_var, video_format_var, video_quality_var, audio_format_var, log_text

#globalize all buttons to turn them off to prevent spamming
global video_opt_button, audio_opt_button, video_config_button, audio_config_button


def log(msg):
    log_text.insert('end', msg + '\n')
    #tk.see scrolls to a position in a text widget, in this case the bottom of the text widget
    log_text.see('end')



def save_undownloaded_links(undownloaded_links):
    #the try keyword tries to execute the block of code written under it.
    # in case of a success, nothing happens unless the user specifies something to happen

    if not undownloaded_links:
       return # stops function by returning nothing
    try:
        #open opens a file in a certain way. <a> means to open a file for appending
        #encoding specifies the text format to use
        #with as automates the opening and closing process for a file
        #w3school did this so i did too
        with open('undownloaded.txt', 'a', encoding='utf-8') as f:
           for link in undownloaded_links:
               f.write(link + '\n')
    # if there's an exception, it will prevent a traceback or whatever it's called occuring.
    # Exception as e assigns whatever exception occured to a variable in string format
    except Exception as e:
       log('Error saving undownloaded links: ' + str(e)) #adding strings instead of a comma ensures
                                                        #that only 1 argument is passed.


def load_undownloaded_links():
    #same as above
    try:
        with open('undownloaded.txt', 'r', encoding='utf-8') as f:
            data = f.read()
            #inserts data at position 0 in the wiget
            link_entry.insert(0, data)
    except Exception as e:
        log('Error loading undownloaded links: ' + str(e))

#disable specified buttons for spam prevention
def disable_buttons(buttons):
   for i in buttons:
       i.config(state=tk.DISABLED)

#enable specified buttons once function finished.
def enable_buttons(buttons):
   for i in buttons:
       i.config(state=tk.NORMAL)






def download():
    #.split splits a string into elements contained in a list along an element, usually a space.
    # in this case, the user enters 1 link per line(\n)
    raw_links = link_entry.get('1.0', 'end').split('\n')
    #lists store data in a bundle, accessible by indexes starting from 0 representing the left or first elemeent
    #example = [1, 2, 3]
    #example[0] = 1
    links = []
    for i in raw_links:
        if i.strip():  #.strip deletes all the whitespace chars < > from a string alongside others if specified, <\t>, <\n>
                       #strings with stuff in them are truthy
                       #strings with nothing in them are falsy
                       #this removes any empty lines
            links.append(i)
            #append adds a element to the end of a list as a new element

    #get information about the download specifications.
    folder = selected_folder_var.get()
    mode = mode_var.get()

    if not links:#detect true or false lists
        log('Error: No links found.')
        Mb.showerror('Error', 'Error: No links found')
        return


    def worker():
        log('--- Starting ' + mode + ' Download ---')
        disable_buttons([video_opt_button, audio_opt_button, video_config_button, audio_config_button])

        #opts is a preexisting dictionary in yt-dlp. we're only changing certain values here.
        #source: ramus's presentation on data structures
        #didn't expect to see it here tbh
        opts = {
            'outtmpl': '%(title)s.%(ext)s',
            'restrictfilenames': True,
        }

        # mode specific options
        # editing values in the big dictionary based on the mode selected
        # referincing global stringvars modified  by the config menus
        #
        if mode == 'Audio':
            opts['format'] = 'bestaudio/best'
            opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': audio_format_var.get(),
                'preferredquality': '192',
            }]
        else:
            v_qual = video_quality_var.get()
            if v_qual == 'best':
                #settings for the downloader
                opts['format'] = 'bestvideo+bestaudio/best'
            else:
                opts['format'] = 'bestvideo[height<='+v_qual+']+bestaudio/best'

            opts['merge_output_format'] = video_format_var.get()





        failed = []
        for link in links:
            log('Downloading: ' + link)
            try:
                with yt_dlp.YoutubeDL(opts) as ydl:
                    ydl.download([link])
                log('Success.')
            except Exception as e:
                log('Error: ' + e)
                failed.append(link)

        if failed:
            log('Done. ' + len(failed) + ' failed.')
            try:
                with open('undownloaded.txt', 'a') as f:
                    for l in failed: f.write(l + '\n')
            except:
                pass
        else:
            log('All finished.')
    t = threading.Thread(target=worker)
    t.join()

