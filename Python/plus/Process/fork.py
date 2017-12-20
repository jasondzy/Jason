import os
import time

pid=os.fork()

if pid == 0:
	while True:
		print('1-----This is a son process-------')
		time.sleep(1)
else:
	while True:
		print('2-----This is a parrent process---')
		time.sleep(1)

