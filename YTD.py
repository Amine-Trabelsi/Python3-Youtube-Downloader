'''
Author: Amine Trabelsi

current status: 
	* Download works well: no errors yet
	* progress bar not stopping after one download


'''

from pytube import YouTube, request 
from tkinter import *
from tkinter import ttk
from os import path, environ
from multiprocessing import Process
from tkinter import filedialog as fd
import subprocess
from tkinter import messagebox
from threading import Thread
import sys


def getdirectory():
	""" Choose the directory """
	print("Initializing Dialogue... \n please select a directory.")
	dirname = fd.askdirectory(title='Please select a directory')
	print(dirname)
	dirnameEvar.set(dirname)

def remove_values_from_list(the_list, val):
	"""to remove none values form resolution list"""
	return [value for value in the_list if value != val]

def UpdateOM():
	""" Append the resolutions to the option menu"""
	for i in streamqvideos:
		OptionList.append(i)
	menu = QOptionMenu["menu"]
	menu.delete(0,"end")
	for string in OptionList:
		menu.add_command(label=string, command=lambda value=string: OptionMenuValue.set(value))

def close():
	""" To close the top level window"""
	topF.destroy()

def CreateTop():
	""" To create a top level window to let the user choose video resolution"""
	global topF
	global QOptionMenu
	global OptionList
	global OptionMenuValue
	topF = Toplevel()
	topF.title("Stream")
	# top icon
	topF.iconbitmap('favicon.ico')
	# top size
	topF.geometry("275x140")
	#topF.resizable(0, 0)
	labf = ttk.Frame(topF)
	labf.grid(row=0, column=0)
	# top label
	Labb = ttk.Label(labf, text='Choose Stream', font='verdana, 25')
	Labb.grid(row=0, column=0,pady=20)
	# top frame
	topff = ttk.Frame(labf)
	topff.grid(row=1,column=0,pady=(0,20),padx=20)
	# stream list
	style.configure('TMenubutton', font=('Helvatica', 14))
	OptionList = ["Streams"]
	OptionMenuValue = StringVar(topff)
	OptionMenuValue.set(OptionList[0]) # default value
	QOptionMenu = ttk.OptionMenu(topff, OptionMenuValue, *OptionList)
	QOptionMenu.grid(row=1, column=0,padx=(0,10))
	
	# OK button
	style.configure('my.TButton', font=('Helvatica', 12), width=6)
	topB = ttk.Button(topff, text="OK", style='my.TButton',command=lambda:close())
	topB.grid(row=1, column=1)


def DV(video):
	video.download(filename='video')
def DA(audio):
	audio.download(filename='audio')
def buttoncommand():
	""" Configure download and streams """
	try:
		try:
			print("Checking URL...")	
			link = YouTube(URLE.get())
		except Exception as e:
			print(e)
		global VideoName
		VideoName = link.title
		VideoName = VideoName.replace(" ","-").replace("/","-").replace("|","-")
		print("URL checked")
		global streamqvideos
		streamqvideos = [stream.resolution for stream in link.streams.filter(adaptive=True).filter(file_extension='mp4')]
		streamqvideos[:] = (value for value in streamqvideos if value != None)
		streamqvideos = [ii for n,ii in enumerate(streamqvideos) if ii not in streamqvideos[:n]]
		# streams available
		print(streamqvideos)
		#
		def PPF(x):
			x.start(10)
		PP = Process(target=PPF(P))
		PP.start()
		CreateTop()
		UpdateOM()
		master.wait_window(topF)
		global directory
		directory = dirnameE.get()
		print("Got Directory")
		ress = OptionMenuValue.get()
		print("Done **********************************")
		global video
		video = link.streams.filter(adaptive=True).filter(file_extension='mp4').filter(res=ress).first()
		print(video)
		# find video size
		file_size = video.filesize / (1e6)
		print("video size: {} MB".format(file_size))
		#
		Vid = Process(target=DV,args=[video,])
		Vid.start()
		audio = link.streams.filter(only_audio=True).first()
		print(audio)
		# find audio size
		file_size = audio.filesize / (1e6)
		print("video size: {} MB".format(file_size))
		#
		AUD = Process(target=DA,args=[audio,])
		AUD.start()
		Vid.join()
		AUD.join()
		N = "{}.mp4".format(VideoName)
		M = "\\ffmpeg\\bin\\ffmpeg.exe -i video -i audio -c copy {}".format(N)
		Del = "Erase audio video"
		subprocess.call(M, shell=True)
		subprocess.call(Del, shell=True)
		print("Merged and deleted")

		print(directory)
		CMDD = 'move "{}" "{}"'.format(N,directory)
		print(CMDD)
		subprocess.call(CMDD,shell=True)
		print("Done!!!")
		PP.join()
		messagebox.showinfo("Info","Download finished!!!!")
		
	except Exception as e:
		print(e)
		messagebox.showerror("Error", "Something Went Wrong\n"
			 "\nPlease check your internet and try again")
		Del = "Erase audio video"
		subprocess.call(Del, shell=True)

def Main():
	global master
	""" Main window """
	master = Tk()
	#App icon
	master.iconbitmap('favicon.ico')
	# window title
	master.title('Downloader')
	# window size
	master.geometry("550x250")
	master.resizable(0, 0)
	# style
	global style
	style = ttk.Style()
	style.theme_use('clam')

	# Main Frame
	global root
	root = ttk.Frame(master,)
	root.grid(row=1, column=1)

	# title
	Lab1 = ttk.Label(root, text="Download video from youtube", font='verdana, 20')
	Lab1.grid(row=1, column=1, pady=20)
	# URL Frame
	URLF = ttk.Frame(root)
	URLF.grid(row=2, column=1,padx=(20,40))


	# URL Label
	URLL = ttk.Label(URLF, text="URL:", font='verdana, 14')
	URLL.grid(row=0, column=0)
	# URL Entry
	global URLE
	URLE = ttk.Entry(URLF, width=40, font='Arial, 14')
	URLE.grid(row=0, column=1)


	# directory Frame 
	dirframe = ttk.Frame(root)
	dirframe.grid(row=3, column=1, pady=(5,0))
	# directory initialing
	global dirnameEvar
	dirnameEvar = StringVar()
	# Directory Label
	DIRL = ttk.Label(dirframe, text="DIR:", font='verdana, 14')
	DIRL.grid(row=0, column=0)
	# Directory info
	global dirnameE
	dirnameE = ttk.Entry(dirframe, state="readonly" , textvariable=dirnameEvar,font='Arial, 12')
	dirnameE.grid(row=0, column=1, padx=5)
	# Choose directory button
	dirbut = ttk.Button(dirframe, text='Browse', command=lambda:getdirectory())
	dirbut.grid(row=0, column=2)
	# Get the desktop address
	desktop_addr = path.join(path.join(environ['USERPROFILE']), 'Desktop')
	dirnameEvar.set(desktop_addr)
	
	global P
	style.configure("TProgressbar",background="red")
	P = ttk.Progressbar(root,length=200,orient="horizontal",mode="indeterminate",style="TProgressbar")
	P.grid(row=5, column=1,pady=(20,0))


	Dowbut = ttk.Button(root, text="Download", command=lambda:buttoncommand(), style='TButton')
	Dowbut.grid(row=6, column=1, ipadx=5, ipady=5, pady=(20,20))
	

	master.mainloop()


app = Process(target=Main)
if __name__ == '__main__':
	app.start()
	app.join()
