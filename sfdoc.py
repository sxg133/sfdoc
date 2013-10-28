from sfdoc_core import sfdoc_main
import main_window
import sys

def main(argv=None):
	if argv is None:
		argv = sys.argv

	# if ui is specified, launch main window
	if '--ui' in argv:
		main_window.main()
		return

	sfdoc_main.main(argv)

if __name__ == "__main__":
	sys.exit(main(sys.argv))