import sys
sys.path.insert(0, '{}'.format(sys.path[0].replace('\\GUI', '\\lib')))
import os
from lib import encrypt
from lib import decrypt
from lib import reader
from lib import writer
from lib import pad
from lib import unpad
from lib import opts
from lib import timer
from lib import padpwd
from lib import padiv
from gooey import Gooey
from gooey import GooeyParser
from colored import stylize, attr, fg



color_template = 'standard' # standard, or matrix.


colorit_status = False
if color_template == 'matrix':
	bg_color = "#000000"
	font_color = "#7CFC00"
	colorit_status = True
else:
	bg_color = ''
	font_color = ''


def colorit(text_type, text):
	try:
		if text_type == 'error':
			new_txt = stylize(text, fg('light_red') + attr('bold'))
		if text_type == 'complete':
			new_txt = stylize(text, fg('dark_green') + attr('bold'))
		text = new_txt
		return new_txt
	except KeyboardInterrupt:
		sys.exit(1)


def engine(args):
	try:
		if args.Encrypt is True:
			if args.Decrypt is True:
				if colorit_status == True:
					parser.error(colorit('error', 'Cannot use --Encrypt and --Decrypt given together.'))
					sys.exit(1)
				else:
					parser.error('Cannot use --Encrypt and --Decrypt given together.')
					sys.exit(1)
			else:
				pass
		if args.Encrypt is False:
			if args.Decrypt is False:
				if colorit_status == True:
					parser.error(colorit('error', 'Must use either --Encrypt, or --Decrypt modes. Not both.'))
					sys.exit(1)
				else:
					parser.error('Must use either --Encrypt, or --Decrypt modes. Not both.')
					sys.exit(1)
			else:
				pass
		if not args.File:
			if colorit_status == True:
				parser.error(colorit('error', 'Cannot use --Encrypt, or --Decrypt without a file location.'))
				sys.exit(1)
			else:
				parser.error('Cannot use --Encrypt, or --Decrypt without a file location.')
				sys.exit(1)
		if not args.Password:
			if colorit_status == True:
				parser.error(colorit('error', 'Cannot use --Encrypt, or --Decrypt without a password.'))
				sys.exit(1)
			else:
				parser.error('Cannot use --Encrypt, or --Decrypt without a password.')
				sys.exit(1)
		if not args.IV:
			if colorit_status == True:
				parser.error(colorit('error', 'Cannot use --Encrypt, or --Decrypt without an IV.'))
				sys.exit(1)
			else:
				parser.error('Cannot use --Encrypt, or --Decrypt without an IV.')
				sys.exit(1)
		key = padpwd(args.Password)
		iv = padiv(args.IV)
		settings = opts(key, iv)
		op = reader(args.File)
		if args.Encrypt is True:
			pd = pad(op)
			enc = encrypt(pd)
			wr = writer(args.File, enc)
			if colorit_status == True:
				print(colorit('complete', 'Encryption completed for: {}'.format(args.File)))
				sys.exit(0)
			else:
				print('Encryption completed for: {}'.format(args.File))
				sys.exit(0)
		if args.Decrypt is True:
			dec = decrypt(op)
			unp = unpad(dec)
			wr = writer(args.File, unp)
			if colorit_status == True:
				print(colorit('complete', 'Decryption completed for: {}'.format(args.File)))
				sys.exit(0)
			else:
				print('Decryption completed for: {}'.format(args.File))
				sys.exit(0)
		else:
			sys.exit(0)
	except KeyboardInterrupt:
		sys.exit(1)
	except FileNotFoundError:
		if colorit_status == True:
			print(colorit('error', 'File Not Found: {}'.format(args.File)))
			sys.exit(1)
		else:
			print('File Not Found: {}'.format(args.File))
			sys.exit(1)



@Gooey(program_name="Volt, Version 1.0",
	default_size=(800, 650), 
	fullscreen=False,
	run_validators=False,
	disable_stop_button=True,
	requires_shell=False,
	show_sidebar=False,
	image_dir='{}'.format(sys.path[0].replace('\\lib', '\\Icons\\')),
	auto_start=False,
	richtext_controls=True,
	dump_build_config=False,
	header_show_title=True,
	header_show_subtitle=True,
	header_bg_color=font_color,
	body_bg_color=bg_color,
	footer_bg_color=bg_color,
	terminal_panel_color=bg_color,
	terminal_font_color=font_color,
	menu=[{
	'name': 'File',
	'items': [{
	'type': 'AboutDialog',
	'menuTitle': 'About Volt',
	'name': 'Volt',
	'description': """
Thank you for using Volt!
	
Volt was inspired just after 2010, when other open-source tools didn't offer 
the options that Volt currently supports, and to freely use them. 
As such, it stems from the belief that you should NOT have to pay to protect your files. 
Your files are yours to protect, which is why I am open-sourcing
this project so you can do such things in a cleaner, neater way.

Volt currently supports two themes(more coming soon) that
allow you to also decorate Volt your way. The default themes included
are standard(Beautiful, but plain.), and matrix(Green text, black background.).

Enjoy!
	""",
	'version': '1.0',
	'copyright': '2020',
	'website': 'https://github.com/th3tr1ckst3r/Volt/',
	'developer': 'Th3tr1ckst3r, you may contribute to get your name added here.',
	'license': 'Attribution-NonCommercial-ShareAlike 4.0 International'
	},{
	'type': 'Link',
	'menuTitle': 'Visit Project Page',
	'url': 'https://github.com/th3tr1ckst3r/Volt/'
	}]
	},{
	'name': 'Help',
	'items': [{
	'type': 'Link',
	'menuTitle': 'Documentation',
	'url': 'https://github.com/th3tr1ckst3r/Volt/wiki'
	}]
	}]
	)
def main():
	try:
		global parser
		parser = GooeyParser(description='A free, secure, and interactive AES256-bit encryption program.')
		modes = parser.add_argument_group("Required Modes(Select One.)", gooey_options={'label_color': font_color})
		opt = parser.add_argument_group("Required Options(All must be completed.)", gooey_options={'label_color': font_color})
		modes.add_argument('-e', '--Encrypt', widget="CheckBox", action='store_true',
		help='Encryption mode.', gooey_options={'label_color': font_color, 'label_bg_color': bg_color, 
		'help_color': font_color, 'help_bg_color': bg_color})
		modes.add_argument('-d', '--Decrypt', widget="CheckBox", action='store_true',
		help='Decryption mode.', gooey_options={'label_color': font_color, 'label_bg_color': bg_color, 
		'help_color': font_color, 'help_bg_color': bg_color})
		opt.add_argument('-f', '--File', widget='FileChooser', 
		help='File location.', gooey_options={'label_color': font_color, 'label_bg_color': bg_color, 
		'help_color': font_color, 'help_bg_color': bg_color})
		opt.add_argument('-p', '--Password', widget='PasswordField',
		help='Password for the file. It can be anything you want, but CANNOT exceed 32 characters in length.',
		gooey_options={'label_color': font_color, 'label_bg_color': bg_color, 
		'help_color': font_color, 'help_bg_color': bg_color})
		opt.add_argument('-iv', '--IV', widget='PasswordField',
		gooey_options={'label_color': font_color, 'label_bg_color': bg_color, 
		'help_color': font_color, 'help_bg_color': bg_color},
		help='IV for the file encryption/decryption. Must be atleast 16 characters long. You may go less than 16, but it will be less secure. The more random, the better.')
		args = parser.parse_args()
		engine(args)
	except KeyboardInterrupt:
		sys.exit(1)
		
		
if __name__ == "__main__":
	main()
	sys.exit(0)
