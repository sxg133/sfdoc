import sys
from Tkinter import *
import tkFileDialog
from sfdoc_core import sfdoc_main
import tkMessageBox

class SFDocApp:

	def __init__(self, master):
		self.frame = Frame(master)
		self.frame.pack()

		self.set_defaults()

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

		self.make_dir_entry(
			"Source Directory:", 
			self.source_directory, 
			self.get_source_directory,
			0, 0,
			group_source_target
			)

		self.make_dir_entry(
			"Target Directory:", 
			self.target_directory, 
			self.get_target_directory,
			1, 0,
			group_source_target
			)


		# Code Options group
		group_code_options = LabelFrame(
			self.frame,
			text="Code Options"
			)
		group_code_options.grid(
			row=3,
			column=0,
			rowspan=3,
			columnspan=2,
			sticky='NW',
			padx=5,
			pady=5,
			ipadx=5,
			ipady=5
			)

		self.make_text_entry(
			"Class Pattern:",
			self.class_pattern,
			3, 0,
			group_code_options
			)

		self.make_text_entry(
			"Test Pattern:",
			self.test_pattern,
			4, 0,
			group_code_options
			)

		Checkbutton(
			group_code_options,
			text="regex",
			variable = self.regex
			).grid(row=5, column=1, sticky="NW")

		# output options
		group_output = LabelFrame(
			self.frame,
			text="Output Options"
			)
		group_output.grid(
			row=7,
			column=0,
			rowspan=4,
			columnspan=2,
			sticky='NW',
			padx=5,
			pady=5,
			ipadx=5,
			ipady=5
			)

		self.make_text_entry(
			"Project Name:",
			self.project_name,
			7, 0,
			group_output
			)


		# Scope group
		group_scope = LabelFrame(
			group_output,
			text="Scope"
			)
		group_scope.grid(
			row=8,
			column=0,
			rowspan=3,
			columnspan=1,
			sticky='NW',
			padx=5,
			pady=5,
			ipadx=5,
			ipady=5
			)

		Checkbutton(
			group_scope,
			text="public",
			variable = self.scope['public']
			).grid(row=8, column=0, sticky="NW")

		Checkbutton(
			group_scope,
			text="protected",
			variable = self.scope['protected']
			).grid(row=9, column=0, sticky="NW")

		Checkbutton(
			group_scope,
			text="private",
			variable = self.scope['private']
			).grid(row=10, column=0, sticky="NW")


		# Exclusion group
		exclusion_group = LabelFrame(
			group_output,
			text="Exclusions"
			)
		exclusion_group.grid(
			row=8,
			column=1,
			rowspan=3,
			columnspan=1,
			sticky='NW',
			padx=5,
			pady=5,
			ipadx=5,
			ipady=5
			)

		Checkbutton(
			exclusion_group,
			text="Exclude properties",
			variable = self.exclude_properties
			).grid(row=8, column=1, sticky="NW")

		Checkbutton(
			exclusion_group,
			text="Exclude method sidebar",
			variable = self.exclude_method_sidebar
			).grid(row=9, column=1, sticky="NW")

		Checkbutton(
			exclusion_group,
			text="Exclude index file",
			variable = self.exclude_index_file
			).grid(row=10, column=1, sticky="NW")

		# generate button
		self.button_exit = Button(
			self.frame,
			text="Generate Doc",
			command=self.create_doc
			)
		self.button_exit.grid(row=11, column=0)

		# exit button
		self.button_exit = Button(
			self.frame,
			text="Exit",
			command=self.frame.quit
			)
		self.button_exit.grid(row=11, column=1)

	def make_dir_entry(self, label_text, textvar, pick_directory_callback, grid_row, grid_start_column, master):
		label_directory = Label(
			master,
			text=label_text
			).grid(row=grid_row, column=grid_start_column, padx=10)

		entry_directory = Entry(
			master,
			textvariable=textvar
			).grid(row=grid_row, column=grid_start_column+1, padx=10)

		button_directory = Button(
			master,
			text="...",
			command=pick_directory_callback
			).grid(row=grid_row, column=grid_start_column+2, padx=10)

	def make_text_entry(self, label_text, textvar, grid_row, grid_start_column, master):
		label = Label(
			master,
			text=label_text,
			).grid(row=grid_row, column=grid_start_column)
		entry = Entry(
			master,
			textvariable=textvar
			).grid(row=grid_row, column=grid_start_column+1)

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

	def set_defaults(self):
		self.source_directory = StringVar()
		self.target_directory = StringVar()
		self.class_pattern = StringVar()
		self.test_pattern = StringVar()
		self.regex = IntVar()
		self.project_name = StringVar()
		self.scope = {
			'public' : IntVar(),
			'protected' : IntVar(),
			'private' : IntVar()
		}
		self.exclude_properties = IntVar()
		self.exclude_method_sidebar = IntVar()
		self.exclude_index_file = IntVar()

		self.class_pattern.set('*.cls')
		self.test_pattern.set('*Test.cls')
		self.project_name.set('Apex Class Documentation')
		self.scope['public'].set(1)

	def create_args(self):
		scope = 'public'
		if self.scope['protected']:
			scope = 'protected'
		if self.scope['private']:
			scope = 'private'

		args = [
			'-p', self.class_pattern.get(),
			'-tp', self.test_pattern.get(),
			'-n', self.project_name.get(),
			self.source_directory.get(),
			self.target_directory.get()
		]

		if self.regex.get():
			args.append('--regex')
		if self.exclude_properties.get():
			args.append('--noproperties')
		if self.exclude_method_sidebar.get():
			args.append('--nomethodlist')
		if self.exclude_index_file.get():
			args.append('--noindex')

		return args

	def create_doc(self):
		args = self.create_args()
		title = ''
		dialog = ''
		try:
			sfdoc_main.main(args)
			tkMessageBox.showinfo(
				'Success!',
				'Doc generated successfully'
				)
		except Exception as inst:
			tkMessageBox.showerror(
				'Error!',
				'The follwoing error occured: ' + str(inst)
				)
			print(inst.args)


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