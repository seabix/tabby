#!/usr/local/bin/python3.10
# a really quick (like 13 min) script for PIM (grin) - like sticky notes.
# pyinstaller tabby1.py --name tabby --onefile -w
# https://pyinstaller.org/en/stable/usage.html

# USE THIS- it works! [but must fix tag names read]
#https://py2app.readthedocs.io/en/latest/tutorial.html#create-a-setup-py-file

from datetime import datetime
from os.path import exists
from os.path import realpath
import sys
import tkinter as tk	
from tkinter import ttk
from tkinter import Text
from tkinter import Button
from tkinter import messagebox
from tkinter.simpledialog import askstring
from tkinter.ttk import Style

boxnames = ["text_boxTab1", "text_boxTab2", "text_boxTab3", "text_boxTab4","text_boxTab5","text_boxTab6"]
boxchanged = [False, False, False, False, False, False]
box_size = [0, 0, 0, 0, 0, 0]

# ------------------------------------------------------
def testo(thefiletofind):
	filetouse = ""
	the_text = ""
	# trying to fix the file
	try:
		# PyInstaller creates a temp folder and stores path in _MEIPASS
		basePath = sys._MEIPASS
	except Exception:
		basePath = os.path.abspath(".")
	
	bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
	filetouse = os.path.join(bundle_dir, thefiletofind)
	return filetouse


# =================================================

root = tk.Tk()
root.title("Tabby Widget")
tabControl = ttk.Notebook(root)

# Create an instance of ttk style
style = ttk.Style()
style.theme_use('default')
style.configure('TNotebook.Tab', bg="rgba(234,162,33,0.5)")
style.map("tabControl", bg= [("selected", "rgba(234,162,33,0.5)")])

""" DEBUG STUFF """
import os
file_path = os.path.realpath(__file__)
folder_to_use = file_path[0:-13]

tabLabels = []
tabNameFileToUse = testo("tabNames.txt")
#tabLabels = ["Music","Code Projects","To-Do","Passwords","Web Links", "Other"]
try:
	with open(tabNameFileToUse) as f:
		#messagebox.showinfo("File: ", tabNameFileToUse)
		data = f.read()
		temp = data.split("\n")
		for i in range(0, len(temp)):
			tabLabels.append(temp[i])
except FileNotFoundException:
		tabLabels = ["Tab 1", "Tab 2", "Tab 3", "Tab 4", "Tab 5", "Other"]
		
def clear_textbox():
	text_box.delete(1.0, "end")
	
def quit_script():
	now = datetime.now()
	dt = now.strftime("%b %d %Y, %H:%m.%S")
	for i in range(0, len(boxnames)):
		if i == 0:
			data_to_save = text_boxTab1
		elif i == 1:
			data_to_save = text_boxTab2
		elif i == 2:
			data_to_save = text_boxTab3
		elif i == 3:
			data_to_save = text_boxTab4
		elif i == 4:
			data_to_save = text_boxTab5
		else:
			data_to_save = text_boxTab6;
		file_name = testo(boxnames[i] + ".txt")	
		the_text = data_to_save.get('1.0', 'end-1c')
		#if len(the_text) > 3 or len(box_size[i]) != the_text:    # ADDED THIS SIZE DIFF.
		if box_size[i] != len(the_text) and len(the_text) > 3:    # ADDED THIS SIZE DIFF.
			the_text = data_to_save.get('1.0', 'end')+"\t("+dt+")\n"
		else:
			the_text = ""
		try:
			with open(file_name, "w") as f:
				f.write(the_text)
				f.truncate()
		except:
			messagebox.showerror("File problem", "Sorry cannot save your notes.😧")
	root.destroy()

	
def get_content(number):
	message = ""
	# get the real path - 
	#file_to_read = testo(boxnames[number] + ".txt")
	file_to_read = testo(boxnames[number] + ".txt")
	try:
		with open(file_to_read) as f:
			message = f.read()
	except FileNotFoundError:
		message = ""
	box_size[number] = len(message)
	return message
	
	
def get_data():
	the_text = text_boxTab2.get('1.0', 'end-1c')
	prompt = askstring("Save", "Save to what file name?")
	prompt = testo(prompt)
	print("\nPROMPT: ",prompt)
	try:
		f = open(prompt, "a")
		try:
			f.write(the_text)
			f.truncate()
		except:
			messagebox.showerror("File problem", "Sorry cannot save your notes. 😧")
		finally:
			f.close()
	except:
		messagebox.showerror("File problem", "Cancelled or other file issue. 😧")
	else:
		print(f"File {prompt} saved.")


tab1 = ttk.Frame(tabControl)
tabTab1 = ttk.Frame(tabControl)
tabTab2 = ttk.Frame(tabControl)
tabTab3 = ttk.Frame(tabControl)
tabTab4 = ttk.Frame(tabControl)
tabTab5 = ttk.Frame(tabControl)
tabTab6 = ttk.Frame(tabControl)

tabControl.add(tab1, text ='Welcome')
tabControl.add(tabTab1,text = tabLabels[0])
tabControl.add(tabTab2,text = tabLabels[1])
tabControl.add(tabTab3,text = tabLabels[2])
tabControl.add(tabTab4,text = tabLabels[3])
tabControl.add(tabTab5,text = tabLabels[4])
tabControl.add(tabTab6,text = tabLabels[5])

tabControl.pack(expand = 1, fill ="both")

ttk.Label(tab1, text ="Welcome to the Tabbed Sticky Notes Widget.\
	\nGB Sept 19, 2022 - version 1.").grid(column = 0,
	row = 0,
	padx = 30,
	pady = 30)

# Text Areas (poorly done but hey ... )
# --- start a text box and what it needs ----
message = get_content(0)
text_boxTab1 = Text(tabTab1, 
	height = 13,
	width = 60,
	wrap='word',
	font=('Avenir Next', 14)
)
text_boxTab1.pack(expand = True)
text_boxTab1.insert('end', message)
# end the text box

# Tab2 Text Area
message = get_content(1)
text_boxTab2 = Text(tabTab2, 
	height = 13,
	width = 60,
	wrap='word',
	font=('Avenir Next', 14)
)
text_boxTab2.pack(expand = True)
text_boxTab2.insert('end', message)
# end the text box

# To Do Text Area
message = get_content(2)
text_boxTab3 = Text(tabTab3, 
	height = 13,
	width = 70,
	wrap='word',
	font=('PT Mono', 14)
)
text_boxTab3.pack(expand = True)
text_boxTab3.insert('end', message)
# end the text box

# tabTab4 Text Area
message = get_content(3)
text_boxTab4 = Text(tabTab4, 
	height = 13,
	width = 60,
	wrap='word',
	font=('Avenir Next', 14)
)
text_boxTab4.pack(expand = True)
text_boxTab4.insert('end', message)
# end the text box

# tabTab5 Text Area
message = get_content(4)
text_boxTab5 = Text(tabTab5, 
	height = 13,
	width = 60,
	wrap='word',
	font=('Avenir Next', 14)
)
text_boxTab5.pack(expand = True)
text_boxTab5.insert('end', message)
# end the text box

# Tab6 Text Area
message = get_content(5)
text_boxTab6 = Text(tabTab6, 
	height = 13,
	width = 60,
	wrap='word',
	font=('Avenir Next', 14)
)
text_boxTab6.pack(expand = True)
text_boxTab6.insert('end', message)
# end the text box

# BUTTONS
Button(
	tab1,
	text = "Save all tab contents and quit script.",
	width = 38, height = 1,
	command = quit_script
).grid(column = 0, row = 1, padx=0, pady=30)
Button(
	tabTab2,
	text = "Export to other than default file",
	width= 28,
	height= 1,
	command = get_data
).pack(expand=True)

if __name__ == "__main__":
	root.mainloop()