#import stuff
import tkinter as tk
from tkinter import messagebox as Mb
import yt_dlp
import threading

#we assign the log function in main. we treat log_func as a function for now.

def save_undownloaded_links(undownloaded_links, log_func):
	if not undownloaded_links:
		return
	try:
		with open('undownloaded.txt', 'a', encoding='utf-8') as f:
			for link in undownloaded_links:
				f.write(link + '\n')
	except Exception as e:
		log_func('Error saving undownloaded links: ' + str(e))


def load_undownloaded_links(link_entry, log_func):
	try:
		with open('undownloaded.txt', 'r', encoding='utf-8') as f:
			data = f.read()
			link_entry.delete('1.0', 'end')
			link_entry.insert('1.0', data)
	except Exception as e:
		log_func('Error loading undownloaded links: ' + str(e))


def clear_undownloaded_links(log_func):
	try:
		with open('undownloaded.txt', 'w', encoding='utf-8') as f:
			pass
	except Exception as e:
		log_func('Error clearing undownloaded links ' + str(e))



def download(link_entry, selected_folder_var, mode_var, video_format_var,
			 video_quality_var, audio_format_var, log_func, disable_buttons_func, enable_buttons_func):
	raw_links = link_entry.get('1.0', 'end').split('\n')
	links = []
	for i in raw_links:
		if i.strip():
			links.append(i.strip())

	folder = selected_folder_var.get()
	mode = mode_var.get()

	if not links:
		log_func('Error: No links found.')
		Mb.showerror('Error', 'Error: No links found')
		return

	def worker():
		log_func('--- Starting ' + mode + ' Download ---')
		disable_buttons_func()

		opts = {
			'outtmpl': folder + '/%(title)s.%(ext)s',
			'restrictfilenames': True,
			'nocheckcertificate': True
		}

		# Mode specific options
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
				opts['format'] = 'bestvideo+bestaudio/best'
			else:
				opts['format'] = 'bestvideo[height<=' + v_qual + ']+bestaudio/best'

			opts['merge_output_format'] = video_format_var.get()

		failed = []
		for link in links:
			log_func('Downloading: ' + link)
			try:
				with yt_dlp.YoutubeDL(opts) as ydl:
					ydl.download([link])
				log_func('Success.')
			except Exception as e:
				log_func('Error: ' + str(e))
				failed.append(link)

		if failed:
			log_func('Done. ' + str(len(failed)) + ' failed.')
			save_undownloaded_links(failed, log_func)
		else:
			log_func('All finished.')
			clear_undownloaded_links(log_func)


		enable_buttons_func()

	# Start the thread properly
	t = threading.Thread(target=worker)
	t.daemon = True  # Makes thread stop when main program exits
	t.start()