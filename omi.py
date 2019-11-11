"""
SHIT LEFT TO DO
---------------
> stack statusbar below textarea

>> fix tabbing (custom sizes and proper indentation)

>>> syntax highlighting
"""
import tkinter as tk
from tkinter import filedialog, messagebox
from datetime import datetime

#general preferences
tabwidth = 4
tabstyle = "tab" #tab | space
fontspecs = ("Consolas", 10) #universal font

settingstext = "\n\tControls:\n\t---------\n\tCTRL+N - New/Clear\n\tCTRL+S - Save\n\tCTRL+SHIFT+S - Save as..\n\tCTRL+O - Open file\n\tCTRL+W - Close window\n\tCTRL+` - Toggle status bar\n\tCTRL+Z - Undo\n\n\t--COMING SOON\n\tCTRL+F - Find text"

class Statusbar:
	def __init__(self, parent):
		self.status = tk.StringVar()
		self.textarea = parent.textarea
		
		self.label = tk.Label(self.textarea, textvariable=self.status, bg="white", fg="black", anchor="sw", font=fontspecs)
		self.statuson = True
	
	def setstatus(self, *args):
		self.statuson = False if self.statuson else True
	
	def updatestatus(self, *args):
		self.label.pack(side=tk.BOTTOM, fill=tk.X) if self.statuson else self.label.pack_forget()
		
		#calculated shit
		char = str(len(self.textarea.get(1.0, tk.END)))
		word = str(len(self.textarea.get(1.0, tk.END).split(" ")))
		poscol,posrow = self.textarea.index(tk.INSERT).split(".")
		
		#to display
		charcount = " | char: " + char
		wordcount = " | word: " + word
		cursorcol = "- row: " + poscol
		cursorrow = " | col: " + posrow
		
		self.status.set(( "saved | " if isinstance(args[0], bool) else "") + cursorcol + cursorrow  + charcount + wordcount)
		
class Menubar:
	def __init__(self, parent):
		menubar = tk.Menu(parent.master, font=fontspecs)
		parent.master.config(menu=menubar)
		
		dropdown = tk.Menu(menubar, font=fontspecs, tearoff=0)
		dropdown.add_command(label="New File", command=parent.newfile, accelerator="Ctrl+N")
		dropdown.add_command(label="Open File", command=parent.openfile, accelerator="Ctrl+O")
		dropdown.add_command(label="Save", command=parent.save, accelerator="Ctrl+S")
		dropdown.add_command(label="Save As..", command=parent.saveas, accelerator="Ctrl+Shift+S")
		dropdown.add_command(label="Close", command=parent.master.destroy, accelerator="Ctrl+W")
		
		#toggle menubar display
		#menubar.add_cascade(label="xxx", menu=dropdown)
		
class omi:
	def __init__(self, master):
		self.filename = None;
		master.title(self.filename)
		master.geometry("400x400")
		master.minsize(100,100)
		self.master = master
		
		#textarea
		self.textarea = tk.Text(master, font=fontspecs, wrap=tk.WORD, undo=True, maxundo=20, autoseparators=True)
		self.textarea.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
		
		#placeholder for instructions
		self.textarea.insert("1.0", settingstext)
		
		#set up window - menubar / statusbar / keybindings
		self.menubar = Menubar(self)
		self.statusbar = Statusbar(self)
		self.keybinds()
		
		self.textarea.focus_force()

	#functions
	def worddelete(self, *args):
		try:		
			curpos = self.textarea.index(tk.INSERT)
			curcharcol = int(curpos.split(".")[1])
			curcharrow = int(curpos.split(".")[0])
			delchar = ".".join([str(curcharrow), str(curcharcol-1)])
	
			while self.textarea.get(delchar) != " " and curcharcol != 0:
				self.textarea.delete(delchar)
				curcharcol -= 1
				delchar = ".".join([str(curcharrow), str(curcharcol)])
		except Exception as e:
			print(e)
			
	def synhi(self, word):
		return 0
	
	def indent(self,  *args, width=tabwidth):
		self.textarea.insert(tk.INSERT, " "*width)
		return "break"
		
	def setwindowtitle(self, name=None):
		if name:
			self.master.title(name)
		else:
			self.master.title("")
	
	def newfile(self, *args):
		self.textarea.delete(1.0, tk.END)
		self.setwindowtitle(None)
		
	def openfile(self, *args):
		self.filename = filedialog.askopenfilename(
			defaultextension=".txt"
			,filetypes=[
				("All Files", "*.*")
				,("Text", "*.txt")
				,("Markup", "*.*ml")
				,("CSS", "*.css")
				,("Python", "*.py")
				,("JavaScript", "*.js")
			]
		)
		
		if self.filename:
			self.textarea.delete(1.0, tk.END)
			with open(self.filename, "r") as f:
				self.textarea.insert(1.0, f.read())
			self.setwindowtitle(self.filename)
	
	def save(self, *args):
		savecontent = self.textarea.get(1.0, tk.END)
		if self.filename:
			try:
				savecontent = self.textarea.get(1.0, tk.END)
				with open(self.filename, "w") as f:
					f.write(savecontent)
				self.statusbar.updatestatus(True)
				return True
			except Exception as e:
				print(e)
				return False
		else:
			return self.saveas()
		
	def saveas(self, *args):
		try:
			newfile = filedialog.asksaveasfilename(
				initialfile="new"+datetime.now().strftime("%M_%S_%d_%m")
				,defaultextension=""
				,filetypes=[
					("All Files", "*.*")
				]
			)
			savecontent = self.textarea.get(1.0, tk.END)
			with open(newfile, "w") as f:
				f.write(savecontent)
			self.filename = newfile
			self.setwindowtitle(self.filename)
			self.statusbar.updatestatus(True)
			return True
		except Exception:
			donotsave = tk.messagebox.askyesno("DID NOT SAVE", "Would you like to close\nthe file without saving?", default=tk.messagebox.YES)
			return True if donotsave else self.saveas()
		
	def kill(self, *args):
		if self.textarea.get(1.0, tk.END).strip() == settingstext.strip() or self.save():
			self.master.destroy()
	
	#shortcuts
	def keybinds(self):
		self.textarea.bind('<Control-n>', self.newfile)
		self.textarea.bind('<Control-o>', self.openfile)
		self.textarea.bind('<Control-s>', self.save)
		self.textarea.bind('<Control-S>', self.saveas)
		self.textarea.bind('<Control-`>', self.statusbar.setstatus)
		self.textarea.bind('<Control-w>', self.kill)
		if tabstyle=="space":
			self.textarea.bind('<Tab>', self.indent)
		self.textarea.bind('<Control-BackSpace>', self.worddelete)
		self.textarea.bind('<KeyRelease>', self.statusbar.updatestatus)
		
if __name__ == "__main__":
	master = tk.Tk()
	master.iconbitmap(default="logo.ico")
	window = omi(master)
	master.mainloop()
	
