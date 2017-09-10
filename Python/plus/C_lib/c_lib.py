

from ctypes import *#must include , use to load c library
import threading

LIB = cdll.LoadLibrary('./test.so')# loadding 


for i in range(4):
    th = threading.Thread(target=LIB.Loop)#use the c function
    th.start()



while True:
    pass
