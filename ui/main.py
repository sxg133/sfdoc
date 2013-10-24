import sys
from Tkinter import *
import tkFileDialog

class SFDocApp:

	def __init__(self, master):
		self.frame = Frame(master)
		self.frame.pack()

		# open directory options
		self.dir_opt = {
			'initialdir' : 'C:\\',
			'mustexist' : True,
			'parent' : master,
			'title' : ''
		}

		# Source / Target group
		group_source_target = LabelFrame(
			self.frame,
			text="Source / Target"
			)
		group_source_target.grid(
			row=0,
			column=0,
			rowspan=2,
			columnspan=3,
			sticky='NW',
			padx=5,
			pady=5,
			ipadx=5,
			ipady=5
			)

		# source directory
		self.source_directory = StringVar()
		self.make_dir_entry(
			'Source Directory:', 
			self.source_directory, 
			self.get_source_directory,
			0, 0,
			group_source_target
			)

		# target directory
		self.target_directory = StringVar()
		self.make_dir_entry(
			'Target Directory:', 
			self.target_directory, 
			self.get_target_directory,
			1, 0,
			group_source_target
			)

		# exit button
		# self.button_exit = Button(
		# 	frame,
		# 	text="Exit",
		# 	fg="red",
		# 	command=frame.quit
		# 	)
		# self.button_exit.grid(row=5, column=2)

	def make_dir_entry(self, label_text, textvar, pick_directory_callback, grid_row, grid_start_column, master):
		label_directory = Label(
			master,
			text=label_text
			).grid(row=grid_row, column=grid_start_column)
		self.target_directory = StringVar()
		entry_target_directory = Entry(
			master,
			textvariable = self.target_directory
			).grid(row=grid_row, column=grid_start_column+1)
		button_target_directory = Button(
			master,
			text="...",
			command=pick_directory_callback
			).grid(row=grid_row, column=grid_start_column+2)

	def get_source_directory(self):
		self.set_directory_entry(self.source_directory, 'Select apex class directory...')

	def get_target_directory(self):
		self.set_directory_entry(self.target_directory, 'Select the output directory...')

	def set_directory_entry(self, textvar, title='pick a directory'):
		self.dir_opt['title'] = title
		if textvar:
			self.dir_opt['initialdir'] = textvar.get()
		directory = self.pick_directory()
		if directory is not None and directory:
			textvar.set(directory)

	def pick_directory(self):
		return tkFileDialog.askdirectory(**self.dir_opt)

def main(argv=sys.argv):
	root = Tk()
	app = SFDocApp(root)
	root.mainloop()
	try:
		root.destroy()
	except:
		pass

if __name__ == "__main__":
	sys.exit( main() )