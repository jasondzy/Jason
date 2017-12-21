from multiprocessing import Pool
import time, os, random


def long_time_task(name): #这里创建了子进程需要运行的函数
	print('Run task %s (%s)..'%(name,os.getpid()))
	start = time.time()
	time.sleep(random.random()*3)
	end = time.time()
	print('task %s runs %0.2f seconds'%(name, (end-start)))

if __name__ == '__main__':
	print('Parent Process %s'%os.getpid())
	p = Pool(4) #使用进程池创建了4个进程，也就是该进程池中只有4个进程在运行
	for i in range(5):#这里调用for循环，往Pool中存放5次的任务，如下的apply_async函数中的args是向函数传递的参数，这是元组类型，当只有一个参数的时候需要在最后添加一个,
		p.apply_async(long_time_task, args=(i,)) #往进程池中放入需要运行的函数，由于进程池中只有四个进程，而这里放入了5个任务，所以必会有一个任务无法立刻得到运行
	print('waiting for all subprocess done...') #此处是主进程运行的打印

	p.close() # 在join前边需要调用close函数，表明不会再有任务往进程池中存放了
	p.join() #调用了join函数，表明主进程会在此处block，等待所有的子进程运行结束后才会往下运行，这里用来作为主进程和子进程的同步
	print('all subprocess done...')#运行到这里表明所有的子进程和主进程都运行完毕了