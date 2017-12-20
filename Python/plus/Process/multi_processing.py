
from multiprocessing import Process
import time 

def test():#这里表示的是子进程中所要运行的程序
	for i in range(5):
		print('---son Process---')
		time.sleep(1)

son = Process(target=test)#这里使用Process类创建了一个进程son，里边的参数是一个函数表明son这个进程需要处理的事情,参数中的test运行结束后子进程自动消亡

son.start()#start方法表示的是开始运行子进程

time.sleep(1)

#son.terminate() #Process中的terminate方法的作用是立刻停止所创建的子进程并返回，到这里子进程就结束了了，整个程序就只剩下主进程了

son.join()#这里表示的是主进程在这里等待子进程运行完毕后才会往下执行，这里起到进程的同步作用

while True:#这里表示的是主进程中所要运行的程序
	print('---parent process--')
	time.sleep(1)