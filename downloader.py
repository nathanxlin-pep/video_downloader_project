#downloader.py
#this module handles downloading videos and audio from links using yt-dlp
#it reads links from the text entry, configures download options based on user settings, and downloads each link
#if a download fails, it saves the failed link to a file so the user can retry it later
#it uses threading to download in the background so the gui doesn't freeze
#it disables buttons during download and re-enables them when done

#import stuff
import tkinter as tk
from tkinter import messagebox as Mb
import yt_dlp
import threading

#this function takes 2 parameters, the undownloaded links as a list, and log_func as the log function
#it iterates over a list and writes it to a file.
def save_undownloaded_links(undownloaded_links, log_func):
	# we assign the log function in main. we treat log_func as a function for now.
	# the parameters will be continually referenced in the parent function until main.py, where actual values will be assigned.
	# for now, we treat the parameters as if they actually exist.
	#a empty value returns false.
	# https://www.w3schools.com/python/python_booleans.asp empty list detection
	if not undownloaded_links:
		return

	#try except first tries to execute code under <try>
	#if there's an error, the code under <except> is executed
	#you can also store the error with Exception as e as a string
	try:
		#the open function opens a file in a selected mode
		#the 'a' mode  opens the file for appending or adding on to.

		#with as assigns the result from opening the file to a variable, f.
		#it automaatically handles the opening and closing of a file.
		#https: // www.w3schools.com / python / python_file_open.asp
		with open('undownloaded.txt', 'a') as f:
			#iterate over the undownlaoded links parameter, add each element to the undownloaded file
			for link in undownloaded_links:
				#.write writes a string into a file object
				#we put a newline at the end so that the user can download immediately after loading the failed links.
				f.write(link + '\n')
	except Exception as e:
		#save the error as E.
		#the actual log function gets passed as a parameter.
		log_func('Error saving undownloaded links: ' + str(e))



#this function reads the undownloaded.txt, and puts the contents into
#the link entry, represented by the link entry parameter.
def load_undownloaded_links(link_entry, log_func):
	# we assign the log function in main. we treat log_func as a function for now.
	# the parameters will be continually referenced in the parent function until main.py, where actual values will be assigned.
	# for now, we treat the parameters as if they actually exist.
	#try except explained before
	try:
		#opening the file in read mode assigns the file object to f
		#https://www.w3schools.com/python/python_file_open.asp
		with open('undownloaded.txt', 'r') as f:
			#this time, we need to access the whole file.
			#f.read reads the entire file.
			data = f.read()
			#.delete deletes the contents of a text widget from 1 index to another
			#.end is the end of the text widget
			link_entry.delete('1.0', 'end')
			#.insert inserts data into a text widget at a position
			#position 1.0 is the start of the text in a text widget
			link_entry.insert('1.0', data)
	except Exception as e:
		# save the error as E.
		# the actual log function gets passed as a parameter later on.
		log_func('Error loading undownloaded links: ' + str(e))

#this function wipes the undownloaded text file
def clear_undownloaded_links(log_func):
	try:
		#passing when opening a file in write mode wipes the file.
		with open('undownloaded.txt', 'w') as f:
			pass
	except Exception as e:
		# save the error as E.
		# the actual log function gets passed as a parameter later on.
		log_func('Error clearing undownloaded links ' + str(e))


#this function reads the undownloaded.txt, and puts the contents into
#the link entry, represented by the link entry parameter.
def load_undownloaded_links(link_entry, log_func):
    # we assign the log function in main. we treat log_func as a function for now.
    # the parameters will be continually referenced in the parent function until main.py, where actual values will be assigned.
    # for now, we treat the parameters as if they actually exist.
    #try except explained before
    try:
       #opening the file in read mode assigns the file object to f
       #https://www.w3schools.com/python/python_file_open.asp
       with open('undownloaded.txt', 'r') as f:
          #this time, we need to access the whole file.
          #f.read reads the entire file.
          data = f.read()
          #.delete deletes the contents of a text widget from 1 index to another
          #.end is the end of the text widget
          link_entry.delete('1.0', 'end')
          #.insert inserts data into a text widget at a position
          #position 1.0 is the start of the text in a text widget
          link_entry.insert('1.0', data)
    except Exception as e:
       # save the error as E.
       # the actual log function gets passed as a parameter later on.
       log_func('Error loading undownloaded links: ' + str(e))

#this function wipes the undownloaded text file
def clear_undownloaded_links(log_func):
    try:
       #passing when opening a file in write mode wipes the file.
       with open('undownloaded.txt', 'w') as f:
          pass
    except Exception as e:
       # save the error as E.
       # the actual log function gets passed as a parameter later on.
       log_func('Error clearing undownloaded links ' + str(e))



#this function takes in the options, link entry widget, and the misc functions to download.
#it processes the links from the entry widget, creates a seperate thread, and downloads the links.
def download(link_entry, selected_folder_var, mode_var, video_format_var,
           video_quality_var, audio_format_var, log_func, disable_buttons_func, enable_buttons_func):
    #.get gets the contents of a text widget from a start index to an end index
    #.split splits a string into a list by a delimiter, in this case a newline
    raw_links = link_entry.get('1.0', 'end').split('\n')
    #create a empty list to store the processed links
	#lists store a number of values in a single referencable variable
	#the data inside can be accessed by indexes, from 0 representing the 1st element onwards.
    links = []
    #iterate over the raw links
    for i in raw_links:
       #.strip removes whitespace from the start and end of a string
       #if the string is not empty after stripping, add it to the links list
       if i.strip():
          links.append(i.strip())

    #.get returns the value of a tkinter stringvar
	#strinvars aren't readable by python. .get converts them into a readable format.
    folder = selected_folder_var.get()
    mode = mode_var.get()

    #if the links list is empty, log an error and return
    #empty values return false
    if not links:
       log_func('Error: No links found.')
       #messagebox.showerror shows a error popup with nothing else attached
       Mb.showerror('Error', 'Error: No links found')
       return

    #this function is the worker thread that downloads the links
    #we define it inside the download function so it can access the variables
    def worker():
       log_func('--- Starting ' + mode + ' Download ---')
       #disable the buttons so the user cant mess with the settings while downloading
	   #or spam anything
       disable_buttons_func()


       #opts is a dictionary that contains the options for yt_dlp
	   #it is a dictionary so the user doesn't have to enter 27183125 parameters.
	   #the user can just edit the values in the dictionary they want to change.

	   #dictionaries are data structures that store values in relation to a pointer
	   #for example, outtmpl is a pointer to the value asscociated to outtmpl.
	   #referenging the outtmpl index in the dictionary allows the user to manipulate the value ascocciated with outtmpl


       #outtmpl is the naming convention for the downloaded files
       #restrictfilenames restricts the filenames to ascii characters
       #nocheckcertificate disables ssl certificate verification. Without it, everything breaks.
       opts = {
          'outtmpl': folder + '/%(title)s.%(ext)s',
          'restrictfilenames': True,
          'nocheckcertificate': True
       }

       # Mode specific options
       #if the mode is audio, we need to extract the audio from the video
       if mode == 'Audio':
          #format specifies the format to download
		  #editing the format value in the big yt-dpl option dictionary
          opts['format'] = 'bestaudio/best'
          #postprocessors is a list of postprocessors to run after downloading
          #FFmpegExtractAudio extracts the audio from the video
          opts['postprocessors'] = [{
             'key': 'FFmpegExtractAudio',
             'preferredcodec': audio_format_var.get(),
             'preferredquality': '192',
          }]

       else:
          #if the mode is video, we need to specify the quality
          v_qual = video_quality_var.get()
          #if the quality is best, we download the best quality video and audio
		  #'bestvideo+bestaudio/best' is too long to fit onto the screen on a button
          if v_qual == 'best':
             opts['format'] = 'bestvideo+bestaudio/best'
          else:
             #otherwise, we download the video with the specified quality and the best audio
             #the format string specifies the video quality
             opts['format'] = 'bestvideo[height<=' + v_qual + ']+bestaudio/best'

          #merge_output_format specifies the format to merge the video and audio into
          opts['merge_output_format'] = video_format_var.get()

       #create a empty list to store the failed links
       failed = []
       #iterate over the links
       for link in links:
          log_func('Downloading: ' + link)
          #try except explained
		  #with as explained
          try:
             #YoutubeDL is the main class for yt_dlp
             #we pass in the options dictionary
             with yt_dlp.YoutubeDL(opts) as ydl:
                #.download downloads the links
                #we pass in a list with the link
                ydl.download([link])
             log_func('Success.')
          except Exception as e:
             #if there's an error, log it and add the link to the failed list
			 #logging is good for debugging and selecting options.
             log_func('Error: ' + str(e))
             failed.append(link)

       #if there are failed links, save them to the undownloaded file
       if failed:
          #str(len(failed)) converts the length of the failed links list to a string
          log_func('Done. ' + str(len(failed)) + ' failed.')
          save_undownloaded_links(failed, log_func)
       else:
          #if there are no failed links, clear the undownloaded file
          log_func('All finished.')
          clear_undownloaded_links(log_func)

       #enable the buttons after downloading
       enable_buttons_func()

    # Start the thread properly
	#threading assigns code to be run in another thread of the cpu
	#it allows for multitasking. we can run worker in the background, which allows the main program to continue running.
    #threading.Thread creates a new thread
    #target is the function to run in the thread
    t = threading.Thread(target=worker)
    #daemon threads stop when the main program exits
    t.daemon = True  # Makes thread stop when main program exits
    #.start starts the thread
    t.start()