import os
import sys
import time
import shutil
import codecs
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding


def timer(num):
	try:
		time.sleep(num)
	except KeyboardInterrupt:
		sys.exit(1)


def opts(key, iv):
	try:
		global cipher
		cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
	except KeyboardInterrupt:
		sys.exit(1)


def encrypt(bin_data):
	try:
		encryptor = cipher.encryptor()
		ct = encryptor.update(bin_data) + encryptor.finalize()
		return ct
	except KeyboardInterrupt:
		sys.exit(1)
		
		
def decrypt(bin_data):
	try:
		decryptor = cipher.decryptor()
		return decryptor.update(bin_data) + decryptor.finalize()
	except KeyboardInterrupt:
		sys.exit(1)
		
		
def reader(f):
	try:
		data = open(f, 'rb').read()
		return data
	except KeyboardInterrupt:
		sys.exit(1)
		
		
def writer(f, bin_data):
	try:
		data = open(f, 'wb+')
		data.write(bin_data)
		data.close()
	except KeyboardInterrupt:
		sys.exit(1)



def pad(bin_data):
	try:
		padder = padding.PKCS7(256).padder()
		return padder.update(bin_data) + padder.finalize()
	except KeyboardInterrupt:
		sys.exit(1)



def unpad(bin_data):
	try:
		unpadder = padding.PKCS7(256).unpadder()
		data = unpadder.update(bin_data) + unpadder.finalize()
		return data
	except KeyboardInterrupt:
		sys.exit(1)
		
		
def padiv(iv):
	try:
		while True:
			if len(iv) == 16:
				return iv.encode()
			if len(iv) > 16:
				t = len(iv) - 16
				m = iv[:-t]
				return m.encode()
			else:
				iv = iv + " "
	except KeyboardInterrupt:
		sys.exit(1)
		
		
def padpwd(pwd):
	try:
		while True:
			if len(pwd) == 32:
				return pwd.encode()
			if len(pwd) > 32:
				t = len(pwd) - 32
				m = pwd[:-t]
				return m.encode()
			else:
				pwd = pwd + " "
	except KeyboardInterrupt:
		sys.exit(1)

