import sys
sys.path.insert(0, '{}'.format(sys.path[0].replace('\\CLI', '\\lib')))
import os
import argparse
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


def engine(args):
	try:
		if args.Encrypt is True:
			if args.Decrypt is True:
				parser.error('Cannot use --Encrypt and --Decrypt given together.')
				sys.exit(1)
			else:
				pass
		if args.Encrypt is False:
			if args.Decrypt is False:
				parser.error('Must use either --Encrypt, or --Decrypt modes. Not both.')
				sys.exit(1)
			else:
				pass
		if not args.File:
			parser.error('Cannot use --Encrypt, or --Decrypt without a file location.')
			sys.exit(1)
		if not args.Password:
			parser.error('Cannot use --Encrypt, or --Decrypt without a password.')
			sys.exit(1)
		if not args.IV:
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
			print('Encryption completed for: {}'.format(args.File))
			sys.exit(0)
		if args.Decrypt is True:
			dec = decrypt(op)
			unp = unpad(dec)
			wr = writer(args.File, unp)
			print('Decryption completed for: {}'.format(args.File))
			sys.exit(0)
		else:
			sys.exit(0)
	except KeyboardInterrupt:
		sys.exit(1)
	except FileNotFoundError:
		print('File Not Found: {}'.format(args.File))
		sys.exit(1)


def main():
	try:
		global parser
		parser = argparse.ArgumentParser(description='A free, and secure AES256-bit encryption program.')
		modes = parser.add_argument_group("Required Modes(Select One.)")
		opt = parser.add_argument_group("Required Options(All must be completed.)")
		modes.add_argument('-e', '--Encrypt', action='store_true', help='Encryption mode.')
		modes.add_argument('-d', '--Decrypt', action='store_true', help='Decryption mode.')
		opt.add_argument('-f', '--File', action='store', required=True, help='File location.')
		opt.add_argument('-p', '--Password', action='store', required=True,
		help='Password for the file. It can be anything you want, but CANNOT exceed 32 characters in length.')
		opt.add_argument('-iv', '--IV', action='store', required=True,
		help='IV for the file encryption/decryption. Must be atleast 16 characters long. You may go less than 16, but it will be less secure. The more random, the better.')
		args = parser.parse_args()
		engine(args)
	except KeyboardInterrupt:
		sys.exit(1)
		
		
if __name__ == "__main__":
	main()
	sys.exit(0)
