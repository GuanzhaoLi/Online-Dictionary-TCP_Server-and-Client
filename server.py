
from socket import *
import os
import time
import signal
import pymysql
import sys

DICT_TEXT = 'dict.txt'
HOST = '0.0.0.0'
PORT = 8888
ADDR = (HOST, PORT)

ACCEPT_NEW_DICT = True # if False, server rejects upload new dicr

# user registration
def register(c,db,data):
	print('doing user register')

	cursor = db.cursor()
	l = data.split(' ') # R name pwd
	name = l[1]
	password = l[2]

	sql = "select * from user where name = '%s'"%name 
	cursor.execute(sql)
	r = cursor.fetchone()

	if(r != None):
		c.send('EXISTS')

	sql = 'insert into user values ("%s", md5("%s"))'%(name,password)

	try:
		print('trying to create user')
		cursor.execute(sql)
		db.commit()
		c.send(b'OK')

	except:
		print('40')
		c.send(b'FALL')
		db.rollback()
		return
	else:
		print('register success')


# user login
def login(c, db, data):
	print('logging in ....')
	cursor = db.cursor()
	l = data.split(' ')
	name = l[1]
	password = l[2]

	try:
		sql = 'Select * from user where name = "%s" and passwd = md5("%s")'\
		%(name, password)
		print(sql)
		cursor.execute(sql)
		r = cursor.fetchone()

	except Exception as e:
		print(e)
		

	if(r == None):
		c.send(b'FAIL')
	else:
		c.send(b'OK')

	return

# check for word
def check_word(c, db, data):
	print('checking words....')
	cursor = db.cursor()
	l = data.split(' ')
	name = l[1]
	word = l[2]

	try:
		with open(DICT_TEXT, 'r') as f:
			c.send(b'OK')
			for line in f.readlines():	
				tmp = line.split(' ')[0]
				if(word == tmp):
					c.send(line.encode())
					insert_history(db,name,word)
					return

				elif tmp> word:
					c.send(b'not found')
					break
	except Exception as e:
		print(e)
		c.send(b'FAIL')
		print("c sent fail")
		return


# check history
def check_hist(c, db, data):
	print('checking history')
	name = data.split(' ')[1] # data: H name
	cursor = db.cursor()
	
	try:
		sql = 'select * from hist where name = "%s"'%(name)
		cursor.execute(sql)
		r = cursor.fetchall()
		if not r:
			c.send(b'FAIL')
		else:
			c.send(b'OK')

	except:
		print('checking hist failed')

	time.sleep(0.1) # split msg
	for item in r:
		msg = '%s %s %s'%(item[0], item[1], item[2])
		c.send(msg.encode())
		time.sleep(0.1) # split msg

	c.send(b'##') # tell client end




# insert word to user-specified history
def insert_history(db, name, word):
	print('inserting in to history...')
	cursor = db.cursor()
	sql = 'insert into hist value("%s", "%s", "%s")'%(name, time.ctime(), word)

	try:
		cursor.execute(sql)
		db.commit()
	except:
		db.rollback()
		return
	else:
		print('insert successful')

def give_hist_log(c, db, data):
	print('sending out hist log....')
	name = data.split(' ')[1] # data: H name
	cursor = db.cursor()
	
	try:
		sql = 'select * from hist where name = "%s"'%(name)
		cursor.execute(sql)
		r = cursor.fetchall()
		if not r:
			c.send(b'FAIL')
		else:
			c.send(b'OK')
	except Exception as e:
		print(e)

	time.sleep(0.1) # split msg
	for item in r:
		msg = '%s %s %s'%(item[0], item[1], item[2])
		c.send(msg.encode())
		time.sleep(0.1) # split msg

	c.send(b'##') # tell client end


def get_update_dict(c):

	if(ACCEPT_NEW_DICT):
		c.send(b'OK')

		with open(DICT_TEXT, 'w') as f:
			while True:
				data = c.recv(1024).decode()
				if(data == '##'):
					break
				f.write(data + '\n')
		print('updated dictionary')

	else:
		c.send(b'Not accepting new dictionary')
		print('rejected request to modify dictionary')
		return


def do_child(c, db):

	while True:
		data = c.recv(128).decode()
		print('Request: ', data)

		if(data[0] == 'R'):
			register(c, db, data)

		if(data[0] == 'E'):
			c.close()
			sys.exit(0)

		if(data[0] == 'L'):
			login(c, db, data)

		if(data[0] == 'C'):
			check_word(c, db, data)

		if(data[0] == 'H'):
			check_hist(c, db, data)

		if(data[0] == 'D'):
			give_hist_log(c, db, data)

		if(data[0] == 'U'):
			get_update_dict(c)



# listen request but with multiprocess
def main():
	db = pymysql.connect('localhost', 'root', '', 'dict')
	s = socket() # use TCP
	s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
	s.bind(ADDR)
	s.listen(5)
	signal.signal(signal.SIGCHLD, signal.SIG_IGN)

	while True:
		try:
			c, addr = s.accept()
			print('Connect from ', addr)
		except KeyboardInterrupt:
			os._exit(0)
		except:
			continue

		pid = os.fork()


		if pid < 0:
			print('Failed to create child process')
			c.close()
		elif pid == 0:
			s.close()
			do_child(c, db)
		else:
			c.close()
			continue

		db.close()
		s.close()
		os._exit(0)


if __name__ == '__main__':
	main()
