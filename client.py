
from socket import *
import os
import time
import signal
import sys
import shutil


DICT_TEXT = './dict.txt'
HOST = '' # your ip
PORT = 8888
ADDR = (HOST, PORT)


# send request to check word
def check_word(s, name):
	while  True:
		word = input('word: ')
		if word == "##":
			break
		msg = 'C %s %s'%(name, word)
		s.send(msg.encode())
		data = s.recv(128).decode()

		if(data[:2] == 'OK'):
			data = s.recv(2048).decode()
			if(data[:9] == 'not fouund'):
				print('cannot find the input word')
			else:
				print(data)

		else:
			print('failed to check word')


# send request to check hist
def check_hist(s, name):
	msg = 'H %s '%name
	s.send(msg.encode())
	data = s.recv(128).decode()

	if data[:2] == 'OK':
		while True:
			data = s.recv(1024).decode()
			if(data == '##'):
				break
			print(data)
	else:
		print('failed to check hist')



# register user
def register(s):

	while True:
		name = input('please type your username: ')
		password = input('please type your password: ')
		password1 = input('retype your password: ')

		if(password != password1):
			print(password)
			print(password1)
			print('passwords not same, make sure your retype the same pwd')
			continue
		msg = 'R %s %s'%(name, password)

		s.send(msg.encode()) # send now, wait for confirmation
		data = s.recv(128).decode()

		if(data[:2] == 'OK'):
			return 0

		elif(data[:6] == 'EXISTS'):
			print('username already exist')
			return -1

		else:
			return -1



def login(s):
	name = input('username: ')
	password = input('password: ')

	msg = 'L %s %s'%(name, password)
	s.send(msg.encode())
	data = s.recv(128).decode()

	if(data[:2] == 'OK'):
		return name
	else:
		return -1

# get user history but store in a txt file instead of printing out
def download_hist(s, name):
	msg = 'D %s'%(name)
	s.send(msg.encode())
	data = s.recv(128).decode()

	if(data[:2] == 'OK'):
		try:
			filename = "downloaded_history_%s"%name
			with open(filename+'.txt', 'w') as f:
				while True:
					data = s.recv(1024).decode()
					if data == '##':
						break
					f.write(data+'\n')

			print("downloaded %s successfull"%filename)
			return
		except Exception as e:
			print(e)
	else:
		print("download failed")
		return

def update_dict(s, filename):
	backup_filename = 'old_dict_%s'%time.ctime()

	shutil.copyfile(DICT_TEXT, backup_filename+'.txt')

	print('trying to upload new dictionary....')

	s.send(b'U')

	data = s.recv(128).decode()
	if not data:
		print('server refuse to update')
		return


	try:
		with open(backup_filename+'.txt', 'r') as f:
			lines = f.readlines()
			time.sleep(0.1)
			for line in lines:
				s.send(line.encode())

		time.sleep(0.1)
		s.send(b"##")

		print('send new dict successfull')
		return


	except Exception as e:
		print(e)


def login_view(s, name):

	while True:
		print('==================WELCOME==================')
		print('====== 1: check  2: history  3: quit ======')
		print('==== 4: download history 5: upadte dict====')

		try:
			cmd = int(input('please enter option: '))
		except:
			print('please select from 1, 2, 3, 4, or 5')
			continue

		if(cmd not in [1,2,3, 4, 5]):
			print('please select from 1, 2, 3, 4, or 5')
			sys.stdin.flush()
			continue

		if(cmd == 1):
			check_word(s, name)

		if(cmd == 2):
			check_hist(s, name)

		if(cmd == 3):
			s.send(b'E')
			s.close()
			sys.exit()

		if(cmd == 4):
			download_hist(s, name)

		if(cmd == 5):
			filename = input('please give the name of new dictionary: ')
			update_dict(s, filename)



def main():
	if(len(sys.argv) != 3):
		print('need to provide host address')
		return

	HOST = sys.argv[1]
	PORT = int(sys.argv[2])
	s = socket()
	s.connect((HOST, PORT))

	while True:
		print('==================WELCOME==================')
		print('====== 1: register  2: login  3: quit======')

		try:
			cmd = int(input('please enter option: '))
		except:
			print('please select from 1, 2, or 3')
			continue

		if(cmd not in [1,2,3]):
			print('please select from 1, 2, or 3')
			sys.stdin.flush()
			continue

		if(cmd == 1):
			if(register(s) == 0):
				print('register success')
			else:
				print('failed to register')

		if(cmd == 2):
			name = login(s)
			if(name == -1):
				print('failed to login')
			else:
				login_view(s, name)

		if(cmd == 3):
			s.send(b'E')
			s.close()
			sys.exit()

if __name__ == '__main__':
	main()