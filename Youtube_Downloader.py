from tkinter.filedialog import askdirectory
from pytube import YouTube, Playlist, exceptions
import pytube, webbrowser
import time, os, threading, socket, urllib.request, datetime 
from tkinter import ttk 
import tkinter as tk
from PIL import ImageTk, Image
from win10toast import ToastNotifier
from socket import create_connection
from os import path



def is_connected():
	try:
		create_connection(('www.google.com', 80))
		return True
	except:
		return False


def notifier(msg):
	toaster = ToastNotifier()
	toaster.show_toast("YouTube Downloader", msg, icon_path="icon.ico",
	duration=5, threaded=True)

dirname = "C:" + os.path.join(os.environ["HOMEPATH"], "Downloads").replace("\\", "/")
file_size = 0
video = ''
# PROGRESSBAR CALCULATION
def progress_Check(chunk = None, file_handle = None, remaining = None):
    global file_size, progress
    percent = (100*(file_size-remaining))/file_size
    progress['value'] = percent
    style.configure('text.Horizontal.TProgressbar', 
                    text = str(int(percent)) + " %")
    root.update()

# SECOND TO TIME
def convert(n): 
    return str(datetime.timedelta(seconds = n)) 

# VIDEO DOWNLOAD FUNCTION
def download():
	global dirname, video, progress, file_size, all_response
	if not is_connected():
		video_title.set("Please check Internet!")
		quit()
	if not path.exists(dirname):
		video_title.set(f"{dirname} not found!")
		quit()
	video_title.set("Please wait. . .")
	download_btn.place_forget()
	disabled_btn.place(x = 510, y = 56)
	video_url = url.get()
	if all_response:
		progress['value'] = 0
		style.configure('text.Horizontal.TProgressbar', 
                    text = "0 %")
		count = 1
		for video in all_response:
			try:
				stream = video.streams.filter(progressive=True, file_extension = 'mp4').order_by('resolution').desc().first()
				video_title.set(f"{stream.default_filename}")
				filename = f"{count}. {stream.default_filename}" if video_type.get() == 2 else stream.default_filename
				video.register_on_progress_callback(progress_Check)
				file_size = stream.filesize
				mb = round(file_size/1024/1024, 2)
				sizeinmb.set(f"{mb} MB")
				video_time.set(convert(int(video.length)))
				stream.download(dirname, filename)
				count += 1
			except pytube.exceptions.VideoUnavailable:
				video_title.set("Video does not exists!")
				continue
		all_response = []
		progress['value'] = 0
		sizeinmb.set("0.00 MB")
		video_time.set("00:00:00")
		style.configure('text.Horizontal.TProgressbar', 
	    text = "0 %")
		notifier("Video downloaded successfully.")
		video_title.set("Video downloaded successfully.")


	else:
		video_title.set("Video does not exists!")


def choose_path(event):
	global dirname
	select = askdirectory()
	if select:
		dirname = select
	file_path.set(dirname)

def focus_in(event):
	if "http" not in url.get():
		textbox.delete(0, tk.END)

def disabled(msg = ''):
	root.title("YouTube Downloader")
	sizeinmb.set("0.00 MB")
	video_time.set("00:00:00")
	video_title.set(msg)
	progress['value'] = 0
	style.configure('text.Horizontal.TProgressbar', 
	    text = "0 %")

def focus_out(event):
	video_url = url.get()
	if not video_url:
		textbox.insert(tk.END, "Please enter a YouTube URL")
		disabled()

temp = ''
all_response = []
def checking():
	if not is_connected():
		video_title.set("Please check Internet!")
		quit()
	global quality, video, selected, temp, disabled_btn, download_btn
	global is_url
	global all_response
	all_response = []
	video_url = url.get()
	single_or_playlist = video_type.get()
	if video_url:
		if (video_url) and (video_url != "Please enter a YouTube URL") and ("http" in video_url):
			disabled(msg = "Please wait, getting video information")
			try:
				if single_or_playlist == 1:
					video = YouTube(video_url, on_progress_callback = progress_Check)
				else:
					video = Playlist(video_url)
			except pytube.exceptions.RegexMatchError:
				video_title.set("Please enter valid URL!")
				quit()
			except urllib.error.URLError:
				video_title.set("error : Please check Internet!")
				quit()
			except:
				video_title.set("error : URL does not exists!")
				quit()
		else:
			disabled("")
			quit()

		all_response = []
		if single_or_playlist == 1:
			all_response.append(video)
		else:
			try:
				for vid in video.videos:
					all_response.append(vid)
			except KeyError:
				video_title.set(f"Something went wrong, with this{ ' Video ' if single_or_playlist == 1  else' Playlist'} try again!")
				download_btn.place_forget()
				disabled_btn.place(x = 510, y = 56)
				quit()
		disabled_btn.place_forget()
		download_btn.place(x = 510, y = 56)
		video_title.set("Success : You can download now")
	else:
		disabled("Please enter video URL!")			

def start_download():
	threading.Thread(target=download).start()

def choose_select(index, value, op):
	sizeinmb.set(quality.get().split("/")[1].split("[")[1].split("]")[0])

def start_checking(event):
	threading.Thread(target=checking).start()


def radion_btn_change():
	get_video_type = video_type.get()
	video_url = url.get()
	if (video_url) and (video_url != "Please enter a YouTube URL") and ("http" in video_url):
		threading.Thread(target=checking).start()

def open_developer_fb():
	webbrowser.open('https://www.facebook.com/sadirul4')


def closing_coffee_window():
	global top, is_coffee_open
	top.destroy()
	is_coffee_open = False

root = tk.Tk()
root.title("YouTube Downloader")
root.geometry("600x300+400+140")
root.resizable(width = False, height = False)
root.wm_iconbitmap("icon.ico")


# STYLE
style = ttk.Style(root)
style.layout('text.Horizontal.TProgressbar', 
             [('Horizontal.Progressbar.trough',
               {'children': [('Horizontal.Progressbar.pbar',
                              {'side': 'left', 'sticky': 'ns'})],
                'sticky': 'nswe'}), 
              ('Horizontal.Progressbar.label', {'sticky': ''})])
style.configure('text.Horizontal.TProgressbar', text='0 %')


# C = tk.Canvas(root)
filename = tk.PhotoImage(file = "bg.png")
bg_label = tk.Label(root)
bg_label.configure(image = filename)
bg_label.place(x = 0, y = 0, relwidth = 1, relheight = 1)
tk.Label(root, text = "YouTube Downloader", font = ("Arial", 14), fg = "white", bg = "#6600ff", width = 54).place(x = 0, y = 1)

developer_link = tk.Label(root, cursor = "hand2", text = "Developed by : Sadirul Islam", font = ("Courier", 14), fg = "white", bg = "#6600ff", width = 54)
developer_link.place(x = 0, y = 276)
developer_link.bind("<Button-1>", lambda e : open_developer_fb())
# SHOW VIDEO LENGTHin video_time
video_time = tk.IntVar()
tk.Label(root, textvariable = video_time, font = ("Arial, 12"), fg = "black", bg = "#f2f2f2", width = 8).place(x = 510, y = 90)
video_time.set("00:00:00")
is_coffee_open = False
top = True
open_image = Image.open("qr_code.png")
# open_image.resize((20, 20))
qr_image = ImageTk.PhotoImage(open_image)
def open_popup():
	global is_coffee_open, top, qr_image
	if not is_coffee_open:
	   is_coffee_open = True
	   top = tk.Toplevel(root)
	   top.geometry("330x420+530+140")
	   top.title("YouTube Downloader - Buy me a Coffee")
	   top.resizable(width = False, height = False)
	   top.wm_iconbitmap("icon.ico")
	   tk.Label(top, text = "Scan this QR Code", font = ("Arial", 14), fg = "white", bg = "#6600ff", width = 30).place(x = 0, y = 1)
	   top_bg_label = tk.Label(top)
	   top_bg_label.configure(image = qr_image)
	   top_bg_label.place(x = 13, y = 35)
	   top.protocol("WM_DELETE_WINDOW", closing_coffee_window)


buy_me_coffee = tk.Label(root, text = "Buy me a Coffee", font = ("Arial, 8 underline"), cursor = "hand2", fg = "blue", width = 15)
buy_me_coffee.place(x = 500, y = 30)
buy_me_coffee.bind("<Button-1>", lambda e : open_popup())

sizeinmb = tk.IntVar()
tk.Label(root, textvariable = sizeinmb, font = ("Arial, 13"), fg = "black", bg = "#f2f2f2", width = 8).place(x = 7, y = 30)
sizeinmb.set("0.00 MB")

video_type  = tk.IntVar()
one_video_radio_btn = ttk.Radiobutton(root, text = 'One video', value = 1, variable = video_type, command = radion_btn_change, style = "TRadiobutton").place(x = 90, y = 30)
playlist_radio_btn = ttk.Radiobutton(root, text = 'Playlist', value = 2, variable  = video_type, command = radion_btn_change, style = "TRadiobutton").place(x = 180, y = 30)
video_type.set(1)

# URL ENTRY BOX
url = tk.StringVar()
textbox = ttk.Entry(root, textvariable = url)
textbox.place(x = 7, y = 56, height = 25, width = 490)
# textbox.bind("<Leave>", start_checking)
textbox.bind("<FocusIn>", focus_in)
url.trace("w", lambda name, index, mode, sv=url: start_checking(url))
textbox.bind("<FocusOut>", focus_out)
textbox.insert(tk.END, "Please enter a YouTube URL")

# SAVE FILE PATH
file_path = tk.StringVar()
save_path = ttk.Entry(root, textvariable = file_path, state = "readonly", cursor = "arrow")
save_path.place(x = 7, y = 90, height = 23, width = 489)
file_path.set(dirname)
save_path.bind("<Button-1>", choose_path)

disabled_btn = ttk.Button(root, text='Download', state = tk.DISABLED, command = start_download, cursor = "no", width = 12)
disabled_btn.place(x = 510, y = 56)


# DOWNLOAD START BUTTON
download_btn = ttk.Button(root, text='Download', command = start_download, width = 12, cursor = 'hand2')

# PROGRESSBAR
progress = ttk.Progressbar(root, length = 586, orient = tk.HORIZONTAL, mode = 'determinate', style='text.Horizontal.TProgressbar')
progress.place(x = 7, y = 123, height = 30)

# VIDEO TITLE
video_title = tk.StringVar()
title_label = tk.Label(root, textvariable =video_title, font = ("Courier", 12), fg = "white", bg = "#4d4d4d", width = 58, height = 3)
title_label.place(x = 7, y = 160)
video_title.set("")

root.mainloop()
